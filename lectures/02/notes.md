# 第 02 讲：PyTorch 与资源核算

英文标题：PyTorch, resource accounting · 关联：A1 · 版本：Spring 2025

## 看完后要能做到

- [ ] 追踪 batch、sequence、hidden、heads 各个张量维度。
- [ ] 理解 Parameter、autograd 和矩阵乘法。
- [ ] 估算小模型参数、梯度及优化器状态占用。

## 本讲动手任务

用随机小张量验证矩阵乘法和 reshape；实现 Linear、Embedding，接入官方测试。

## 所需资料（已整合）

- [官方材料：lecture_02.py](https://stanford-cs336.github.io/spring2025-lectures/?trace=var/traces/lecture_02.json)

- [官方 2025 课程日程 / 视频入口](https://stanford-cs336.github.io/spring2025/)
- [官方作业 A1（原始框架与 handout）](../../assignments/01-basics/README.md)
- [中文笔记：第一章完整版v1.pdf](../../references/weiruihhh/笔记/第一章完整版v1.pdf)
- [中文参考实现：chapter1](../../references/weiruihhh/chapter1/)
- [ShallowU 参考实现与说明：assignment1](../../references/shallowu/assignment1/README.md)
- [辅助材料总索引（含另一份参考实现）](../../resources/INDEX.md)

中文笔记按知识章节整理，不与视频讲次一一对应；这里给的是相关主题入口。参考实现未经本项目逐项验证，以官方 handout 与测试为准。

## 我的笔记

- 视频链接 / B 站分 P：
- 用自己的话解释核心概念：
- 关键公式及每个张量的 shape：
- 实现文件与测试命令：
- 卡点、错误原因与解决过程：
- 下次只做的一件事：

## 课后记录

下面是命令模板，替换用时和收获再运行。只看完视频用 `--watched`；做完上面的动手任务再加 `--practice`；需要同步 GitHub 再加 `--push`。

```powershell
python study.py record --lecture 2 --minutes 60 --summary "替换为本次收获" --watched
```
