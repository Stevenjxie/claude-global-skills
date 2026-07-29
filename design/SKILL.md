---
name: design
description: "统一设计 Skill — 设计工作唯一入口/路由枢纽。覆盖: (0) 交互体验/流程/空态/UX文案 (→ ux-flow 门 + impeccable shape/critique/onboard/clarify), (A) Artifact 原型评估 (单文件/断外链, 栈规范与项目端不同), (1) 业务页面开发 (Vue/RN/小程序三端规范, 本 skill 权威), (2) 创意展示页 (landing page/showcase/海报 → taste/impeccable), (3) 截图提取设计系统 (→ impeccable extract), (4) UI 审查 (→ impeccable audit), (5) 品牌物料 (logo/CIP/banner/社媒图/slides → promax-design), (6) 动效 (→ gsap-*/emil-design-eng/apple-design)。当用户说\"做页面\"、\"设计UI\"、\"照着截图做\"、\"审查UI\"、\"美化\"、\"landing page\"、\"加动画\"、\"这个流程怎么走\"、\"交互体验\"、\"用户会不会卡\"、\"空态\"、\"错误提示怎么写\"、\"出几版看看\"、\"做个原型\"时触发。"
---

# 统一设计 Skill (路由枢纽 v2)

自动识别设计意图，路由到正确的工作流。

**v2.1 (2026-07-29) 变更**: 补 **Route 0 交互体验/流程**（原路由表全是产物导向，行为/流程问题无入口，`ux-flow` 只能靠 CLAUDE.md 硬门触发，走 design 永远碰不到）+ **Route A Artifact 原型**（taste §3.A 的 React/Tailwind/next-font 栈在 Artifact 里全部跑不了，此前无人标注）+ 边界铁律 5/6。

**v2 (2026-07-28) 变更**: 设计 skill 群精简后重排 — `banner-design`/`slides`/`ui-styling` 已删（前两者内容 promax-design 逐字节内置；shadcn 栈本项目用不上）；`gsap-*`×8 与 `ui-ux-pro-max` 只保留全局副本（`~/.claude/skills/`）；创意页与 UI 打磨首选 `impeccable`/`taste`（Steve 主用）。

## 意图检测与路由

| 用户说的 | 检测信号 | 路由 |
|----------|---------|------|
| "这个流程怎么走"、"用户会不会卡"、"操作步骤"、"交互体验"、"空态/首次使用"、"错误提示怎么写" | **行为/流程问题（不是要产物）** | **→ Route 0 交互体验**（见下，产物之前先走这里） |
| "出几版看看"、"做个原型"、"artifact 出图"、"哪个好" | 要可评估的原型，不是要落地代码 | **→ Route A Artifact 原型**（见下，栈规范与项目端完全不同） |
| "做一个xx页面"、"加个表单"、"写个列表页" | 具体业务功能 | **→ Route 1 业务页面**（本 skill 权威，见下） |
| "landing page"、"展示页"、"官网"、"portfolio"、"海报" | 独立创意页 | **→ `taste`**（`~/.claude/skills/taste/`，anti-slop landing/portfolio 专精，Design Read → 三旋钮） |
| "美化"、"打磨"、"重设计"、"这界面不够好" | 已有界面改进 | **→ `impeccable`**（craft/shape/polish/refine；先按其 SKILL.md 跑 context.mjs setup） |
| "照着这个截图做"、"参考这个设计" | 提供截图/参考图 | **→ `impeccable` extract** |
| "审查UI"、"检查设计"、"accessibility" | 审查类动词 | **→ `impeccable` audit** + `web-design-guidelines` 合规清单 + 对照 Route 1 references |
| "优化动画"、"动效"、"滚动动画"、"parallax" | 动画需求 | **→ `gsap-*`（全局）** 实现；动效代码 review → `review-animations`（严格关卡）；品味哲学 → `emil-design-eng`；Apple 式手势/spring → `apple-design` |
| "RN 卡顿"、"FPS/启动慢"、"bundle 太大"、"内存泄漏" | RN 性能 | **→ `react-native-best-practices`**（Callstack 官方：Hermes/FlashList/re-render/TTI） |
| "配色建议"、"字体搭配"、"这个品类该长啥样" | 设计灵感/情报 | **→ `ui-ux-pro-max`（全局，只读情报库）** |
| "做Logo"、"CIP"、"icon"、"banner"、"社媒图"、"pitch deck/演示" | 品牌/营销物料 | **→ `promax-design`**（全内置）；其外部依赖 `brand`/`design-system` 独立可用 |
| "AI 面板"、"AI 助手/对话界面"、"copilot"、"RAG UI"、"AI 工作台" | AI 产品功能/界面 | **→ `ai-interface-design`**（功能契约→状态机→信任控件→视觉，AIChat/SmartBI 场景专用） |
| "BP"、"商业计划书" | — | **→ `bp-creator`（全局）** |
| 图表/数据可视化 | — | **→ 内置 `dataviz` skill** |
| 不确定 | — | 问用户："你要做业务页面还是创意展示页？" |

## 外部 skill 委派地图 (v2)

| 需求 | 委派给 | 说明 |
|------|--------|------|
| 低技术素养用户流程（operator/仓管/质检） | `ux-flow`（项目内） | **强制门**，见 CLAUDE.md UX Flow Gate。brainstorming 的 propose approaches 之前必跑；Phase 1 的「UX Flow Analysis」是 spec 强制组成 |
| 交互体验 / 流程 / 空态 / UX 文案 | `impeccable` 的 `shape`/`critique`/`onboard`/`clarify` + `reference/interaction-design.md` | 见 Route 0 分诊表。这些是**行为**问题，别当成"做页面"路由到 Route 1 |
| 创意 landing / portfolio / 官网 / 重设计 | `taste`（frontmatter 名 `design-taste-frontend`） | 全局。真设计系统选型（Fluent/Material/Carbon/GOV.UK…）+ 反 AI 默认审美。**不接 dashboard/数据表/多步产品 UI** |
| 产品 UI 打磨 / 审查 / 截图提取 / 大胆视觉 | `impeccable` | 全局。子命令 craft/shape/audit/polish/extract/animate…；**必须先跑其 context.mjs setup 步骤** |
| 动效/微交互实现 | `gsap-core` `gsap-timeline` `gsap-scrolltrigger` `gsap-plugins` `gsap-utils` `gsap-performance` `gsap-react` `gsap-frameworks` | **全局副本**（项目副本 2026-07-28 已删）。Vue 用 `gsap-frameworks`。⚠️ 引入 gsap 依赖前先确认要采用（现有 `useCountUp` 是手写 RAF） |
| 动效/细节品味 review | `emil-design-eng`、`apple-design` | 全局。Emil 哲学（Before/After 表输出）；Apple spring/手势/材质 |
| 设计灵感 / 配色 / 字体 / 品类风格 / UX 指南 | `ui-ux-pro-max` | **全局副本**。只读情报库（84风格/161配色/73字体），只出建议不替代 Route 1 规范 |
| Logo / CIP / icon / banner / 社媒图 / slides | `promax-design` | 全内置（原 `banner-design`/`slides` 独立 skill 内容与之逐字节相同，已删）。AI 出图脚本需 `GEMINI_API_KEY`，缺则降级为规范/brief 建议 |
| AI 功能/界面设计（助手/copilot/RAG/数据分析 AI/生成工作台） | `ai-interface-design` | 全局（2026-07-28 自 Codex 侧引入）。先定 AI Product Contract 再谈样式；状态机 idle→streaming→tool-running→…；落地实现仍守 Route 1 三端规范与防呆 |
| 品牌 voice / 资产规范 / 一致性 | `brand` | promax 的外部依赖，独立可用（inject-brand-context.cjs 等脚本） |
| Token 架构 / CSS 变量体系 | `design-system` | promax 的外部依赖。仅 greenfield，不改现有三端 token |

### ⛔ 边界铁律 (防错栈污染)

1. **Route 1 三端业务页 (Vue Element Plus / RN Paper / 小程序 WXSS) 永远走本 skill 的 references**，绝不采纳 taste/impeccable/ui-ux-pro-max 的通用栈建议（shadcn/Tailwind/绿地配色）——会违反「不发明新样式」原则 + `fool-proof-design.md` 防呆规范。
2. taste/impeccable 只接**独立创意页**（landing/showcase/官网/海报/Artifacts）与 UI 打磨审查；业务页面落地实现回 Route 1 平台规范。
3. 防呆 (`fool-proof-design.md`) + `ux-flow` 门是 Route 1 的强制前置，外部 skill 不覆盖它们。
4. shadcn/ui + Tailwind 栈（原 `ui-styling` skill）已移除——三端都装不了；真有 React 绿地需求再从 claudekit 重装。
5. **交互体验问题不要路由到产物 skill**。"这一步用户会不会点错"、"空态显示什么"、"这句错误提示怎么写"是**行为**问题，答案在 Route 0 那批；路由到 taste/impeccable 的视觉工作流会答非所问。
6. **Artifact 原型 ≠ 交付物**。Route A 产物是评估用近似（装不了 Element Plus / Paper / WXSS 组件），选中后必须按 Route 1 平台规范重写，不得直接搬进业务代码。

---

## Route 0: 交互体验 / 流程（产物之前）

这块料分散在 7 个地方，没有统一入口——本表就是那个入口。**先判断问的是行为还是产物**：问"该怎么走/会不会卡/显示什么"是行为，进本表；问"长什么样"才是产物，回上面的意图表。

| 问题形态 | 去哪 |
|---|---|
| RN 低技术素养屏幕（operator/仓管/质检；报工/入库/出库/盘点/扫码收货） | **`ux-flow` 强制门** — CLAUDE.md UX Flow Gate 管辖，brainstorming 的 propose approaches 之前必跑 |
| 需求还没定、要做的是新功能 | `superpowers:brainstorming` 先行，再回本表 |
| 写码前规划一个功能的 UX/UI | `impeccable shape` |
| 已有界面的 UX 评审打分 | `impeccable critique`（快照存 `critique-storage.mjs`，`polish` 会当 backlog 读） |
| 首次运行 / 空态 / 激活流程 | `impeccable onboard` |
| 文案 / 标签 / 错误信息 | `impeccable clarify` |
| 通用交互原则 | `impeccable reference/interaction-design.md` |
| 无障碍 / 触控 / 表单 / 导航 合规清单 | `ui-ux-pro-max --domain ux`（99 条，优先级 1→10）+ `web-design-guidelines` |
| 三端防呆 | `fool-proof-design.md`（rule，`frontend`/`web-admin` 路径自动加载；Route 1 强制前置） |

⚠️ **operator 屏幕不要发散**。防呆规范的本质是**减少选择**，和"多出几版看看"方向相反。高频内部操作屏要的是可预测与一致，Route A 的原型 shuffle 不适用于这一类。

---

## Route A: Artifact 原型（评估用）

**硬约束**：Artifact 是单文件、无构建、CSP 断一切外部 host（CDN / 外链字体 / 远程图片 / fetch 全断）、没有 package.json。

### ⛔ taste §3.A 栈规范在此全部不适用

React / Next RSC、Tailwind v4 + `@tailwindcss/postcss`、`motion/react`、`next/font`、`@phosphor-icons/react`、`npx shadcn add` —— **一个都装不了**。改用：

| taste 原规范 | Artifact 里的替代 |
|---|---|
| Tailwind v4 utilities | 原生 CSS，全部内联 |
| `next/font` / 自托管 `@font-face` | 系统字体栈，或字体 data: URI 内嵌 |
| 图标库（Phosphor/Tabler…） | 手写内联 SVG——**此处覆盖 taste §3.C 的「禁止手绘 SVG 图标」**，因为图标库根本引不进来 |
| Motion / GSAP | 原生 CSS 动画或 WAAPI；真要 GSAP 必须内联源码 |
| `useMotionValue` 等 React 机制 | vanilla JS + CSS 自定义属性 |

### 图片资产

taste §4.8 的优先级链在此**失效**：本环境无 image-gen 工具，`picsum.photos` 被 CSP 断。可选项只有 ① data: URI 内嵌，② 纯 CSS/SVG 构图，③ 留标注占位（`<!-- TODO: hero 图 1600x1200 -->`）并在回复里告诉用户缺哪几张。**不要因为引不到图就退回手绘 SVG 插画**——impeccable 的禁令在这条上仍然生效。

### 仍然生效的

impeccable 的绝对禁令全套、对比度 ≥4.5:1、行长 65–75ch、`prefers-reduced-motion`、light/dark 双主题（`prefers-color-scheme` + `:root[data-theme]` 双向覆盖）、favicon 跨 redeploy 保持不变、宽内容自己 `overflow-x: auto`。

### 保真度分层（决定原型能评什么）

| 层 | 对象 | 能评 |
|---|---|---|
| **高** | 官网 / landing / showcase / pitch；驾驶舱与报表的视觉与信息架构 | 几乎等于交付物 |
| **中** | AI 面板 / 对话界面（流式态、工具运行态可做真交互假动作）；web-admin 业务页；小程序页 | **评「该怎么排」有效，评「长什么样」会失真** |
| **不适用** | RN 屏幕（浏览器跑不了 Paper / 手势 / 键盘行为）；要真实数据/权限/RLS 才能判断的页面 | 走 Route 0 / Route 1 |

---

## Route 1: 业务页面开发

### 平台自动检测

| 信号 | 平台 | 加载规范 |
|------|------|---------|
| 路径含 `web-admin/`、提到 Element Plus / Vue / el-table | **Vue Web Admin** | 读 [references/vue-web-admin.md](references/vue-web-admin.md) |
| 路径含 `frontend/CretasFoodTrace/`、提到 RN / Expo / Paper | **React Native** | 读 [references/react-native.md](references/react-native.md) |
| 路径含 `MallCenter/mall_miniprogram/`、提到小程序 / WXSS | **微信小程序** | 读 [references/miniprogram.md](references/miniprogram.md) |
| 多平台对比 | 跨平台 | 读 [references/cross-platform-tokens.md](references/cross-platform-tokens.md) |

**原则**: 严格遵循平台设计规范 (颜色/间距/组件)，不发明新样式。

---

## Route 2 fallback: 创意页设计原则（委派不可用时的最低标准）

正常情况创意页直接走 `taste`/`impeccable`。若不可用，至少守住：

1. **定调**: 选一个鲜明的美学方向，输出一行 Design Read 再动手
2. **排版**: 不用 Arial/Inter/Roboto 默认组合，选有个性的字体搭配
3. **色彩**: 大胆主色 + 锐利点缀，拒绝紫色渐变白底
4. **动效**: 入场动画 > 零散微交互，CSS-only 优先，必配 prefers-reduced-motion
5. **禁止**: cookie-cutter 三等分卡片、通用玻璃拟态、一切"AI味"审美

实现要求: 可运行的 production-grade HTML/CSS/JS 或框架代码。
