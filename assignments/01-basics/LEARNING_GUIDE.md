# 作业一：从视频到自己的代码

**第一次做？先读 [作业一新手指南](BEGINNER_START_HERE.md)**。它详细说明软件、目录、环境配置、代码骨架、adapter 接线，以及第一条测试怎么运行。

课程版本：2025。先读本目录中的官方 PDF；以下只是学习顺序建议，不替代完整要求。

## 最小开始方式

1. 打开 `tests/adapters.py` 看需要接入的函数签名与 docstring。
2. 在 `cs336_basics/` 新建自己的实现模块。
3. 在 adapter 对应函数中导入并调用你的实现；不要改官方测试来迁就错误实现。
4. 每完成一个小模块，只跑有关测试。最初其他测试失败正常。

## 分步路线

| 步骤 | 视频 / 补充 | 自己实现的内容 | 在当前目录运行的测试 |
|---|---|---|---|
| 1 | 第 1 讲 + PDF 分词部分 | 字节级 BPE 训练、合并规则 | `uv run pytest tests/test_train_bpe.py -q` |
| 2 | 第 1 讲 + tokenizer 规范 | encode / decode / iterable / 特殊 token | `uv run pytest tests/test_tokenizer.py -q` |
| 3 | 第 2 讲 + PDF 架构部分 | Linear、Embedding、RMSNorm 等小层 | `uv run pytest tests/test_model.py -q`（可用 -k 选择已实现测试） |
| 4 | 第 3 讲 + PDF 公式 | RoPE、注意力、SwiGLU、block、LM | `uv run pytest tests/test_model.py -q` |
| 5 | PDF 优化训练部分，按需补 PyTorch 基础 | softmax、cross entropy、AdamW、调度、梯度裁剪 | `uv run pytest tests/test_nn_utils.py tests/test_optimizer.py -q` |
| 6 | PDF 数据与训练部分 | batch、保存恢复、训练循环 | `uv run pytest tests/test_data.py tests/test_serialization.py -q` |
| 7 | PDF 实验与生成要求 | TinyStories 训练、解码与消融实验 | `uv run pytest -q` 后按 PDF 运行实验；测试通过并不等于完成实验 |

先用 `uv run pytest tests/test_model.py --collect-only -q` 查看真实测试名称，再选择 `-k`，不要猜测试函数名。训练脚本需要你自己写；框架不是填完 adapters 就会自动训练。

## 资料对照（都在本仓库）

| 任务 | 中文说明 / 参考一 | 参考二 |
|---|---|---|
| 全部基础 | [第一章 PDF](../../references/weiruihhh/笔记/第一章完整版v1.pdf) | [原 README：博客 / Colab](../../references/shallowu/README.md) |
| BPE | [hw1](../../references/weiruihhh/chapter1/hw1/) | [bpe.py](../../references/shallowu/assignment1/cs336_basics/bpe.py) |
| tokenizer | [hw2](../../references/weiruihhh/chapter1/hw2/) | [tokenizer.py](../../references/shallowu/assignment1/cs336_basics/tokenizer.py) |
| Transformer 层 | [hw3](../../references/weiruihhh/chapter1/hw3/) | [layer.py](../../references/shallowu/assignment1/cs336_basics/layer.py) |
| 优化与损失 | [hw4](../../references/weiruihhh/chapter1/hw4/) | [optimizer.py](../../references/shallowu/assignment1/cs336_basics/optimizer.py)、[loss.py](../../references/shallowu/assignment1/cs336_basics/loss.py) |
| 数据 / 检查点 | [hw5](../../references/weiruihhh/chapter1/hw5/) | [data.py](../../references/shallowu/assignment1/cs336_basics/data.py)、[util.py](../../references/shallowu/assignment1/cs336_basics/util.py) |
| 训练 / 生成 | [hw6–7](../../references/weiruihhh/chapter1/hw7/) | [train/](../../references/shallowu/assignment1/train/) |

## 自检里程碑

- [ ] 在纸上解释 BPE 合并，而不是只看懂代码。
- [ ] tokenizer 能对中文、英文及特殊 token 做往返测试。
- [ ] 能写清楚注意力每一步的 shape 与 causal mask。
- [ ] 小规模前向 / 反向工作正常。
- [ ] 官方正确性测试通过，未修改测试绕过问题。
- [ ] 完成 handout 指定的训练与实验，保留真实配置和结果。
- [ ] 能从 checkpoint 恢复并生成文本。

暂时没有 GPU，也可以先做前几项。正式训练的设备要求以 handout 和实际模型大小为准。
