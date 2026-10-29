#!/usr/bin/env python3
"""CS336 study journal. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone, timedelta
import uuid

ROOT = Path(__file__).resolve().parent
TZ = timezone(timedelta(hours=8))


def load_course(root):
    return json.loads((root / "course.json").read_text(encoding="utf-8"))


def read_events(root):
    path = root / "records/sessions.jsonl"
    events = []
    if path.exists():
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{n}: invalid JSON; restore this line before continuing") from exc
    return events


def stamp():
    return datetime.now(TZ).isoformat(timespec="seconds")


def append_event(root, event):
    # Verify existing records before adding another one.
    read_events(root)
    path = root / "records/sessions.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {"id": uuid.uuid4().hex, "timestamp": stamp(), **event}
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
    return event


def states(course, events):
    result = {x["id"]: {"minutes": 0, "sessions": 0, "watched": False, "practice": False} for x in course["lectures"]}
    for e in events:
        if e.get("kind") == "session":
            s = result[e["lecture"]]
            s["minutes"] += e["minutes"]
            s["sessions"] += 1
            s["watched"] |= e.get("watched", False)
            s["practice"] |= e.get("practice", False)
    return result


def esc(value):
    return html.escape(str(value), quote=True)


def md_cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>").replace("\r", "")


def render(root, check=False):
    course = load_course(root)
    events = read_events(root)
    state = states(course, events)
    watched = sum(s["watched"] for s in state.values())
    practiced = sum(s["practice"] for s in state.values())
    minutes = sum(s["minutes"] for s in state.values())
    n = len(course["lectures"])
    md = ["# 学习进度", "", "由 `python study.py render` 生成；数据来源：`records/sessions.jsonl`。", "",
          f"已看完视频 **{watched}/{n}** · 已做本讲练习 **{practiced}/{n}** · 累计学习 **{minutes} 分钟**", "",
          "视频与练习分别统计；练习标记不表示整份作业已完成。初始状态不假设你已经学过任何一讲。", "",
          "| 讲次 | 内容 | 视频 | 本讲练习 | 用时（分钟） |", "|---|---|---|---|---|"]
    cards = []
    for lecture in course["lectures"]:
        i, title, note = lecture["id"], lecture["title"], lecture["note"]
        s = state[i]
        md.append(f"| {i:02d} | [{title}]({note}) | {'✅' if s['watched'] else '—'} | {'✅' if s['practice'] else '—'} | {s['minutes']} |")
        goals = "".join(f"<li>{esc(g)}</li>" for g in lecture["goals"])
        resources = "".join(f'<li><a href="{esc(r["path"])}">{esc(r["label"])}</a></li>' for r in lecture["resources"])
        text = (root / note).read_text(encoding="utf-8")
        cards.append(f'''<article><div class="eyebrow">LECTURE {i:02d} · {esc(lecture['assignment'])}</div>
<h2>{esc(title)}</h2><p class="status">视频：{'已看完' if s['watched'] else '待学习'}　练习：{'已完成' if s['practice'] else '待练习'}　{s['minutes']} 分钟</p>
<ul>{goals}</ul><details><summary>本讲资料与笔记</summary><ul>{resources}</ul>
<p><a href="{esc(note)}">打开 Markdown 笔记文件</a>（编辑后重新运行 render）</p><pre>{esc(text)}</pre></details>
<code>python study.py record --lecture {i} --minutes 60 --summary "本次收获" --watched --push</code></article>''')
    md += ["", "## 最近记录", "", "| 时间（UTC+8） | 类型 | 内容 |", "|---|---|---|"]
    for e in reversed(events[-20:]):
        label = f"第 {e['lecture']} 讲" if e["kind"] == "session" else f"A{e['assignment']} 实验"
        md.append(f"| {md_cell(e['timestamp'])} | {label} | {md_cell(e.get('summary', e.get('name', '')))} |")
    if not events:
        md.append("| — | — | 尚无学习记录 |")
    md += ["", "完整结构化数据保存在 `records/`；代码与手写笔记直接使用 Git 追踪。", ""]
    css = """*{box-sizing:border-box}body{margin:0;background:#f4f5f1;color:#182522;font:16px/1.7 system-ui,'Microsoft YaHei',sans-serif}main{max-width:1040px;margin:auto;padding:48px 24px}header{padding-bottom:30px;border-bottom:1px solid #ccd7cf}h1{font-size:38px;line-height:1.25;margin:12px 0}h2{font-size:22px;margin:8px 0}.eyebrow{font-size:12px;letter-spacing:.12em;color:#43645a}.stats{display:flex;flex-wrap:wrap;gap:14px;margin:24px 0}.stats div{background:#174d3e;color:#fff;border-radius:12px;padding:16px 26px}.stats b{font-size:30px;display:block}.nav{display:flex;flex-wrap:wrap;gap:18px}a{color:#14634d}article{background:white;border:1px solid #dce3dd;border-radius:12px;padding:24px;margin:18px 0}article code{display:block;background:#f1f4f0;padding:12px;overflow:auto;font-size:12px}.status{color:#597066;font-size:14px}summary{cursor:pointer;color:#14634d;padding:8px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f7f8f5;padding:18px;font:14px/1.7 ui-monospace,monospace}input{width:100%;padding:12px 16px;border:1px solid #b8c9be;border-radius:8px;margin:24px 0 8px;font:inherit}footer{font-size:13px;color:#597066;margin-top:30px}button{padding:9px 14px;cursor:pointer}@media(max-width:600px){main{padding:25px 16px}h1{font-size:29px}article{padding:18px}}"""
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CS336 学习工作台</title><style>{css}</style></head>
<body><main><header><div class="eyebrow">STANFORD CS336 · SPRING 2025 · PERSONAL LEARNING LAB</div><h1>一讲一记录，一步一步构建语言模型。</h1><p>官方作业、中文参考资料与自己的实现放在一起。先理解，再动手，最后记录。</p>
<nav class="nav"><a href="README.md">开始使用</a><a href="resources/INDEX.md">全部资料</a><a href="assignments/01-basics/LEARNING_GUIDE.md">作业一分步路线</a><a href="PROGRESS.md">GitHub 进度页</a></nav></header>
<section class="stats"><div><b>{watched}/{n}</b>已看完视频</div><div><b>{practiced}/{n}</b>完成本讲练习</div><div><b>{minutes}</b>累计分钟</div></section>
<p>完成练习由你主动标记，不等同于自动通过测试。这里展示的是本地生成时的记录；更新后刷新页面。</p>
<label for="search">查找课程 / 知识点</label><input id="search" placeholder="例如：分词、PyTorch、对齐、推理"><section id="lessons">{''.join(cards)}</section>
<footer>数据文件 records/sessions.jsonl · 全部初始进度为零 · 不自动上传，只有 --push 或 sync 才会推送。</footer></main>
<script>document.getElementById('search').addEventListener('input',function(){{let q=this.value.trim().toLowerCase();for(let a of document.querySelectorAll('article'))a.hidden=!a.textContent.toLowerCase().includes(q);}});</script></body></html>'''
    csvbuf = io.StringIO(newline="")
    fields = ["id", "timestamp", "kind", "lecture", "minutes", "summary", "question", "video", "watched", "practice", "assignment", "name", "metrics", "config", "seed", "device"]
    writer = csv.DictWriter(csvbuf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for e in events:
        writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v for k, v in e.items()})
    outputs = {"PROGRESS.md": "\n".join(md), "index.html": page, "records/summary.csv": csvbuf.getvalue()}
    stale = []
    for name, content in outputs.items():
        path = root / name
        if check:
            if not path.exists() or path.read_text(encoding="utf-8").replace("\r\n", "\n") != content.replace("\r\n", "\n"):
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        raise ValueError("进度文件需要更新：" + ", ".join(stale) + "；运行 python study.py render")


def git(root, *args, check=True, env=None):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if check and result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip() or "Git command failed")
    return result


def sync(root, message, api_only=False):
    top = git(root, "rev-parse", "--show-toplevel", check=False)
    if top.returncode or Path(top.stdout.strip()).resolve() != root.resolve():
        raise ValueError("当前项目尚未初始化为独立 Git 仓库。请先按 README 连接 GitHub。")
    if git(root, "remote", "get-url", "origin", check=False).returncode:
        raise ValueError("尚未设置 origin；学习记录已经保存在本地。请先按 README 连接 GitHub。")
    if git(root, "var", "GIT_AUTHOR_IDENT", check=False).returncode:
        raise ValueError("请先设置此仓库的 git user.name 和 user.email。")
    branch = git(root, "symbolic-ref", "--short", "HEAD", check=False)
    if branch.returncode:
        raise ValueError("当前是 detached HEAD；请切换到学习分支后再同步。")
    if git(root, "diff", "--name-only", "--diff-filter=U").stdout.strip():
        raise ValueError("存在合并冲突；请先解决冲突，再同步。")
    render(root)
    git(root, "add", "--all", "--", ".")
    if git(root, "diff", "--cached", "--quiet", check=False).returncode:
        now_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
        git(root, "commit", "-m", message, env={**os.environ, "GIT_AUTHOR_DATE": now_utc, "GIT_COMMITTER_DATE": now_utc})
        print("已创建本地提交。")
    # Also retries a previously failed push when there are no new changes.
    if api_only:
        from github_sync import sync_api
        sync_api(root, branch.stdout.strip())
        return
    pushed = git(root, "push", "--set-upstream", "origin", branch.stdout.strip(), check=False)
    if pushed.returncode:
        raise ValueError("学习记录和本地提交已保留，但推送失败。检查网络/登录或远端冲突后运行 python study.py sync；GitHub API 可用时可运行 python study.py sync --api。\n" + pushed.stderr.strip())
    print("已同步到 GitHub。")


def positive(value):
    n = int(value)
    if n <= 0:
        raise argparse.ArgumentTypeError("必须大于 0")
    return n


def parse_metrics(items):
    metrics = {}
    for item in items:
        if "=" not in item:
            raise ValueError("指标格式应为 --metric val_loss=1.8")
        name, value = item.split("=", 1)
        if not name or name in metrics:
            raise ValueError("指标名称不能为空或重复")
        value = float(value)
        if not math.isfinite(value):
            raise ValueError("指标必须是有限数字")
        metrics[name] = value
    return metrics


def main(argv=None, root=ROOT):
    parser = argparse.ArgumentParser(description="CS336 课后记录与 GitHub 同步")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="查看进度")
    render_parser = sub.add_parser("render", help="更新进度 Markdown、CSV 和本地网页")
    render_parser.add_argument("--check", action="store_true")
    record = sub.add_parser("record", help="追加一次学习记录（默认只保存在本地）")
    record.add_argument("--lecture", type=int, required=True)
    record.add_argument("--minutes", type=positive, required=True)
    record.add_argument("--summary", required=True)
    record.add_argument("--question", default="")
    record.add_argument("--video", default="")
    record.add_argument("--watched", action="store_true", help="标记本讲视频已经看完")
    record.add_argument("--practice", action="store_true", help="标记本讲笔记要求的练习已完成，不代表整份作业完成")
    record.add_argument("--push", action="store_true")
    record.add_argument("--api", action="store_true", help="与 --push 一起使用，通过 GitHub API 推送")
    exp = sub.add_parser("experiment", help="追加一条实验记录")
    exp.add_argument("--assignment", type=int, choices=range(1, 6), required=True)
    exp.add_argument("--name", required=True)
    exp.add_argument("--metric", action="append", default=[])
    exp.add_argument("--config", default="", help="配置文件相对路径或配置说明")
    exp.add_argument("--seed", type=int)
    exp.add_argument("--device", default="")
    exp.add_argument("--summary", default="")
    exp.add_argument("--push", action="store_true")
    exp.add_argument("--api", action="store_true", help="与 --push 一起使用，通过 GitHub API 推送")
    sp = sub.add_parser("sync", help="提交本项目所有未忽略的更改并推送")
    sp.add_argument("--message", default="study: update notes and progress")
    sp.add_argument("--api", action="store_true", help="绕过普通 Git 网络连接，通过 GitHub API 同步（需要已登录凭据）")
    args = parser.parse_args(argv)
    try:
        course = load_course(root)
        if args.command == "status":
            ss = states(course, read_events(root))
            print(f"CS336 2025：视频 {sum(s['watched'] for s in ss.values())}/{len(ss)}；练习 {sum(s['practice'] for s in ss.values())}/{len(ss)}；累计 {sum(s['minutes'] for s in ss.values())} 分钟")
            print("笔记入口：lectures/；资料入口：resources/INDEX.md；本地看板：index.html")
        elif args.command == "render":
            render(root, args.check)
            print("进度文件检查通过。" if args.check else "进度页、CSV 和本地看板已更新。")
        elif args.command in ("record", "experiment"):
            if args.api and not args.push:
                raise ValueError("--api 需要与 --push 一起使用；只保存本地时无需 --api")
            if args.command == "record":
                if args.lecture not in {x["id"] for x in course["lectures"]}:
                    raise ValueError("讲次不存在；2025 版讲次为 1–19")
                if not args.summary.strip():
                    raise ValueError("请写一句本次学习的收获，summary 不能为空")
                if args.video and not args.video.startswith(("https://", "http://")):
                    raise ValueError("video 应是 http(s) 视频链接")
                event = {"kind": "session", **{k: getattr(args, k) for k in ("lecture", "minutes", "summary", "question", "video", "watched", "practice")}}
                message = f"study: lecture {args.lecture:02d} session"
            else:
                if not args.name.strip():
                    raise ValueError("实验名称不能为空")
                event = {"kind": "experiment", **{k: getattr(args, k) for k in ("assignment", "name", "config", "seed", "device", "summary")}, "metrics": parse_metrics(args.metric)}
                message = f"experiment: A{args.assignment} {args.name}"
            saved = append_event(root, event)
            render(root)
            print(f"已保存在本地：{saved['id']}。同一讲可以多次记录；每次 minutes 只填本次用时。")
            if args.push:
                sync(root, message, args.api)
        elif args.command == "sync":
            sync(root, args.message, args.api)
    except (ValueError, OSError, KeyError) as exc:
        print(f"操作未完成：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
