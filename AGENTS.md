# Working with UTS_PBS_Skills

## Install this skill

A one-sentence installation request is sufficient to start. Infer the current host, operating system and execution environment from the session and available tools. Read the installer before running it. For a URL-only request, fetch the repository or standalone installer over HTTPS.

Install in the user's submission environment, outside Cetus. Choose `--client codex|claude|dsh|cursor|copilot|gemini|opencode` for the actual host. For another host, consult its documented discovery path and use `--skills-dir PATH`. Desktop applications need not have a terminal executable. Use personal scope unless the user requests a project scope; `--project` requires an existing directory. On Windows, read `docs/windows.md` and distinguish Windows and WSL homes.

Resolve routine choices without asking the user to select flags, clone the repository or supply a discoverable destination. Ask only for missing information that affects the installation. Do not install another AI application or change SSH credentials as a side effect. Identical installs are skipped and changed copies are backed up automatically.

Read the installed SKILL.md and check its references/assets. Report the actual location and host invocation. A new session may be needed for discovery. Installing the skill does not require another AI process or a PBS submission.

## Use PBS

Load `skills/cetus-pbs/SKILL.md` and follow the user's requested operation: connection setup, submission, status, collection, cancellation or retry. Inspect the current task files and existing tools. Infer applicable commands, paths and settings from that evidence, and generate operational records automatically. A Git repository, dataset, scientific method, metrics file or initial smoke job is not a prerequisite. Ask together only for unresolved execution-critical choices. Do not add jobs, shrink inputs or expand the batch beyond the authorized scope.

## Maintain this repository

Write for any Cetus user. Keep personal accounts, project names, private paths, research methods and historical machine settings out of default workflows. Any runnable demonstration must be labelled as an example with its assumptions. Git, node-local scratch, input datasets, checkpoints and metrics are conditional on the workload. Obtain queue limits and resource requirements from current task/site configuration rather than fixed historical values.

Keep English and Chinese README/client/Windows guides consistent. Preserve the one-sentence installation/use entries before advanced instructions. Use HTTPS GitHub URLs. Keep the skill independent of host-specific tool names and invocation syntax; adapters belong in the installer and client guide. Describe bundled template conventions separately from PBS requirements or UTS policy. Keep project research records out of this repository.

Preserve isolated runs, submission receipts and existing results. Do not contact Cetus or submit real jobs to validate documentation or installation changes. Use temporary local directories for tests. Run `python3 -m unittest discover -s tests -v` after installer or job-template changes, check Bash syntax and validate the skill format. State when checks simulate PBS rather than exercise a scheduler.
