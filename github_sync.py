"""Publish existing Git objects through the GitHub API without force-pushing.

No external packages. Credentials come from GITHUB_TOKEN/GH_TOKEN or Git's
credential helper and are never printed or stored in this repository.
"""
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import ssl
import subprocess
import urllib.error
import urllib.parse
import urllib.request


def run(root, *args, binary=False, check=True):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if check and result.returncode:
        raise ValueError(result.stderr.decode('utf-8', 'replace'))
    return result.stdout if binary else result.stdout.decode('utf-8', 'replace').strip()


class GitHub:
    def __init__(self, root):
        remote = run(root, 'remote', 'get-url', 'origin')
        match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)([\w.-]+/[\w.-]+?)(?:\.git)?/?', remote)
        if not match:
            raise ValueError('API 同步只支持标准 github.com 仓库地址，不接受含密码或 token 的 URL。')
        self.repo = match.group(1)
        self.root = root
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if not token:
            env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'GCM_INTERACTIVE': 'Never'}
            result = subprocess.run(['git', '-c', 'credential.interactive=false', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', text=True, capture_output=True, env=env)
            values = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
            token = values.get('password')
        if not token:
            raise ValueError('没有 GitHub 凭据。请先使用 Git Credential Manager 登录，不要将 token 写入代码。')
        self.token = token

    def request(self, method, path, body=None, allow_404=False):
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode('utf-8')
        request = urllib.request.Request('https://api.github.com' + path, data=data, method=method, headers={
            'Authorization': 'Bearer ' + self.token, 'User-Agent': 'cs336-study-lab',
            'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28'})
        # Does not change system/Git proxies. Direct API access is an explicit alternative.
        context = ssl.create_default_context()
        # Use certifi as an additional CA source if already installed; it is optional.
        try:
            import certifi
            context.load_verify_locations(certifi.where())
        except ImportError:
            pass
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=context))
        try:
            with opener.open(request, timeout=90) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if allow_404 and exc.code == 404:
                return None
            try:
                detail = json.loads(exc.read()).get('message', '')
            except (ValueError, UnicodeError):
                detail = 'request rejected'
            raise ValueError(f'GitHub API HTTP {exc.code}: {detail}; 本地提交已保留，可稍后重试。') from None
        except urllib.error.URLError as exc:
            raise ValueError('无法连接 GitHub API；本地提交已保留，可稍后重试。网络原因：' + str(exc.reason)) from None

    def repo_request(self, method, path, body=None, allow_404=False):
        return self.request(method, '/repos/' + self.repo + path, body, allow_404)


def utc_string(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat()


def sync_api(root, branch):
    api = GitHub(root)
    branch_url = urllib.parse.quote(branch, safe='')
    ref = api.repo_request('GET', '/git/ref/heads/' + branch_url, allow_404=True)
    remote = ref['object']['sha'] if ref else None
    head = run(root, 'rev-parse', 'HEAD')
    if remote == head:
        print('GitHub 已是最新版本。')
        run(root, 'update-ref', 'refs/remotes/origin/' + branch, head)
        return
    if remote:
        ancestor = subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', remote, head], capture_output=True)
        if ancestor.returncode:
            raise ValueError('远端包含本地尚未合并的提交；请先 fetch / pull 处理后再同步，不会覆盖远端。')
    commits = run(root, 'rev-list', '--reverse', (remote + '..HEAD') if remote else 'HEAD').splitlines()
    remote_blobs = set()
    if remote:
        tree = api.repo_request('GET', '/git/trees/' + remote + '?recursive=1')
        if tree.get('truncated'):
            raise ValueError('远端文件树过大，需改用普通 Git 推送。')
        remote_blobs = {x['sha'] for x in tree['tree'] if x['type'] == 'blob'}
    for commit in commits:
        values = run(root, 'show', '-s', '--format=%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI', commit).split('\0')
        info = dict(zip(('author_name', 'author_email', 'author_date', 'committer_name', 'committer_email', 'committer_date'), values))
        # The REST API normalizes dates to UTC; do not rewrite manual commits.
        if not all(info[key].endswith(('+00:00', 'Z')) for key in ('author_date', 'committer_date')):
            raise ValueError('此提交使用非 UTC 的 Git 时间戳；为保留原提交哈希，请使用普通 Git 推送。工作台自动提交使用 UTC。')
        entries = []
        inline = set()
        for entry in run(root, 'ls-tree', '-rz', commit, binary=True).split(b'\0'):
            if not entry:
                continue
            attrs, path = entry.split(b'\t', 1)
            mode, kind, sha = attrs.decode().split()
            if kind != 'blob':
                raise ValueError('API 备用同步不支持 submodule；请使用普通 Git。')
            item = {'path': path.decode('utf-8'), 'mode': mode, 'type': kind, 'sha': sha}
            if sha not in remote_blobs:
                data = run(root, 'cat-file', 'blob', sha, binary=True)
                if len(data) > 90 * 1024 * 1024:
                    raise ValueError('文件过大，先把训练产物移出 Git，再推送。')
                try:
                    text = data.decode('utf-8')
                    if '\0' in text or len(data) > 2 * 1024 * 1024:
                        raise UnicodeError()
                    del item['sha']
                    item['content'] = text
                    inline.add(sha)
                except UnicodeError:
                    obj = api.repo_request('POST', '/git/blobs', {'content': base64.b64encode(data).decode('ascii'), 'encoding': 'base64'})
                    if obj['sha'] != sha:
                        raise ValueError('上传对象校验失败，停止同步。')
                    remote_blobs.add(sha)
            entries.append(item)
        tree = api.repo_request('POST', '/git/trees', {'tree': entries})
        expected_tree = run(root, 'rev-parse', commit + '^{tree}')
        if tree['sha'] != expected_tree:
            raise ValueError('文件树校验失败，远端分支未更新。')
        remote_blobs.update(inline)
        # Preserve trailing newlines in the raw commit message.
        raw = run(root, 'cat-file', 'commit', commit, binary=True)
        message = raw.split(b'\n\n', 1)[1].decode('utf-8')
        parents = run(root, 'show', '-s', '--format=%P', commit).split()
        created = api.repo_request('POST', '/git/commits', {
            'message': message, 'tree': tree['sha'], 'parents': parents,
            'author': {'name': info['author_name'], 'email': info['author_email'], 'date': utc_string(info['author_date'])},
            'committer': {'name': info['committer_name'], 'email': info['committer_email'], 'date': utc_string(info['committer_date'])}})
        if created['sha'] != commit:
            raise ValueError('提交哈希与本地不一致；远端分支未更新，请改用普通 Git 推送。')
    # No force: protects against remote changes while objects were uploading.
    if ref:
        api.repo_request('PATCH', '/git/refs/heads/' + branch_url, {'sha': head, 'force': False})
    else:
        api.repo_request('POST', '/git/refs', {'ref': 'refs/heads/' + branch, 'sha': head})
    run(root, 'update-ref', 'refs/remotes/origin/' + branch, head)
    run(root, 'config', 'branch.' + branch + '.remote', 'origin')
    run(root, 'config', 'branch.' + branch + '.merge', 'refs/heads/' + branch)
    print('已通过 GitHub API 同步，并校验文件树与提交哈希。')
