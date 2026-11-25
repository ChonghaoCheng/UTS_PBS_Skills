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
| OpenCode | `--client opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` |

The installer appends `cetus-pbs/` to each directory. It honors `CLAUDE_CONFIG_DIR`, `DSH_HOME` and `XDG_CONFIG_HOME` for personal installs. Several clients also read `.agents/skills/`; avoid installing different versions under multiple roots that the same client scans.

The default installer uses an active Codex/Claude session marker when present, then executable names on PATH. A desktop app can be installed without a command on PATH. Select it explicitly in that case. `--client all` installs files for every adapter in the table, without requiring the applications to be installed first.

For any other client, find its documented skill directory and pass that directory directly:

```bash
bash scripts/install.sh --skills-dir /path/to/client/skills
```

This creates `/path/to/client/skills/cetus-pbs/`. Use `--skills-dir` by itself, without `--client` or `--project`. It supports hosts with custom skill roots and future Agent Skills clients. Reopen the agent session, list its available skills, and ask it to load `cetus-pbs`. Confirm that it reads the SSH/PBS references and resolves `assets/job.pbs` before giving it a real job. Client versions, workspace trust and administrator settings can affect discovery.

For manual installation, copy the entire `skills/cetus-pbs/` folder from this repository into the host's skill root, retaining `references/` and `assets/`. If the host supports uploading a skill archive, follow its documented packaging/import procedure. Copying only `SKILL.md` omits the runnable PBS template and operational references.

Ordinary Claude chat/Cowork and cloud-only sessions have different upload/distribution mechanisms from local Claude Code. Likewise, local installation does not automatically install a skill in a cloud agent or remote IDE worker. Follow the host's supported import procedure and ensure its execution environment complies with the local-agent/Cetus-computation boundary.

## Optional client setup

Use an existing desktop app or IDE integration, installed and signed in through its product's official setup. Installing this skill only copies its files; it does not install an AI application, add SSH keys or sign into a provider.

For a terminal client or Harness Web UI on Linux/macOS, the following setup commands are available. Choose the client you want, then run the skill installer. Windows commands are in the [Windows guide](windows.md).

| Client | Install or launch | Sign in |
| --- | --- | --- |
| Codex, with supported Node.js/npm | `npm install -g --prefix "$HOME/.local" @openai/codex` | `codex login` |
| Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` | `claude auth login` |
| DeepSeek Harness | `npx @deepseek-ai/dsh web` | Configure the provider in the local Web UI. |

Harness 0.2.2-rc.5 requires Node.js ≥24.9.0; check the current package's engine requirement before installing. The validation used Node 24.22.3. Add `~/.local/bin` to PATH if needed with `export PATH="$HOME/.local/bin:$PATH"`. Use the complete official Codex package because copying a single executable can omit required components.

Identical skill installs are skipped; changed copies are backed up under `skill-backups/` alongside `skills/`. Each client is updated independently. If a multi-client install stops partway, fix the reported issue and rerun.

## Verification status

Codex CLI 0.172.0, Claude Code 2.1.332 and Harness 0.2.2-rc.5 were installed in an isolated Linux home. Codex and Claude sent the complete installed skill body and asset reference to a local protocol test endpoint. Harness launched its Web UI and its shipped filesystem provider discovered and loaded the complete skill. These checks exercised real client code without external model credentials or inference.

Cursor, Copilot, Gemini and OpenCode mappings follow their official documentation. Their desktop/IDE behavior and native Windows loading have not been exercised in this environment. Routing tests cover the installer destinations; these are separate from real-client loading tests.

[Validation record](validation.md)

## Official client references

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Harness skill discovery](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
- [Cursor skills](https://prod.cursor.com/docs/skills)
- [Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Gemini skills](https://geminicli.com/docs/cli/skills/)
- [OpenCode skills](https://opencode.ai/docs/skills/)
