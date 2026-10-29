# 第 08 讲：并行训练（二）

英文标题：Parallelism · 关联：A2 · 版本：Spring 2025

## 看完后要能做到

- [ ] 理解优化器状态与参数分片。
- [ ] 解释通信与计算重叠。
- [ ] 对比不同并行方案的内存和吞吐。

## 本讲动手任务

记录一个并行方案的权衡；有多 GPU 再运行指定实验，没有设备明确标记未运行。

## 所需资料（已整合）

- [官方材料：lecture_08.py](https://stanford-cs336.github.io/spring2025-lectures/?trace=var/traces/lecture_08.json)

- [官方 2025 课程日程 / 视频入口](https://stanford-cs336.github.io/spring2025/)
- [官方作业 A2（原始框架与 handout）](../../assignments/02-systems/README.md)
- [中文笔记：第二章完整版v1.pdf](../../references/weiruihhh/笔记/第二章完整版v1.pdf)
- [中文参考实现：chapter2](../../references/weiruihhh/chapter2/)
- [ShallowU 参考实现与说明：assignment2](../../references/shallowu/assignment2/README.md)
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
python study.py record --lecture 8 --minutes 60 --summary "替换为本次收获" --watched
```
