# Working with UTS_PBS_Skills

## When the user asks to install this skill

Run the installation on the user's local workstation. Use `bash scripts/install.sh --client codex` when acting as Codex, `--client claude` for Claude Code, or `--client dsh` for DeepSeek Harness. Install to personal scope unless the user requests a project scope. `--project` requires an existing project directory.

From a URL-only request, fetch this repository over HTTPS and read the installer before running it. The script also works as a standalone download and fetches its own skill payload. Installation replaces changed copies after backing them up and leaves identical copies alone. Do not install or launch AI clients on Cetus.

Read the resulting SKILL.md to verify it and its references/assets exist. Report its actual path and the invocation for the chosen client. A restart may be needed for discovery. Installing this skill does not require starting another AI process, submitting a PBS job, or changing SSH credentials.

## When editing this repository

Keep README.md and README.zh-CN.md consistent. Use HTTPS GitHub URLs. Keep scientific project documentation outside this repository. The skill describes PBS operation, and runnable examples must preserve run isolation and avoid duplicate submission.

Run `python3 -m unittest discover -s tests -v` after changing installation or job-template behavior. Test with temporary project directories, without installing into the developer's real client directory or contacting Cetus. State clearly when tests simulate PBS rather than run on the cluster.
