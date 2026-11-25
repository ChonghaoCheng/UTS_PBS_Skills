# UTS PBS Skills

[English](README.md) | **简体中文**

用于 UTS Cetus 的可复用技能，通过 SSH、rsync 和 PBS 原生命令完成资源估算、代码快照、任务脚本、有限并发的 Job Array、监控、结果回收和失败重跑。

AI CLI 在本地工作站运行，通过 SSH 操作 Cetus，计算任务交给 PBS。根据本工作流使用者提供的规定，Cetus 登录节点和计算节点均禁止运行 AI CLI。

## 在本地安装 CLI

以下命令适用于本地 Ubuntu/Bash，其他操作系统请参考官方说明。

### Codex CLI

本地已有受支持的 Node.js 和 npm 时：

```bash
npm install -g --prefix "$HOME/.local" @openai/codex
export PATH="$HOME/.local/bin:$PATH"
codex --version
codex login
```

浏览器回调不可用时，可用 `codex login --device-auth`。使用完整官方 npm 包或安装器，单独复制 release 可执行文件可能导致 `CLI has no complete local package`。

[官方安装说明](https://learn.chatgpt.com/docs/codex/cli) · [认证说明](https://learn.chatgpt.com/docs/auth)

### Claude Code

```bash
curl -fsSL https://claude.ai/install.sh -o /tmp/claude-code-install.sh
bash /tmp/claude-code-install.sh
export PATH="$HOME/.local/bin:$PATH"
claude --version
claude auth login
```

按需将 PATH 写入本地 shell 配置。可用功能取决于账号订阅或服务提供方。

[官方安装说明](https://code.claude.com/docs/en/setup)

## 自动安装技能

克隆仓库后，在本地运行：

```bash
bash scripts/install.sh --client both
# 或选择单个 CLI
bash scripts/install.sh --client codex
bash scripts/install.sh --client claude
# 安装到已有的研究项目
bash scripts/install.sh --client both --project /path/to/research-repo
# 更新已安装副本，保留备份
bash scripts/install.sh --client both --update
```

脚本安装技能文件，CLI 本体安装和账号登录见上文。请在本地工作站运行，脚本会拒绝常见 Cetus 主机名和 PBS 分配环境。已有技能需显式加 --update，备份保存在同级隐藏目录。多客户端安装遇到文件系统错误时可能只完成其中一个，请根据输出路径检查后重试。

## 安装技能

在本地克隆仓库：

```bash
git clone git@github.com:ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
```

按使用的 CLI 选择安装位置。目标已存在时，先检查或备份再更新。

```bash
# Codex 个人技能
mkdir -p "$HOME/.agents/skills"
cp -R skills/cetus-pbs "$HOME/.agents/skills/"

# Claude Code 个人技能
mkdir -p "$HOME/.claude/skills"
cp -R skills/cetus-pbs "$HOME/.claude/skills/"
```

也可安装到研究仓库的 `.agents/skills/`（Codex）或 `.claude/skills/`（Claude Code）。每个 CLI 选择一种范围，避免多份同名技能。安装后重新打开 CLI 会话。更新时拉取本仓库，并更新安装位置的副本。

[Codex 技能位置](https://learn.chatgpt.com/docs/build-skills) · [Claude Code 技能说明](https://code.claude.com/docs/en/skills)

## 配置 SSH

在本地 `~/.ssh/config` 中填写自己的 UTS 账号和获准使用的登录节点：

```sshconfig
Host cetus
    HostName hpc-login02.hpc.uts.edu.au
    User YOUR_UTS_LOGIN
    IdentityFile ~/.ssh/id_ed25519_cetus
    IdentitiesOnly yes
    ControlMaster auto
    ControlPath ~/.ssh/cetus-%C
    ControlPersist 30m
```

首次登记密钥时选择尚未使用的文件名，并设置私钥口令，只上传公钥：

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_cetus -C "cetus-workstation"
ssh-copy-id -i ~/.ssh/id_ed25519_cetus.pub cetus
ssh-add ~/.ssh/id_ed25519_cetus
ssh -oBatchMode=yes cetus 'hostname; command -v qsub qstat rsync'
```

首次连接按学校说明验证主机指纹，按要求连接 UTS VPN。多台电脑可以分别使用自己的密钥。

[Cetus SSH 指南](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/)

## 使用

从本地实验仓库启动 CLI。Codex 提示词示例：

> 使用 $cetus-pbs。冻结指定代码版本与输入数据，先通过 SSH/PBS 跑一个最小真实实验，监控到结束，收集日志和指标并验证结果。所有 AI CLI 在本地运行。

Claude Code 提示词示例：

> /cetus-pbs 使用指定代码、数据和参数准备最小 PBS 实验，核对资源，保留运行清单，回收结果并分析失败原因。

请提供代码 commit、实验入口、数据路径和版本、参数及资源预算。本仓库提供操作指令和 PBS 脚本示例，需按实际实验修改。实验环境和 submit/status/collect 可执行工具需要自行准备。

[PBS 参考](skills/cetus-pbs/references/pbs.md) 包含可复用任务脚本、提交监控命令、并发受限数组、独立输出和失败处理。[SSH 参考](skills/cetus-pbs/references/ssh.md) 说明认证与多机接入。

每次使用独立 run ID、代码快照和冻结输入。大数据保存在共享存储，高频读取只暂存所需分片到 scratch，长任务保存检查点，失败项单独重跑。技能规则用于指导代理，执行时仍需核对资源和命令。

## 仓库结构

```text
README.md
README.zh-CN.md
skills/cetus-pbs/
  SKILL.md
  references/
    ssh.md
    pbs.md
```
