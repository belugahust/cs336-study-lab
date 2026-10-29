# 一站式课程资料

## 课程版本

本项目按 Spring 2025 组织：[官方日程](https://stanford-cs336.github.io/spring2025/)。上游作业固定到 2025 年内的版本，详细 SHA 和文件哈希见 [sources.lock.json](sources.lock.json)。B 站分 P 可能不同，请按英文讲标题匹配，并在个人笔记填入自己的视频地址。

## 官方作业（A1–A4 快照 + A5 本地下载入口）

| 作业 | 本地入口 | 与课程关系 |
|---|---|---|
| A1 Basics | [README](../assignments/01-basics/README.md)、[分步路线](../assignments/01-basics/LEARNING_GUIDE.md) | 重点是第 1–3 讲，训练细节继续读 PDF |
| A2 Systems | [README](../assignments/02-systems/README.md) | GPU、Triton、并行训练 |
| A3 Scaling | [README](../assignments/03-scaling/README.md) | 第 9、11 讲；历史训练 API 是否可用需另行确认 |
| A4 Data | [README](../assignments/04-data/README.md) | 第 13–14 讲；自己下载所需公开数据 |
| A5 Alignment | [README](../assignments/05-alignment/README.md) | 第 15–17 讲；运行下载脚本后本地查看原 handout |

A1–A4 原始 PDF 就在对应目录；A5 通过固定版本下载脚本准备在本地 upstream/；各作业测试与 fixture 保留。自己的实现写在 assignments/，不要改 references/ 里的上游参考快照。

## 中文辅助资料：weiruihhh

来源：[cs336_note_and_hw](https://github.com/weiruihhh/cs336_note_and_hw)。署名保留，CC BY-NC-SA 4.0；作者提示笔记存在纰漏，不能替代官方要求。

| 主题 | 本地笔记 PDF | 参考代码 |
|---|---|---|
| 基础 / A1 | [第一章](../references/weiruihhh/笔记/第一章完整版v1.pdf) | [chapter1](../references/weiruihhh/chapter1/) |
| 系统 / A2 | [第二章](../references/weiruihhh/笔记/第二章完整版v1.pdf) | [chapter2](../references/weiruihhh/chapter2/) |
| 缩放 / A3 | [第三章](../references/weiruihhh/笔记/第三章.pdf) | [chapter3](../references/weiruihhh/chapter3/) |
| 数据 / A4 | [第四章](../references/weiruihhh/笔记/第四章v1草稿.pdf) | [chapter4](../references/weiruihhh/chapter4/) |
| 对齐 / A5 | [第五章](../references/weiruihhh/笔记/第五章笔记初版.pdf) | [chapter5](../references/weiruihhh/chapter5/) |
| DPO / 选做 | [DPO 笔记](../references/weiruihhh/笔记/第五章补充(DPO)笔记初版.pdf) | [补充代码](../references/weiruihhh/chapter5-supplement/) |

还有 [Markdown 版笔记](../references/weiruihhh/web/content/) 和 [上游 README](../references/weiruihhh/README.md)。第一二章合并版 PDF 也保留在笔记目录；未重复打包 1–6 章合订版，使用各章 PDF 即可，不必来回打开上游项目。

## 中文辅助资料：ShallowU

来源：[cs336-assignment](https://github.com/ShallowU/cs336-assignment)，Apache-2.0。本地保留作业 1、2、5 的参考实现及原说明，避免重复携带上游数据集与测试模型权重。

- [作业一代码入口](../references/shallowu/assignment1/README.md)
- [作业二代码入口](../references/shallowu/assignment2/README.md)
- [作业五代码入口](../references/shallowu/assignment5/README.md)
- [作者原 README（含中文博客与 Colab 链接）](../references/shallowu/README.md)

博客 / Colab 是联网补充入口，未把外站网页全文复制进项目；本地已有代码和 weiruihhh 的中文笔记可离线查阅。参考代码未被本项目认证正确，使用时对照官方接口与测试。

## 如何避免资料越看越乱

平时只打开本讲 `lectures/XX/notes.md`。先看里面的目标和动手任务，需要解释时再点相关 PDF；遇到实现卡点再对照一个参考模块。记录一条收获、一条疑问即可继续，不要求每次都补完所有笔记。
