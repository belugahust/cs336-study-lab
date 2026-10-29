"""Download the pinned official A5 into a Git-ignored local directory."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import tempfile
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / 'assignments/05-alignment/upstream'
    if target.exists():
        print('A5 upstream already exists; keeping your current files untouched.')
        return
    lock = json.loads((ROOT / 'resources/sources.lock.json').read_text(encoding='utf-8'))
    repo = 'stanford-cs336/assignment5-alignment'
    source = next(s for s in lock['sources'] if s['repo'] == repo)
    files = [f for f in lock['files'] if f['repo'] == repo]
    if not files:
        raise ValueError('No pinned A5 files in lockfile')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.a5-download-', dir=target.parent) as scratch:
        scratch = Path(scratch)

        def download(item):
            relative = Path(item['source_path'])
            destination = scratch / relative
            if relative.is_absolute() or not destination.resolve().is_relative_to(scratch.resolve()):
                raise ValueError('Invalid source path')
            url = 'https://raw.githubusercontent.com/' + repo + '/' + source['commit'] + '/' + urllib.parse.quote(item['source_path'], safe='/')
            request = urllib.request.Request(url, headers={'User-Agent': 'cs336-study-lab'})
            with urllib.request.urlopen(request, timeout=120) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError('File checksum mismatch: ' + item['source_path'])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for n, _ in enumerate(pool.map(download, files), 1):
                if n % 20 == 0:
                    print(f'Verified {n}/{len(files)} files', flush=True)
        # Temp directory cleanup sees only an empty directory after this rename.
        scratch.rename(target)
    print('Downloaded and verified A5. See assignments/05-alignment/upstream/README.md')


if __name__ == '__main__':
    main()
