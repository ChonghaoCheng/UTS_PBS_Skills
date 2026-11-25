# UTS PBS Skills

[English](README.md) · **简体中文**

面向 UTS Cetus 的 Agent Skill，提供 SSH 接入、PBS 提交、任务监控和结果回收的操作规程与模板。支持具备文件访问和终端工具的桌面应用、IDE 助手及终端客户端。

## 一句话安装

将下面这句话发送给正在使用的 AI 助手：

```text
请读取 https://github.com/ChonghaoCheng/UTS_PBS_Skills，为当前客户端自动安装 cetus-pbs，并检查技能及配套文件是否完整。
```

助手根据当前客户端、操作系统和可用工具选择安装方式，默认安装到个人范围，并报告实际路径与调用方式。相同内容重复安装会跳过，更新前会备份已有副本。安装完成后开启新会话即可使用。

## 一句话运行

在本地实验仓库中打开客户端，发送：

```text
使用 cetus-pbs，根据当前仓库的配置在 Cetus 跑一次最小实验，完成后回收日志和指标并报告结果。
```

助手先读取仓库说明、实验配置、启动脚本、已有 PBS 工具和 SSH 配置，再完成代码冻结、资源配置、单次提交、状态监控及结果分析。`run_id`、版本记录、PBS Job ID 和起止时间由助手生成或采集。

只有实验入口、输入数据或 SSH 身份等执行必需的信息无法确定时，才集中询问。资源配置优先复用仓库已有的小规模运行设置，并结合队列限制调整。

需要限定范围时，直接在同一句补充，例如“使用当前已提交代码，只运行一个随机种子，最长 10 分钟”。Codex 可显式使用 `$cetus-pbs`，Claude Code 可使用 `/cetus-pbs`。

## 手动安装

需要直接使用终端或指定安装范围时，展开以下说明。[Windows 原生与 WSL 2 步骤](docs/windows.zh-CN.md)另有说明。

<details>
<summary>安装命令与参数</summary>

技能安装需要 Bash、curl 和 tar。在本地终端执行：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

默认优先识别当前 Codex 或 Claude 会话，否则检测 PATH 中支持的客户端命令。没有命令入口的桌面应用可显式指定适配器：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

也可从源码安装：

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex
```

| 参数 | 行为 |
| --- | --- |
| 无参数或 `--client auto` | 自动选择客户端，默认安装到个人技能目录 |
| `--client NAME` | 指定 `codex`、`claude`、`dsh`、`cursor`、`copilot`、`gemini` 或 `opencode` |
| `--client all` | 为全部七个内置适配器安装技能 |
| `--project PATH` | 安装到已存在的项目目录，可与 `--client` 配合使用 |
| `--skills-dir PATH` | 指定其他宿主的技能目录，单独使用，不与 `--client`、`--project` 混用 |
| `--help` | 输出完整参数说明 |

安装器输出 `SKILL.md` 的实际路径。保留整个技能目录及其 `references/`、`assets/`。技能安装到代理实际执行命令的环境，Windows 原生客户端与 WSL 使用各自的个人目录。

</details>

## 执行约束

- AI 客户端运行在本地工作站。Cetus 登录节点仅用于文件传输、轻量检查和调度操作，计算密集型任务通过 PBS 在计算节点执行。
- 每次实验使用独立的 `run_id`、代码快照、配置和输出目录，记录代码与数据版本、参数、PBS Job ID、时间、退出状态和结果文件。
- 批量独立实验使用带并发上限的 Job Array。最小实验只运行一个有界案例，扩展规模需要明确的实验范围。
- 保存提交回执，按设定间隔轮询并设置监控截止时间。提交结果不明时先核对已有任务；需重跑时仅对失败项创建新运行，并保留原始日志和来源记录。
- 删除任务或覆盖实验结果前必须获得用户确认。禁止循环提交任务，禁止在 Cetus 登录节点或计算节点运行 AI 客户端。

## 文档与模板

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](skills/cetus-pbs/SKILL.md) | 技能入口与执行规约 |
| [SSH 接入](skills/cetus-pbs/references/ssh.md) | 连接配置与认证诊断 |
| [PBS 工作流](skills/cetus-pbs/references/pbs.md) | 代码冻结、提交、任务数组、监控及结果回收 |
| [job.pbs](skills/cetus-pbs/assets/job.pbs) | 可复用的 PBS 作业模板 |
| [客户端兼容性](docs/clients.zh-CN.md) | 宿主适配与技能发现方式 |
| [Windows 指南](docs/windows.zh-CN.md) | Windows 原生与 WSL 2 安装和使用 |
