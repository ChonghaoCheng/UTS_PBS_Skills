# 客户端兼容性

[English](clients.md) · [返回 README](../README.zh-CN.md)

技能采用 [Agent Skills 格式](https://agentskills.io/specification)。桌面代理、IDE 助手、终端代理，以及其他能读取技能文件、在本地执行 SSH 和文件传输命令的兼容宿主都可以接入。技能应安装到代理实际运行的环境。纯网页聊天和远端工作进程需要各自支持的文件、工具接入方式。

| 客户端或使用界面 | 安装选项 | 个人目录 | 项目目录 |
| --- | --- | --- | --- |
| Codex 桌面端、IDE、CLI | `--client codex` | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code 终端、IDE、桌面 Code 界面 | `--client claude` | `~/.claude/skills/` | `.claude/skills/` |
| DeepSeek Harness | `--client dsh` | `~/.dsh/skills/` | `.dsh/skills/` |
| Cursor | `--client cursor` | `~/.cursor/skills/` | `.cursor/skills/` |
| GitHub Copilot 支持代理的界面 | `--client copilot` | `~/.copilot/skills/` | `.github/skills/` |
| Gemini CLI | `--client gemini` | `~/.gemini/skills/` | `.gemini/skills/` |
| OpenCode | `--client opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` |

安装器会在这些目录下创建 `cetus-pbs/`。个人安装支持 `CLAUDE_CONFIG_DIR`、`DSH_HOME` 和 `XDG_CONFIG_HOME`。部分客户端还会读取 `.agents/skills/`，同一客户端会扫描的不同目录应避免安装不同版本。

自动检测优先使用 Codex/Claude 当前会话标记，再检查 PATH 中的程序名称。桌面应用可能没有命令入口，此时直接指定客户端即可。`--client all` 为表中的全部适配器安装文件，也支持在安装应用前准备技能。

其他客户端先查明其官方技能目录，然后直接指定：

```bash
bash scripts/install.sh --skills-dir /path/to/client/skills
```

这会创建 `/path/to/client/skills/cetus-pbs/`。`--skills-dir` 单独使用，不与 `--client`、`--project` 混用，可接入自定义技能目录和后续新增的 Agent Skills 客户端。安装后重开代理会话，查看技能列表并要求加载 `cetus-pbs`，确认能够读取 SSH/PBS 参考文件并解析 `assets/job.pbs`，再安排真实任务。客户端版本、工作区信任和管理员设置可能影响发现过程。

手动安装时，把仓库的整个 `skills/cetus-pbs/` 复制到宿主技能目录，保留 `references/` 和 `assets/`。客户端支持技能压缩包导入时，按它的官方打包及导入流程操作。仅复制 `SKILL.md` 会缺少 PBS 模板和操作参考。

普通 Claude 聊天、Cowork 和纯云端会话采用不同于本地 Claude Code 的分发方式。本地安装也不会自动传到云端代理或远端 IDE 工作进程。请按宿主支持的导入方式接入，并保证实际执行环境遵守本地运行代理、Cetus 运行计算的边界。

## 官方参考

- [Codex 技能](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code 技能](https://code.claude.com/docs/en/skills)
- [Harness 技能发现](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
- [Cursor 技能](https://prod.cursor.com/docs/skills)
- [Copilot 技能](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Gemini 技能](https://geminicli.com/docs/cli/skills/)
- [OpenCode 技能](https://opencode.ai/docs/skills/)
