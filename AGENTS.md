# Working with UTS_PBS_Skills

## When the user asks to install this skill

Run the installation on the user's local workstation, in the environment where their agent actually runs. This repository distributes a portable Agent Skill for desktop, IDE and terminal clients. Select the current host explicitly with `--client codex|claude|dsh|cursor|copilot|gemini|opencode`. For other hosts, consult their documented skill discovery path and use `--skills-dir PATH`. Do not assume a desktop application has a terminal executable. Install to personal scope unless the user requests a project scope. `--project` requires an existing project directory.

A one-sentence installation request is sufficient to perform the installation. Infer the host, operating system and execution environment from the current session and available tools. Read the client and Windows guides when relevant. Choose the matching adapter and personal scope without asking the user to select flags, copy commands, clone the repository or supply a destination that can be determined locally. Ask only when the host cannot be identified or a required action genuinely needs user input. Do not install extra AI applications or change SSH credentials as a side effect of skill installation.

From a URL-only request, fetch this repository over HTTPS and read the installer before running it. The script also works as a standalone download and fetches its own skill payload. Installation replaces changed copies after backing them up and leaves identical copies alone. Do not install or launch AI clients on Cetus.

Read the resulting SKILL.md to verify it and its references/assets exist. Report its actual path and the invocation for the chosen client. A restart may be needed for discovery. Installing this skill does not require starting another AI process, submitting a PBS job, or changing SSH credentials. On Windows, read `docs/windows.md` and distinguish the Windows and WSL homes. Follow the user's chosen client rather than installing a different client for convenience.

## When the user asks to run an experiment

Load `skills/cetus-pbs/SKILL.md` and begin discovery in the current repository. Read its instructions, experiment configs, launch scripts and existing PBS tooling, and inspect the existing SSH setup. Derive the commit, entry point, parameters and data identifiers from that evidence. Generate run IDs, hashes, timestamps and submission records automatically. For a minimal-run request, use one bounded representative case and report the selected configuration; do not expand into a sweep. Ask together only for unresolved execution-critical choices, such as an ambiguous experiment or an unavailable dataset/account. Never invent credentials, dataset paths or scientific settings to avoid a necessary question.

## When editing this repository

Write for any Cetus user. Describe PBS capabilities in terms of jobs, task inputs, resources and outputs. Keep specific research methods and datasets out of default workflows; label optional examples clearly.

Keep README.md and README.zh-CN.md consistent, including linked client and Windows guides. Use HTTPS GitHub URLs. Keep scientific project documentation outside this repository. Keep the skill body independent of client-specific tools and invocation syntax; put discovery adapters in the installer and client guide. The skill describes PBS operation, and runnable examples must preserve run isolation and avoid duplicate submission. Separate real client loading evidence from directory tests and documentation-only compatibility claims.

Run `python3 -m unittest discover -s tests -v` after changing installation or job-template behavior. Test with temporary project directories, without installing into the developer's real client directory or contacting Cetus. State clearly when tests simulate PBS rather than run on the cluster.
