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

在保存任务文件的目录中打开客户端，发送：

```text
使用 cetus-pbs，根据当前目录已有的任务配置向 Cetus 提交 PBS 作业，完成后回收日志和输出并报告状态。
```

助手先读取任务说明、启动脚本、配置、已有 PBS 工具和 SSH 设置，再准备独立的任务文件、配置资源、提交并监控作业。`run_id`、文件快照或适用的 Git 版本、PBS Job ID 和时间记录由助手生成或采集。任务可以来自普通目录，无需 Git 仓库、数据集或指标文件。

只有启动命令、必需输入、SSH 身份或资源需求等执行必需的信息无法确定时，才集中询问。账号、连接别名、工作路径、软件环境、队列和资源申请均从当前任务与环境确定。首次测试或最小任务只在用户要求或同意时执行。

可在同一句补充任务范围、输出要求或“先检查配置，暂不提交”。Codex 可显式使用 `$cetus-pbs`，Claude Code 与 Antigravity 可使用 `/cetus-pbs`。

## 技能内容

技能包包含 `SKILL.md` 操作规约、SSH/PBS 参考文档和 `job.pbs` 作业模板。助手结合当前任务配置，通过 SSH、rsync（本地缺少 `rsync` 时支持 `tar`-over-`ssh`）和 PBS 原生命令执行以下流程：

| 功能 | 内容 |
| --- | --- |
| SSH 接入 | 复用连接配置，拆分首次密钥生成与用户终端交互授权，检查校园网/UTS VPN 前提，诊断权限与连接复用问题 |
| 任务准备 | 读取启动命令与配置，按请求范围准备独立的文件快照、启动脚本和 `run_id`，使用 Git 时记录适用版本 |
| 资源配置 | 根据已有设置、实测开销和 `qstat -Qf` 限制配置队列、CPU、内存、GPU 与运行时长，显式初始化非交互运行时并对齐线程数 |
| 提交与监控 | 保存 PBS Job ID 和提交回执，防止重复提交，按设定间隔及截止时间查询任务与数组子任务状态 |
| 批量任务 | 将多组独立任务组织为带并发上限的 Job Array，按任务索引分别记录配置、日志和结果 |
| 文件与存储 | 确定任务输入、输出和可写目录，记录校验值，高 I/O 负载核实并使用节点本地暂存盘（如 `/scratch`），保留需持久保存的文件 |
| 输出回收 | 通过 `rsync` 或 `tar`-over-`ssh` 收集日志和输出，核对调度器及程序退出状态；指标检查和专业分析按任务需要执行 |
| 失败恢复 | 区分程序、环境、数据暂存和传输故障，单独重跑已定位的失败项，保留原始结果及父运行记录 |

配套模板通过 `qsub` 参数接收任务资源申请，不预设队列、CPU、内存或运行时长。应用线程数、非交互环境加载和工作目录均按任务与执行环境配置；参考文档中的数值和目录名均为演示示例。

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
| `--client NAME` | 指定 `codex`、`claude`、`dsh`、`cursor`、`copilot`、`gemini`、`antigravity` 或 `opencode` |
| `--client all` | 为全部八个内置适配器安装技能 |
| `--project PATH` | 安装到已存在的项目目录，可与 `--client` 配合使用 |
| `--skills-dir PATH` | 指定其他宿主的技能目录，单独使用，不与 `--client`、`--project` 混用 |
| `--help` | 输出完整参数说明 |

安装器输出 `SKILL.md` 的实际路径。保留整个技能目录及其 `references/`、`assets/`。技能安装到代理实际执行命令的环境，Windows 原生客户端与 WSL 使用各自的个人目录。

</details>

## 执行约束

- AI 客户端运行在 Cetus 之外的提交环境。Cetus 登录节点仅用于文件传输、轻量检查和调度操作，计算密集型任务通过 PBS 在计算节点执行。
- 新提交的任务使用独立的 `run_id`、文件快照、配置和输出目录，记录命令、资源申请、适用的版本或校验值、PBS Job ID、时间和退出状态。
- 批量独立任务使用带并发上限的 Job Array，数组范围、任务映射和并发数按实际请求确定。查询、回收和取消已有作业按请求操作。
- 保存提交回执，按设定间隔轮询并设置监控截止时间。提交结果不明时先核对已有任务；需重跑时仅对失败项创建新运行，并保留原始日志和来源记录。
- 取消作业或覆盖输出需要用户授权，明确指定取消对象的请求即可提供该授权。禁止循环提交任务或擅自改变任务规模；本工作流的 AI 客户端保留在 Cetus 之外的提交环境。

## 文档与模板

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](skills/cetus-pbs/SKILL.md) | 技能入口与执行规约 |
| [SSH 接入](skills/cetus-pbs/references/ssh.md) | 连接前提、密钥注册与认证诊断 |
| [PBS 操作](skills/cetus-pbs/references/pbs.md) | 文件快照、队列/GPU、节点暂存、提交、数组、监控与回收 |
| [job.pbs](skills/cetus-pbs/assets/job.pbs) | 可复用的 PBS 作业模板 |
| [客户端兼容性](docs/clients.zh-CN.md) | 宿主适配与技能发现方式 |
| [Windows 指南](docs/windows.zh-CN.md) | Windows 原生与 WSL 2 安装和使用 |
