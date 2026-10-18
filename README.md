# OPD / RLVR：阅读笔记与实验代码

| 内容 | 入口 |
|---|---|
| 11 篇论文的中文解读、原文 PDF 与调研笔记 | [reading-notes](reading-notes/README.md) · [在线阅读](https://tasselszcx.github.io/opd-rlvr-paper-notes/reading-notes/) |
| G-OPD 元教学 MVP 完整源码、配置和测试 | [repositories/gopd-meta-teaching-mvp](repositories/gopd-meta-teaching-mvp/) |
| B300 部署与验收交接 | [HANDOFF_B300.md](repositories/gopd-meta-teaching-mvp/HANDOFF_B300.md) |
| 发给 B300 Codex 的接手指令 | [START_B300_CODEX.txt](repositories/gopd-meta-teaching-mvp/START_B300_CODEX.txt) |

## 在 B300 上接手

```bash
git clone https://github.com/Tasselszcx/opd-rlvr-paper-notes.git
cd opd-rlvr-paper-notes/repositories/gopd-meta-teaching-mvp
```

让执行端先读 `HANDOFF_B300.md`，再按 `START_B300_CODEX.txt` 完成环境适配和真实 8 卡 smoke。完整源码已放在当前目录，无需另传离线仓库包或初始化子模块。

**当前训练代码经过 CPU 验证，B300 环境与 GPU 训练尚未实测。** 本仓库不包含模型权重、正式训练数据或已验证的 B300 环境锁。B300 不使用 `install-hopper`；执行端需复用或建立兼容环境后进行真实验收。

## 目录

```text
reading-notes/                        阅读页面、PDF、调研与生成工具
repositories/
  README.md                          代码目录说明
  gopd-meta-teaching-mvp/             可直接编辑的完整 MVP 源码
    HANDOFF_B300.md                   B300 交接
    START_B300_CODEX.txt              接手指令
    meta_teaching/                   教法选择与多轮实验调度
    mvp_configs/                     smoke、pilot、固定时间配置
    verl/                           G-OPD 所用 verl 及 MVP 修改
    tests_mvp/                      CPU 与接口测试
```

阅读内容整体放在 `reading-notes/`，相对链接和离线资源保留。根目录是在线导航入口，旧论文页面地址通过 `404.html` 跳转到新位置。维护阅读页面时，从仓库根目录执行 `reading-notes/README.md` 中的构建命令。

上游 G-OPD、verl、论文、字体及第三方资源保留各自许可证；代码来源见 [MVP_UPSTREAM.json](repositories/gopd-meta-teaching-mvp/MVP_UPSTREAM.json)。
