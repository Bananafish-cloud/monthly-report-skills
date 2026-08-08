# monthly-report-skills

通用月报 Skill 生成器 + 各项目月报 Skill 的共享仓库（公开）。

## 这是什么

**`monthly-report-skill-builder/`** — 引导式月报工作流生成器。让同事用自己的 agent（WorkBuddy / Claude Code / Codex）自主分析、定制某个项目的月报流程，产出一个独立的项目专属月报 Skill，落到自己的 skills 目录自用。

工作模式：把一条启动命令交给 agent → agent 自主解析模板、按项目实际判断翻车点、需要你决策时再交互 → 产出 `SKILL.md + scripts` → 每月由你的 agent 照着跑。

## 安装（推荐：让 agent 自己装，一句话搞定）

对 agent 说：

> 帮我从公开仓库 `https://github.com/Bananafish-cloud/monthly-report-skills` 安装 `monthly-report-skill-builder` 这个 skill 到我的 skills 目录。

clone 还是 ZIP、装到哪个目录，agent 自己会判断（实测 WorkBuddy 可自主 clone + 安全审查 + 安装，无需登录）。

**装完 ⚠️ 必须【新开一个对话/会话】**，agent 才会重新加载并识别到它。然后对它说：
> 用 monthly-report-skill-builder 帮我生成 XX 项目月报的 Skill

（如果不想用 agent 自动装，也可以手动：浏览器下载 ZIP 解压 → 右键 `install.ps1` 用 PowerShell 运行；或 `git clone https://github.com/Bananafish-cloud/monthly-report-skills` 后复制 `monthly-report-skill-builder` 文件夹到你的 skills 目录。）

## 安全说明

skill 内所有脚本仅做**本地 PowerPoint COM 操作**（环境检测、shape 诊断），无网络调用、无破坏性行为，可顺利通过 agent 的安全审查（实测 WorkBuddy P2 安全审查通过）。

## 版本记录

- **v3.2**（2026-08-08）：**回到引导式，把判断力还给 agent**——生成器不产出固定问卷模板，而是给 agent 一条启动命令 + 一套引导协议：agent 自主解析模板、按项目实际判断翻车点，需要用户决策时才交互（少量问题直接问、成批问题用排版良好的 .md 收集），一轮没问完后续继续问，支持多轮动态交互。难度清单是 agent 的自检清单，不是给用户的问卷。
- **v3.1**（2026-08-08）：**一份完整问卷，一次填完**——agent 先用程序解析模板把 Shape 名/类型/表格行列预填（标 ✅），用户只需在问卷上做「人才能做的决策」（数据来源、更新模式、截图方式、文案风格等），不再拆多个 Phase 文件逐个填。问卷分 Part A 项目信息 / B 逐页决策 / C 截图图表 / D 数字与文案 / E 其他。
- **v3.0**（2026-08-08）：改为**问卷 .md 文件驱动交互**（直接在文档里勾选/填空，不必在对话框一问一答）；产出的 Skill 直接落你自己的 skills 目录自用，无需上传/分发；并入动态列、表格更新模式细分、同页混合嵌图、重复标题 nth 定位、表内固定汇总行、数据月份校验、全角数字清洗、AI 文案开头惯例、Shape 定位策略表等 9 项新覆盖
- **v0.2**（2026-08-08）：样板间项目验证完成，补齐动态页面/OCR/口头数据源/累积KPI/标题定位等 7 项差距
- **v0.1**：初始设计，6 Phase 引导流程

## 更新方式（不用重新安装）

仓库是分发点。生成器本体在维护者工作机上迭代，改完推送。你更新时**不用重装**，让 agent 覆盖旧目录即可：

> 更新我本地的 `monthly-report-skill-builder` skill，从 `https://github.com/Bananafish-cloud/monthly-report-skills` 拉最新版覆盖。

agent 会自动 git pull（或重新下载）覆盖。**更新后同样要【新开一个会话】** 才会加载新版本。

手动方式：重新下载 ZIP 解压 → 再右键跑一次 `install.ps1`（它检测到旧目录会自动覆盖）；或 `git pull` 后重新复制到 skills 目录。
