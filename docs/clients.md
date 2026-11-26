# Client compatibility

[简体中文](clients.zh-CN.md) · [Back to README](../README.md)

The skill uses the [Agent Skills format](https://agentskills.io/specification). It can be used by a desktop agent, an IDE assistant, a terminal agent, or another compatible host that can read its files and execute SSH/file-transfer commands on the local computer. Install it where the agent actually runs. A browser-only chat or a remote worker needs its own supported file/tool integration.

| Client / surface | Installer option | Personal directory | Project directory |
| --- | --- | --- | --- |
| Codex desktop, IDE or CLI | `--client codex` | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code terminal, IDE or Code desktop surface | `--client claude` | `~/.claude/skills/` | `.claude/skills/` |
| DeepSeek Harness | `--client dsh` | `~/.dsh/skills/` | `.dsh/skills/` |
| Cursor | `--client cursor` | `~/.cursor/skills/` | `.cursor/skills/` |
| GitHub Copilot agent-capable surfaces | `--client copilot` | `~/.copilot/skills/` | `.github/skills/` |
| Gemini CLI | `--client gemini` | `~/.gemini/skills/` | `.gemini/skills/` |
| Google Antigravity IDE, app or CLI | `--client antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` |
| OpenCode | `--client opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` |

The installer appends `cetus-pbs/` to each directory. It honors `CLAUDE_CONFIG_DIR`, `DSH_HOME` and `XDG_CONFIG_HOME` for personal installs. Note that `--client gemini` targets Gemini CLI (`~/.gemini/skills/`), whereas `--client antigravity` targets Google Antigravity (`~/.gemini/config/skills/` globally, `.agents/skills/` in a workspace). Several clients also read `.agents/skills/`; avoid installing different versions under multiple roots that the same client scans.

The default installer uses an active Codex/Claude session marker when present, then executable names on PATH (`agy` for Antigravity). A desktop app can be installed without a command on PATH. Select it explicitly in that case. `--client all` installs files for every adapter in the table, without requiring the applications to be installed first.

For any other client, find its documented skill directory and pass that directory directly:

```bash
bash scripts/install.sh --skills-dir /path/to/client/skills
```

This creates `/path/to/client/skills/cetus-pbs/`. Use `--skills-dir` by itself, without `--client` or `--project`. It supports hosts with custom skill roots and future Agent Skills clients. Reopen the agent session, list its available skills, and ask it to load `cetus-pbs`. Confirm that it reads the SSH/PBS references and resolves `assets/job.pbs` before giving it a real job. Client versions, workspace trust and administrator settings can affect discovery.

For manual installation, copy the entire `skills/cetus-pbs/` folder from this repository into the host's skill root, retaining `references/` and `assets/`. If the host supports uploading a skill archive, follow its documented packaging/import procedure. Copying only `SKILL.md` omits the runnable PBS template and operational references.

Ordinary Claude chat/Cowork and cloud-only sessions have different upload/distribution mechanisms from local Claude Code. Likewise, local installation does not automatically install a skill in a cloud agent or remote IDE worker. Follow the host's supported import procedure and ensure its execution environment complies with the local-agent/Cetus-computation boundary.

## Official client references

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Harness skill discovery](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
- [Cursor skills](https://prod.cursor.com/docs/skills)
- [Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [Antigravity skills](https://antigravity.google/docs/skills)
- [OpenCode skills](https://opencode.ai/docs/skills/)
