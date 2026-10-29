# 第 15 讲：对齐：SFT / RLHF

英文标题：Alignment - SFT/RLHF · 关联：A5 · 版本：Spring 2025

## 看完后要能做到

- [ ] 区分预训练和监督微调。
- [ ] 理解偏好数据与奖励模型的角色。
- [ ] 理解对齐收益与局限。

## 本讲动手任务

阅读 A5 handout，梳理 SFT 数据和 loss mask；实际训练前确认模型、显存和依赖。

## 所需资料（已整合）

- [官方 2025 课程日程 / 视频入口](https://stanford-cs336.github.io/spring2025/)
- [官方材料：lecture 15.pdf](https://github.com/stanford-cs336/spring2025-lectures/blob/61eddac004df975466cff0329b615f2d24230069/nonexecutable/2025%20Lecture%2015%20-%20RLHF%20Alignment.pdf)
- [官方作业 A5（原始框架与 handout）](../../assignments/05-alignment/README.md)
- [中文笔记：第五章笔记初版.pdf](../../references/weiruihhh/笔记/第五章笔记初版.pdf)
- [中文参考实现：chapter5](../../references/weiruihhh/chapter5/)
- [ShallowU 参考实现与说明：assignment5](../../references/shallowu/assignment5/README.md)
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
python study.py record --lecture 15 --minutes 60 --summary "替换为本次收获" --watched
```
