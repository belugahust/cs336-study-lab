# CS336 学习工作台

跟着 **Stanford CS336 · Spring 2025**，把视频笔记、官方作业、中文参考资料和每次学习的数据留在同一个仓库。所有进度从零开始，由你亲自记录。

## 从这里开始

1. 安装 Python 3.10+ 和 Git。记录工具仅用 Python 标准库，无需安装依赖。
2. 打开本仓库文件夹的终端，运行 `python study.py status`。
3. 打开 [第 01 讲笔记](lectures/01/notes.md)，按“看完后要能做到 → 动手任务 → 所需资料”学习。
4. 打开 [作业一分步路线](assignments/01-basics/LEARNING_GUIDE.md)，边做边测。
5. 课后编辑本讲笔记，再运行下方命令记录并推送。

你也可以双击 `index.html` 查看本地学习看板；运行记录命令后刷新。看板展示笔记和搜索，不会自行上传资料。GitHub 首页看 [学习进度](PROGRESS.md)，无需部署网站。

## 每节课之后：一条命令记录并同步

```powershell
python study.py record --lecture 1 --minutes 60 --summary "理解 UTF-8 字节与 BPE 合并" --question "预分词怎样处理特殊 token？" --watched --push --api
```

上面是格式示例，不是预先填入的成绩。把讲次、用时和总结改成你真实完成的内容。

- `--watched`：本讲视频看完；只是看了一部分就不加。
- `--practice`：本讲笔记中安排的练习完成；不代表整份作业已经完成。
- `--minutes`：只填本次学习时间，不是累计时间。
- `--video "https://..."`：可记录自己的 B 站视频 / 分 P 链接，避免不同搬运版本编号混淆。
- `--push`：提交本项目所有未忽略的更改并推送，包括你手动修改的笔记与作业代码。省略时只保存在本地。
- Windows 可用 `powershell -ExecutionPolicy Bypass -File scripts/check-in.ps1`，按提示填写，默认只保存在本地，可主动选择推送。

推送失败不会删除本地记录。处理网络或登录问题后，运行下面的同步命令即可，**不要重复 record 同一次学习**：

```powershell
python study.py sync --api --message "study: update notes and progress"
```

这是一套“主动课后提交”的流程，不会监控你看视频，也不会后台定时提交。

## 实验数据也一起记

```powershell
python study.py experiment --assignment 1 --name tinystories-small --metric val_loss=2.3 --metric tokens_per_second=1200 --config "configs/small.json; steps=2000" --seed 42 --device "填写实际设备" --summary "填写实际观察" --push --api
```

这些数值只是参数格式示例；请替换为真实结果。建议在 `experiments/` 写实验报告和小配置，把大数据集和权重放在 Git 之外。

## 项目结构

```text
lectures/01..19/notes.md     每讲目标、练习、资料链接与个人笔记
assignments/01..05-*        A1–A4 官方框架与 A5 下载入口（本地 upstream）
references/weiruihhh/       中文笔记 PDF / Markdown 与参考实现
references/shallowu/        作业 1、2、5 参考代码，原 README 含博客 / Colab
resources/INDEX.md          统一资料入口与按任务查找的对照表
resources/sources.lock.json 上游 commit、下载文件哈希和来源
records/                   学习原始记录 JSONL 与导出 CSV
experiments/               自己的实验报告与小配置
PROGRESS.md / index.html    自动生成的进度页 / 本地看板
study.py                   记录、统计、渲染与 GitHub 同步
```

## 怎么跟课，怎么用参考资料

第一份作业的主要视频基础是第 1–3 讲；第 1 讲后就能开始 BPE。优化器、训练循环、实验细节继续按官方 PDF 学，不必等看完整门课。第 4 讲 MoE 不是 A1 必做内容。后续作业不是严格的一讲对应一小题，分配表是本项目的学习建议，正式要求以 handout 为准。

推荐次序：**官方 PDF 理解任务 → 自己写小例子 → 中文笔记解释卡点 → 必要时对照局部参考实现 → 回到自己的实现跑官方测试**。每讲只推进一小步。

原课程面向在校生有独立完成作业的要求；本仓库把第三方代码明确标为参考，不能把它当成自己的课程提交。第三方实现没有在这里全部跑通或认证，不保证完全正确。

## 运行官方作业

记录工具与作业环境分开。先安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，再进入对应作业目录：

```powershell
cd assignments/01-basics
uv sync
uv run pytest tests/test_train_bpe.py -q
```

学生框架初始报 `NotImplementedError` 是预期行为，不等于环境坏了。先做小张量和 CPU 正确性测试，再按作业要求使用 GPU。Triton、分布式与部分依赖适合 Linux / WSL2；不要假定 Windows 原生可以运行所有五份作业。具体依赖以各作业原 README 和 pyproject 为准。

## 连接 / 更换 GitHub 仓库

首次下载 ZIP 的用户需要 `git init -b main`。从 GitHub clone 的用户不必重复初始化。

```powershell
git config user.name "你的 GitHub 用户名"
git config user.email "你的 GitHub 提交邮箱或 noreply 邮箱"
git remote add origin https://github.com/你的用户名/你的仓库.git
python study.py sync --api --message "study: initialize learning workspace"
```

如果已有 origin，使用 `git remote set-url origin ...`。GitHub HTTPS 推送需要 Git Credential Manager 等已登录的凭据，账户密码不能作为 GitHub Git 密码。不要把 token 写进代码或远端 URL。脚本默认普通 Git 推送。此电脑当前普通 Git 连接不可用，建议课后命令加 `--push --api`，或使用 `python study.py sync --api`；API 同步从系统 Git 凭据读取认证，不用额外配置密钥。

默认同步到当前分支，不强制覆盖远端。远端有其他提交时先处理同步/冲突。API 同步也会检查远端祖先关系，不覆盖他人更新。若机器代理失效，请先修复网络配置；脚本不会擅自修改全局代理。

## 项目自身验证

```powershell
python -m unittest discover -s tests -v
python study.py render --check
```

这里只验证记录和同步工具；不会替你通过尚未实现的官方作业测试。GitHub Actions 同样只检查工作台工具。

## 来源与许可

官方课程：[2025 日程](https://stanford-cs336.github.io/spring2025/)。资料快照固定版本，不会自动覆盖你的作业。完整来源、保留范围、第三方许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。中文笔记采用 CC BY-NC-SA 4.0，不能把整个资料包当作可商用的 MIT 项目。
