# UTS PBS Skills

[English](README.md) · **简体中文**

让 Codex、Claude Code 或 DeepSeek Harness 按可复用的流程使用 UTS Cetus。AI 助手在本地工作，通过 SSH 提交 PBS 任务、监控进度，再回收日志与实验结果。

**AI 客户端在本地电脑运行。仿真、训练及其他研究计算交给 PBS 执行。**

## 安装

在本地 Linux 或 macOS 工作站运行，需要 Bash、curl 和 tar：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

脚本优先识别环境中标明的 Codex 或 Claude 会话，否则检查 PATH 中的 `codex`、`claude` 和 `dsh`，为检测到的客户端安装技能。完成后打印 `SKILL.md` 的实际位置。重复执行时，相同内容直接跳过，有变化则先备份再更新。

使用桌面客户端或通过 `npx` 启动 Harness 时，可以直接指定客户端：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

按需替换为 `--client claude`、`--client dsh` 或 `--client all`。默认安装到个人技能目录，完成后开启一个新会话。

也可以把下面这段直接发给 Codex 或其他助手：

> 阅读 https://github.com/ChonghaoCheng/UTS_PBS_Skills ，把 cetus-pbs 技能安装到当前客户端在本地电脑使用的技能目录。请执行安装脚本、检查安装文件，并告诉我如何调用。

想先查看源码，或只安装到某个项目时：

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex --project /path/to/your/project
```

## 使用

先按 [SSH 指南](skills/cetus-pbs/references/ssh.md) 在本地配置 `cetus` 别名，再用 AI 客户端打开本地实验仓库。

| 客户端 | 调用方式 |
| --- | --- |
| Codex | `使用 $cetus-pbs，准备并运行我的实验。` |
| Claude Code | `/cetus-pbs 准备并运行我的实验。` |
| DeepSeek Harness | 要求它加载 `cetus-pbs` 技能并准备实验。 |

例如：

> 用 commit `<commit>`、入口 `<command>` 和共享数据 `<path/version>` 在 Cetus 跑一个最小实验。冻结代码和配置，申请 1 核、2 GB、10 分钟，通过 PBS 提交，监控到完成，回收日志和指标并检查结果。AI 客户端保持在本地运行。

技能覆盖 SSH 接入、资源估算、任务数组、独立代码快照、结果回收和失败项重跑。仓库提供 [PBS 任务模板](skills/cetus-pbs/assets/job.pbs) 和 [完整原生命令示例](skills/cetus-pbs/references/pbs.md)，使用时按实际实验调整资源和冻结的 `command.sh`。

## 客户端准备与安装位置

已有客户端时，执行上面的技能安装命令即可。如果需要在本地安装客户端：

| 客户端 | 安装或启动 | 登录 |
| --- | --- | --- |
| Codex，需支持的 Node.js/npm | `npm install -g --prefix "$HOME/.local" @openai/codex` | `codex login` |
| Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` | `claude auth login` |
| DeepSeek Harness，需 Node.js | `npx @deepseek-ai/dsh web` | 在本地 Web 界面配置模型服务。 |

安装到 `~/.local/bin` 时，按需执行 `export PATH="$HOME/.local/bin:$PATH"`。Codex 使用完整官方安装包，单独复制可执行文件可能缺少交互启动所需的组件。Harness 打开的是本地 Web 界面。

| 客户端 | 个人技能目录 | 项目技能目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/cetus-pbs/` | `.agents/skills/cetus-pbs/` |
| Claude Code | `~/.claude/skills/cetus-pbs/` | `.claude/skills/cetus-pbs/` |
| DeepSeek Harness | `~/.dsh/skills/cetus-pbs/` | `.dsh/skills/cetus-pbs/` |

个人安装支持 `CLAUDE_CONFIG_DIR` 和 `DSH_HOME`，备份保存在对应 `skills/` 的同级 `skill-backups/` 目录。客户端插件单独配置技能路径时，需按实际路径安装。各客户端分别安装，多客户端安装中途遇到错误时，修复提示的问题后重新运行即可。

[Codex CLI](https://learn.chatgpt.com/docs/codex/cli) · [Codex 技能](https://learn.chatgpt.com/docs/build-skills) · [Claude Code](https://code.claude.com/docs/en/setup) · [Claude 技能](https://code.claude.com/docs/en/skills) · [Harness 启动](https://github.com/deepseek-ai/deepseek-harness#run) · [Harness 技能](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
