# UTS PBS Skills

[English](README.md) · **简体中文**

面向桌面应用、IDE 助手和终端客户端的通用 UTS Cetus Agent Skill。AI 助手在本地工作，通过 SSH 提交 PBS 任务、监控进度，再回收日志与实验结果。

**AI 客户端在本地电脑运行。仿真、训练及其他研究计算交给 PBS 执行。**

[Windows 安装](docs/windows.zh-CN.md) · [客户端兼容性](docs/clients.zh-CN.md) · [实际安装验证](docs/validation.md)

## 安装

在本地 Linux 或 macOS 工作站运行，需要 Bash、curl 和 tar：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

脚本优先识别环境中标明的 Codex 或 Claude 会话，否则检查 PATH 中支持的客户端命令。桌面或 IDE 助手没有命令入口时，可显式选择客户端。完成后打印 `SKILL.md` 的实际位置。重复执行时，相同内容直接跳过，有变化则先备份再更新。

桌面或 IDE 客户端没有 PATH 中的命令入口，或通过 `npx` 启动 Harness 时，可以直接指定客户端：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

支持 `codex`、`claude`、`dsh`、`cursor`、`copilot`、`gemini`、`opencode` 和 `all`。默认安装到个人技能目录，完成后开启一个新会话。

也可以把下面这段直接发给 Codex 或其他助手：

> 阅读 https://github.com/ChonghaoCheng/UTS_PBS_Skills ，把 cetus-pbs 技能安装到当前客户端在本地电脑使用的技能目录。请执行安装脚本、检查安装文件，并告诉我如何调用。

想先查看源码，或只安装到某个项目时：

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex --project /path/to/your/project
```

其他 Agent Skills 客户端可以指定其官方技能目录：

```bash
bash scripts/install.sh --skills-dir /path/to/client/skills
```

## 选择客户端

| 客户端 | 安装选项 | 使用界面 |
| --- | --- | --- |
| Codex | `--client codex` | 桌面应用、IDE、终端 |
| Claude Code | `--client claude` | 桌面 Code 界面、IDE、终端 |
| DeepSeek Harness | `--client dsh` | 本地 Web 界面 |
| Cursor | `--client cursor` | IDE 代理 |
| GitHub Copilot | `--client copilot` | 支持技能的 IDE 与代理界面 |
| Gemini CLI | `--client gemini` | 终端 |
| OpenCode | `--client opencode` | 支持的代理界面 |
| 其他 Agent Skills 宿主 | `--skills-dir PATH` | 使用宿主官方说明中的技能目录 |

所有适配器使用同一份 `SKILL.md`、参考文档和 PBS 模板。代理需要读取本地文件并调用 SSH、文件传输工具。技能安装到代理实际运行的环境，包括 WSL 或远程 IDE 的工作环境。本地安装不会自动同步到其他电脑或云端工作进程。

详见[客户端兼容性](docs/clients.zh-CN.md)及 [Windows 原生 / WSL 2 指南](docs/windows.zh-CN.md)。已有桌面或 IDE 客户端时，可以直接使用技能。

## 使用

先按 [SSH 指南](skills/cetus-pbs/references/ssh.md) 在本地配置 `cetus` 别名，再用 AI 客户端打开本地实验仓库。

在新会话中要求助手加载 `cetus-pbs`。Codex 也支持 `$cetus-pbs`，Claude Code 支持 `/cetus-pbs`。然后给出实验信息，例如：

> 用 commit `<commit>`、入口 `<command>` 和共享数据 `<path/version>` 在 Cetus 跑一个最小实验。冻结代码和配置，申请 1 核、2 GB、10 分钟，通过 PBS 提交，监控到完成，回收日志和指标并检查结果。AI 客户端保持在本地运行。

技能覆盖 SSH 接入、资源估算、任务数组、独立代码快照、结果回收和失败项重跑。仓库提供 [PBS 任务模板](skills/cetus-pbs/assets/job.pbs) 和 [完整原生命令示例](skills/cetus-pbs/references/pbs.md)，使用时按实际实验调整资源和冻结的 `command.sh`。

## 验证情况

已在隔离的 Linux 个人目录中实际安装 Codex CLI、Claude Code 和 DeepSeek Harness，验证自动检测、重复安装和技能正文加载。20 项本地回归测试覆盖安装器和 PBS 模板，PBS 部分使用本地模拟调度器。

其他客户端路径已核对官方文档，其实际加载行为及 macOS、Windows 流程仍需在对应系统验证。版本、证据和验证范围见[测试记录](docs/validation.md)。
