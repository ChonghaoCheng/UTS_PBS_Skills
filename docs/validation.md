# Installation and loading validation

[README](../README.md) · [中文 README](../README.zh-CN.md) · [Client compatibility](clients.md)

Validated on 2026-11-25. 已完成隔离 Linux 环境中的真实安装及加载检查。Windows、macOS 和新增客户端的实际加载仍待对应环境验证。

## Environment and source

The test used Bubblewrap with a fresh writable home mounted over the normal home, a separate workspace, cleared environment variables and a temporary `/tmp`. The original home, client settings and account credentials were not used. System binaries came from the existing Ubuntu workstation; this was a clean user environment, not a fresh OS or virtual machine. All AI processes ran locally. No Cetus connection or PBS submission was made.

The initial bootstrap downloaded both READMEs and the standalone installer from GitHub at revision `54fbf98f02c773f23fe531ce1ba7726c800b8149`. The subsequent adapter and portability changes were rechecked with this installer and payload:

```text
scripts/install.sh
SHA256 4daef29d1fe24d165c353b070078dcbca60959d54826e75dd9460a0fe3a46cd5
skills/cetus-pbs/SKILL.md
SHA256 f2cc7074c5ae2c9efa2997886859e9676fe8d0e612410e844b940e5205f3e634
```

| Component | Tested version / installation |
| --- | --- |
| Codex CLI | 0.172.0, official `@openai/codex` npm package |
| Claude Code | 2.1.332, official native Linux installer |
| DeepSeek Harness | 0.2.2-rc.5, official `@deepseek-ai/dsh` npm package and `npx` Web launch |
| Node.js for Harness | 24.22.3, official archive checked against its published SHA256 |

The original system Node 22 was below Harness's declared `>=24.9.0` requirement. The setup guide now records that requirement for the tested Harness release.

## Observed results

| Check | Result |
| --- | --- |
| Run with no clients or session markers | Exit 1 with explicit selection guidance; no skill installed |
| Default installer with real Codex on PATH | Selected Codex and installed the complete folder |
| Default installer after adding real Claude | Selected Codex and Claude |
| Default installer after adding real Harness | Selected all three |
| Repeat each installation | Reported `Already up to date` for the selected clients |
| Update to the revised skill | Backed up each previous copy and installed the new payload |
| Repeat revised installation | Skipped all three unchanged copies |
| Actual Codex skill loading | `$cetus-pbs` expanded the complete installed body into a request; exit 0 |
| Actual Claude Code skill loading | `/cetus-pbs` expanded the complete installed body into a request; exit 0 |
| Actual Harness discovery and reading | Its shipped filesystem provider selected `user-dsh` and returned the complete body |
| Harness launch | `npx @deepseek-ai/dsh web --no-open --port 0` started its local Web server |

Codex and Claude were pointed at temporary loopback HTTP endpoints implementing their respective response protocols. The endpoint returned a fixed acknowledgement. Captured request text was checked for the **entire installed Markdown body**, with YAML frontmatter removed, and the `assets/job.pbs` reference. This exercised the actual client loading code without provider accounts, external inference or model charges. Claude also advertised `cetus-pbs` in its session skill catalogue.

Harness was tested using `FileSystemSkillProvider.list()` and `.get()` from the actual installed `@deepseek-ai/dsh-skill-filesystem` dependency. Its returned content was checked against the complete installed body. The Web server launch was checked separately. This does not establish browser interaction or a model-driven Harness skill-tool invocation.

Sanitized loading results:

```json
{
  "codex": {"exit": 0, "requests": 1, "full_skill_body": true, "asset_reference": true},
  "claude": {"exit": 0, "requests": 1, "full_skill_body": true, "asset_reference": true},
  "harness": {"source": "user-dsh", "full_skill_body": true, "asset_reference": true}
}
```

## Repository regression checks

```bash
python3 -m unittest discover -s tests -v
bash -n scripts/install.sh skills/cetus-pbs/assets/job.pbs
```

All 20 tests passed. Installer coverage includes the seven client adapters, session selection, explicit override, custom directories, changed-copy backups, no-op repeats, failed-update restoration, locking, incomplete downloads and Cetus/PBS guards. These adapter tests use temporary directories and synthetic command discovery; only the three clients above received real loading checks.

The PBS template tests use a local simulated allocation. They check success, application failure, independent array/attempt outputs, checksum rejection, login-node rejection, duplicate submission protection and retained scratch on transfer failure. They do not verify a real scheduler or cluster resources.

## Remaining verification

- Cursor, Copilot, Gemini and OpenCode discovery paths were checked against the official sources linked in the [client guide](clients.md). Their actual runtime loading was not tested.
- Native Windows, WSL 2, macOS, desktop UIs and IDE integrations were not run. The [Windows guide](windows.md) describes the documented setup and keeps Windows and WSL installation locations distinct.
- External model authentication and end-to-end model execution were not tested. A local protocol acknowledgement proves loading, not the model's ability to follow the PBS workflow.
- This installation check did not run a cluster experiment. Validate SSH and submit a minimal real PBS workload when using the skill with your own Cetus account.
