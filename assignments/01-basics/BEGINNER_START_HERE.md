# 作业一新手指南：先知道在哪里写，再开始实现

这份指南面向已经看过一些视频，但不知道如何开始写作业的人。第一次只做第 1–6 步，目标是**能打开项目、运行一个小程序，并看到官方测试开始执行**。不要求第一天完成分词器，更不要求第一天训练大模型。

## 1. 先分清楚你要用的东西

| 名称 | 是什么 | 这次拿它做什么 |
|---|---|---|
| VS Code | 代码编辑器 | 打开整个项目、编辑 Python 文件、打开终端 |
| Python 3.11 | 执行 Python 代码的程序 | 运行你写的代码、测试和学习记录工具 |
| 终端 / PowerShell | 输入命令的窗口 | 安装依赖、运行程序和测试，不是在这里写整份作业 |
| uv | Python 项目环境管理工具 | 按作业规定的版本安装 PyTorch 等依赖 |
| `.venv` | 此作业自己的 Python 环境文件夹 | 隔离依赖，避免和别的项目混用 |
| PyTorch / torch | 张量与深度学习库 | 从矩阵运算开始构建 Transformer；BPE 算法本身不需要 GPU |
| pytest | 自动检查代码的工具 | 用官方准备的输入与正确结果检查你的实现 |
| Git | 本地版本管理工具 | 记录你每次改了什么 |
| GitHub | 远程代码仓库网站 | 保存和展示 Git 提交；代码不需要在网页上写 |

**推荐软件组合：VS Code + Python 3.11 + uv + Git。**现在不用额外学习 PyCharm、Jupyter、Docker，也不用先租服务器。并不是这些不能用，只是先用这一套即可。

写作业的流程是：**VS Code 编辑 `.py` 文件并保存 → 终端运行测试 → 根据错误修改 → 再测试 → GitHub 保存进度**。

## 2. 打开正确的文件夹

这台电脑已经有一份完整项目，不需要重新下载。打开 VS Code，选择：

**文件 → 打开文件夹 → 选择 `cs336-study-lab` 文件夹**。

本次交付在 Windows 上的位置是：

```text
C:\Users\10042\Documents\Codex\2026-10-28\wo\outputs\cs336-study-lab
```

如果以后移动了项目，使用新位置；目录路径不是课程要求。也可以双击项目内的 `cs336-study.code-workspace` 打开工作区。

在 VS Code 左侧“扩展”里安装 Microsoft 发布的 **Python** 扩展（标识 `ms-python.python`）；Pylance 可作为代码提示补充。扩展是编辑辅助，Python 运行环境仍要按下一步配置。

现在看左侧文件树：

```text
cs336-study-lab/                       ← 整个学习仓库：打开这个文件夹
├─ study.py                           ← 学习记录工具，不是模型训练程序
├─ lectures/01/notes.md                ← 第一讲自己的笔记
├─ references/                        ← 两个辅助仓库的笔记与参考实现
└─ assignments/
   └─ 01-basics/                      ← 作业一目录
      ├─ cs336_spring2025_assignment1_basics.pdf ← 官方任务说明（实际文件名见目录）
      ├─ pyproject.toml               ← 依赖要求
      ├─ uv.lock                      ← 固定依赖版本
      ├─ cs336_basics/                ← 你的 Python 实现放在这里
      │  └─ bpe.py                    ← 已准备空白 BPE 骨架，等你实现
      ├─ playground/                  ← 小练习，可先在这里尝试
      │  └─ 01_bytes.py               ← 不需要第三方依赖的字节练习
      ├─ tests/
      │  ├─ adapters.py               ← 连接你的代码与官方测试
      │  ├─ test_train_bpe.py          ← BPE 自动测试：用来运行和阅读
      │  └─ fixtures/                 ← 测试使用的小数据，已经有了
      └─ .venv/                      ← 环境配置后生成，不上传 GitHub
```

**主要编辑 `cs336_basics/` 下你自己的文件；按需要修改 `tests/adapters.py` 中对应的函数体。**`test_*.py`、`fixtures/`、`_snapshots/` 是检查依据，保留原样。`references/` 是参考资料入口，不是你的作业工作目录。

## 3. 打开终端，理解“当前在哪个目录”

在 VS Code 顶部选择 **终端 → 新建终端**，Windows 下选择 PowerShell 即可。

以下命令块中的每一行都是终端命令，输入后按回车。只复制命令本身，不要复制代码块的三条反引号，也不要复制 `PS C:\...>` 这样的终端提示。

先输入：

```powershell
Get-Location
```

它显示终端当前目录。若不是项目根目录，执行：

```powershell
cd "C:\Users\10042\Documents\Codex\2026-10-28\wo\outputs\cs336-study-lab"
```

再进入作业一：

```powershell
cd assignments/01-basics
```

此时终端路径应以 `assignments\01-basics` 结尾。在这里输入 `Get-ChildItem`，应该看到 `pyproject.toml`、`tests` 和 `cs336_basics`。

**后面所有 `uv ...` 命令都从作业一目录运行；`study.py ...` 命令从项目根目录运行。**把二者放在不同目录运行，是常见报错原因。

## 4. 配置作业一环境：两条路线选一条

### 路线 A：使用本项目的一键脚本（推荐）

回到项目根目录（若当前在作业一，`cd ../..`）：

```powershell
cd ../..
powershell -ExecutionPolicy Bypass -File scripts/setup-a1.ps1
```

脚本会依次：

1. 检查电脑能否执行 Python 3.11 或更高版本。
2. 在项目 `.tools/` 创建工具环境并安装 uv，不修改全局 Python 包。
3. 按官方锁定文件为作业一创建 `.venv`，安装所需库。
4. 打印 Python、PyTorch、CUDA 可用性，并执行“收集测试”。

安装需要联网下载 Python / 依赖，PyTorch 体积较大；第一次耗时取决于网络。脚本不会安装显卡驱动、CUDA Toolkit、WSL，也不会修改官方依赖文件。若发生错误，先看终端末尾；失败后可以重跑。uv 安装设置了网络超时，失败时会停止并显示错误。

**本次准备状态（2026-10-29）**：已确认这台电脑有 VS Code 与 Python 3.11.9，字节练习已运行通过；联网安装 uv 时下载长时间没有进展，已停止该次安装。因此作业 `.venv` 尚未建成，官方测试尚未在本机执行，不要把“指南已准备”误认为“环境已全部装好”。网络恢复后重跑上面的脚本即可。项目学习记录工具的测试与官方作业测试是两回事。

“收集测试”只是确认 pytest 能找到测试，不会替你写算法，也不说明作业已经通过。

### 路线 B：自己输入命令（已经安装 uv 的用户）

如果 `uv --version` 已可执行，从作业一目录运行：

```powershell
uv sync --frozen --python 3.11
uv run --frozen python -c "import sys, torch; print(sys.executable); print(torch.__version__); print(torch.cuda.is_available())"
uv run --frozen pytest tests/test_train_bpe.py --collect-only -q
```

这里选 Python 3.11 以减少版本差异；官方要求是 Python >=3.11，作业锁定的 PyTorch 系列是 2.6。`--frozen` 表示按已有锁定文件安装/运行，不自行重新求解并改写锁文件。

`torch.cuda.is_available()` 输出 **False** 只表示当前环境不能使用 NVIDIA CUDA，**不等于环境配错**。你仍可以写分词器和做 CPU 小测试。完整训练是否可行取决于模型、训练要求与设备，届时再安排 GPU。

### 如果用了一键脚本，后面怎样调用 uv？

一键脚本把 uv 安装在 `.tools/`，不会把 `uv` 加入系统 PATH。以下两种用法选一种：

从项目根目录，使用本项目的包装脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/a1.ps1 python -c "import torch; print(torch.__version__)"
powershell -ExecutionPolicy Bypass -File scripts/a1.ps1 pytest tests/test_train_bpe.py --collect-only -q
```

或者从作业一目录，显式调用 uv 所在的 Python：

```powershell
& ../../.tools/Scripts/python.exe -m uv run --frozen pytest tests/test_train_bpe.py --collect-only -q
```

下面讲解用常见的 `uv run --frozen ...` 写法；若用了路线 A，把命令中 `uv run --frozen` 换成上面的显式调用，或使用根目录 `scripts/a1.ps1` 包装脚本。

## 5. 告诉 VS Code：作业用哪个 Python

按 `Ctrl+Shift+P`，输入 **Python: Select Interpreter**（选择解释器），选择：

```text
assignments\01-basics\.venv\Scripts\python.exe
```

如果列表没出现，选择“输入解释器路径”，手动找到这个文件。先完成环境安装才会有这个文件。

它决定 VS Code 用哪个环境做代码提示和运行。**终端手动运行 `python ...` 仍可能调用系统 Python**，所以作业统一使用 `uv run --frozen ...` 或 `scripts/a1.ps1`，避免混用。无需手动激活 `.venv`，也不用先处理 PowerShell 的 `Activate.ps1` 权限问题。

## 6. 先运行一个一定能看懂的小练习

在左侧打开 `assignments/01-basics/playground/01_bytes.py`，读里面的注释。

从项目根目录运行：

```powershell
python assignments/01-basics/playground/01_bytes.py
```

这个练习不依赖 PyTorch，环境安装前也可以运行。它展示字符串、UTF-8 编码、每个字节和解码，还展示一次指定的相邻符号合并。它不是完整 BPE 作业答案。

接着自己在文件中把 `text = "你好，AI"` 改成另一句话，按 `Ctrl+S` 保存，再运行同一条命令。比较中文和英文字符各占多少字节。

**你已经完成了一次实际编程流程：打开文件 → 改代码 → 保存 → 执行 → 观察输出。**

## 7. 作业一究竟要做出什么？

最终目标：从文本出发，自己实现一个小型 Transformer 语言模型的分词、模型、训练和生成流程。

```text
原始文本
  → BPE 训练得到词表 / 合并规则
  → tokenizer 把文本变成 token ID
  → Transformer 根据上下文预测下一个 token
  → 损失和优化器更新模型参数
  → 保存模型，按概率生成后续 token，再解码成文本
```

这是多阶段项目，不是一份十几行的练习。建议顺序：

| 阶段 | 大致在哪写（文件名是建议） | 做完怎样检查 |
|---|---|---|
| BPE 训练 | `cs336_basics/bpe.py` | `tests/test_train_bpe.py` |
| tokenizer 编码/解码 | 自建 `cs336_basics/tokenizer.py` | `tests/test_tokenizer.py` |
| Transformer 的小层与完整模型 | 自建 `cs336_basics/model.py`，也可拆成多文件 | `tests/test_model.py` |
| 数值函数、损失与优化器 | 自建 `cs336_basics/nn_utils.py`、`optimizer.py` | `tests/test_nn_utils.py`、`test_optimizer.py` |
| batch 和保存/恢复 | 自建 `cs336_basics/data.py`、`checkpoint.py` | `tests/test_data.py`、`test_serialization.py` |
| 训练与生成脚本、实验报告 | 自建 `train.py`、`generate.py`；报告放自己的 `experiments/` | 按 PDF 的训练、生成、性能与消融要求完成 |

不要求照这些文件名拆分，但要让 adapters 能调用到你的实现。文件不是都已经替你写好；目前只有 BPE 空白骨架与字节练习。完整要求包括编程、书面分析和实验，按官方 PDF 的各个 Problem 核对。

## 8. 第一小题：怎样写 BPE，而不是只“看懂 BPE”

相关视频：第 1 讲 **Overview, tokenization**。视频提供背景，细节在本目录的官方 PDF 分词部分。前 3 讲是整份 A1 的主要基础，但不代表看完后无需再读 PDF。

### 8.1 先读输入和输出，不急着写循环

打开 `tests/adapters.py`，搜索 `def run_train_bpe`。你能看到：

```python
input_path      # 输入文本文件的位置，不是直接传一段字符串
vocab_size      # 最终词表目标大小，包含基础字节和特殊 token
special_tokens  # 需要特殊处理的字符串列表
```

测试希望拿到两个结果：

```python
vocab: dict[int, bytes]                # token ID → 对应字节
merges: list[tuple[bytes, bytes]]      # 按学习顺序排列的合并规则
```

例如 `vocab[0]` 的值应该是 `bytes` 类型，而不是普通字符串。`merges` 记录“哪两个符号被合并”，不是直接返回编码后的全文。

### 8.2 在自己的文件里写，骨架已准备好

打开 `cs336_basics/bpe.py`。里面有 `train_bpe(...)` 的函数签名、分阶段 TODO 和 `raise NotImplementedError`。

先做最小部分：读取 UTF-8 文件、识别特殊 token 边界、按 PDF 预分词规则处理文本、建立基础字节词表。用小例子打印中间结果，不要一上来运行大数据。

后续再写：统计相邻对 → 选出最高频对 → 合并全部对应的非重叠相邻对 → 更新词表和规则 → 循环，直到达到目标或没有可合并项。**相同频次如何选、特殊 token 怎样隔离、不能跨哪些边界合并，都按 PDF 规范实现**，不能凭直觉省略，否则很可能得到不同结果。

把大问题拆成小函数是你的实现选择，例如预分词函数、统计函数、合并一轮的函数。初学时先让正确性可解释，再考虑增量更新和并行加速。

### 8.3 把自己的实现接到官方测试

仍然打开 `tests/adapters.py`，找到 `run_train_bpe` 的**函数体末尾**。仅把它原来的 `raise NotImplementedError` 替换成：

```python
    from cs336_basics.bpe import train_bpe

    return train_bpe(
        input_path=input_path,
        vocab_size=vocab_size,
        special_tokens=special_tokens,
        **kwargs,
    )
```

注意缩进是函数内的 4 个空格。原函数名、参数和说明保留；不要替换整个 adapters 文件，也不要把其余函数的 `raise` 一起替换。

这段只是“转接线”，没有实现 BPE：

```text
pytest → 官方 test_train_bpe() → adapters.run_train_bpe()
       → 你写的 cs336_basics.bpe.train_bpe()
       → 返回 vocab, merges → 官方测试比较结果
```

接线前报错可能指向 adapters；接线后如果你的实现仍为空，报错会指向 bpe.py。这是执行链路发生变化，**不是已经通过了测试**。

### 8.4 只运行这一条正确性测试

从作业一目录（有全局 uv 的路线）：

```powershell
uv run --frozen pytest tests/test_train_bpe.py::test_train_bpe -q
```

或从项目根目录（一键脚本路线）：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/a1.ps1 pytest tests/test_train_bpe.py::test_train_bpe -q
```

这里 `::test_train_bpe` 是只选这一条测试；先不跑速度测试。测试自带 `tests/fixtures/corpus.en`，**此阶段无需下载完整 TinyStories / OpenWebText**。

常见输出：

| 输出 | 说明 | 接下来 |
|---|---|---|
| `NotImplementedError` | 对应函数还没实现，或 adapter 未接线 | 查看 traceback 最后指出哪个文件、哪一行 |
| `AssertionError` | 程序执行到了结果比较，但结果不符合规范 | 对比 merges 的第一个不同项，检查边界、频数和 tie-break |
| `1 passed` | 这条测试通过 | 再检查特殊 token 测试；通过一条不等于完成作业 |
| `ModuleNotFoundError` | 用错环境、缺依赖或运行位置错误 | 确认用本作业 `.venv`、从正确目录执行 |
| `SyntaxError` / `IndentationError` | Python 语法或缩进有问题 | 按错误行检查，先修语法再讨论算法 |

正确性稳定后再运行整个 BPE 文件：

```powershell
uv run --frozen pytest tests/test_train_bpe.py -q
```

其中速度测试有运行时间要求；设备、后台负载会影响计时。先让结果正确，再分析算法性能；不要通过删除测试或放宽阈值宣称完成。

## 9. 分词器之后，模型部分怎么开始？

第 2 讲配合 PyTorch 基础，从 Linear、Embedding 等小模块开始；第 3 讲配合 PDF 完成 RMSNorm、RoPE、注意力、前馈层、Transformer block 和模型。

同样遵守“自己的实现文件 → 对应 adapter → 单条测试”的方式。例如先研究 `run_linear` 输入输出，自己实现 Linear，再运行：

```powershell
uv run --frozen pytest tests/test_model.py::test_linear -q
```

PyTorch 相关前置知识如果还不熟，先补这些具体操作：`torch.tensor`、张量 shape、`@` 矩阵乘法、广播、`reshape` / `transpose`、`nn.Module`、`nn.Parameter`、反向传播。能看懂公式不等于能处理多维张量，遇到卡点就把 batch 和 hidden 缩小到能手算的规模。

注意官方测试会提供指定权重，adapter 必须按规范加载这些权重；随便初始化一个模型通常不会通过比较。读取对应函数的 docstring 和 PDF，再写接线代码，不能机械复制 BPE 的 adapter。

模型与训练涉及的后续任务和资料对照见 [LEARNING_GUIDE.md](LEARNING_GUIDE.md)。

## 10. 两份辅助资料到底什么时候打开？

开始只保留三个入口：**本指南、官方 PDF、自己当前实现的 Python 文件**。

卡在概念上时，读 [中文第一章 PDF](../../references/weiruihhh/笔记/第一章完整版v1.pdf)。卡在 BPE 代码组织时，再局部参考：

- [weiruihhh：BPE 参考](../../references/weiruihhh/chapter1/hw1/)
- [ShallowU：bpe.py](../../references/shallowu/assignment1/cs336_basics/bpe.py)
- [ShallowU 原说明（含博客与 Colab）](../../references/shallowu/README.md)

先试着写出自己的小例子和流程，再对照一个函数。两份第三方实现未被本项目逐项验证，出现差异时回到官方 PDF 和测试。你可以学习并记录使用了哪些帮助；不要把读懂参考代码等同于自己已经能实现。

## 11. 写完这一小步，怎样保存到 GitHub？

按 `Ctrl+S` 保存所有编辑。在左侧修改 `lectures/01/notes.md`，写三句话即可：今天理解了什么、改了哪个文件、下一步做什么。

终端回到项目根目录：

```powershell
cd ../..
```

如果当前已经在根目录，就不要再执行这行。可以用 `Get-Location` 确认。然后记录实际用时：

```powershell
python study.py record --lecture 1 --minutes 40 --summary "跑通字节练习，读懂 BPE 接口，算法尚未实现" --push --api
```

上面是格式示例，修改为你的真实情况。视频看完才加 `--watched`；完成本讲安排的练习再加 `--practice`。即使代码仍在报 `NotImplementedError`，也可以保存真实的学习进度。

该命令会提交此项目里所有未被忽略的更改，包括你的代码和笔记；`.venv`、`.tools`、常见训练数据和输出目录不会上传。推送失败后本地记录仍在，**运行 `python study.py sync --api` 重试，不要为同一次学习重复 record**。

此处“提交”指保存到自己的 GitHub，不是 Stanford Gradescope 交作业；自学没有必须向课程系统交作业的要求。作业里的书面问题可以写到自己的 Markdown 实验报告。

## 12. 今天只完成这五件事就够了

- [ ] 用 VS Code 打开整个学习仓库，找到自己的实现目录。
- [ ] 按路线 A 或 B 配环境，让 pytest 能收集到 BPE 测试。
- [ ] 运行字节练习，改一句话，保存并重跑。
- [ ] 阅读 `run_train_bpe` 和空白 `bpe.py`，写清输入和输出；愿意的话先接好 adapter。
- [ ] 记录实际做到了哪一步并上传，不伪填“已完成”。

下一次再实现最小 BPE 流程。先把“编辑—运行—看错误”这一圈走通，比一次看完所有视频更有用。
