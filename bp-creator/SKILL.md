---
name: bp-creator
description: "商业计划书 (BP) 全流程制作。编排 NotebookLM 资料查询 + Deep Research 行业研究 + Business Document 正式文档 + PPT Creator 演示文稿，一站式输出投资人级别 BP。使用 /bp-creator 触发。"
---

# BP Creator - 商业计划书全流程制作

> **Goal**: 从用户的项目描述出发，通过多 Skill 编排，输出一套完整的投资人级别商业计划书（BP），包含 Markdown 全文、PDF 正式文档、PPTX 演示文稿。

## When to Use This Skill

触发条件:
- 用户说 "做BP"、"写商业计划书"、"准备融资材料"、"pitch deck"、"创业计划"
- 用户说 "business plan"、"商业计划"、"融资PPT"
- 用户有 NotebookLM 资料想做成 BP

## Quick Start

用户只需说 `/bp-creator` 或 "帮我做BP"，Skill 自动引导完成全流程。

---

## Phase 0: 信息采集 (必做)

### 最小问卷 (10 问)

向用户收集以下信息。用户未回答的项标记为 `[待补充]`，不阻塞流程。

| # | 问题 | 对应章节 |
|---|------|----------|
| 1 | **公司/项目名称**是什么？ | 封面 |
| 2 | **一句话描述**你们做什么？(电梯演讲) | 执行摘要 |
| 3 | 你们解决的**核心痛点**是什么？ | 问题 |
| 4 | 你们的**解决方案**是什么？核心差异化？ | 方案 |
| 5 | **目标市场**是谁？TAM/SAM/SOM 估算？ | 市场 |
| 6 | **商业模式**怎么赚钱？(收费方式、单价、毛利) | 商业模式 |
| 7 | 目前的**发展阶段和关键里程碑**？(用户数、营收、合作) | 牵引力 |
| 8 | **竞争格局**？你的壁垒/护城河？ | 竞争 |
| 9 | **团队**核心成员背景？ | 团队 |
| 10 | 本轮**融资金额和用途**？估值预期？ | 融资需求 |

### 信息采集原则

- 收到回答后，追问 1-2 个关键细节（如单价、增长率、客户案例）
- 如果用户提供了 NotebookLM 链接 → 进入 Phase 1
- 如果用户直接提供了全部信息 → 跳到 Phase 2
- 如果用户说"先做个框架" → 用行业默认数据填充，标注 `[需替换为实际数据]`

---

## Phase 1: 资料研究 (可选，有 NotebookLM 时触发)

### 1a. NotebookLM 文档查询

如果用户有 NotebookLM 笔记本，调用 `notebooklm` skill 提取关键数据：

```bash
# 检查认证
python ~/.claude/skills/notebooklm/scripts/run.py auth_manager.py status

# 查询笔记本获取数据
python ~/.claude/skills/notebooklm/scripts/run.py ask_question.py \
  --question "请列出所有与市场规模、用户数据、财务数据、竞品信息相关的内容" \
  --notebook-url "[用户提供的URL]"
```

**关键查询清单** (逐条查询，每次聚焦一个主题):
1. "这个项目的核心产品/服务是什么？解决什么问题？"
2. "目标市场规模和用户画像是怎样的？"
3. "有哪些财务数据？营收、成本、利润率？"
4. "竞争对手有哪些？我们的差异化优势是什么？"
5. "团队成员背景和核心能力？"
6. "当前的业务数据？用户数、增长率、转化率？"

### 1b. Deep Research 行业分析 (可选)

对于需要补充行业数据的场景，使用 `deep-research` skill:

```
/deep-research <行业名称>市场分析：市场规模、增长趋势、竞争格局、政策环境
```

### 1c. 数据整合

将 NotebookLM + Deep Research 的结果整合到以下结构：

```markdown
## 研究数据汇总
- 市场规模: [数据 + 来源]
- 增长率: [数据 + 来源]
- 竞品列表: [名称 + 融资 + 差异]
- 关键指标: [用户数/营收/增长]
```

---

## Phase 2: BP 正文撰写

### 标准 BP 结构 (10 章)

按以下结构生成完整的 Markdown 文档，保存到 `output/bp-{项目名}/bp-full.md`:

```markdown
# {公司名称} 商业计划书

## 1. 执行摘要 (Executive Summary)
- 一句话定位
- 核心问题 & 方案
- 市场机会 (TAM/SAM/SOM)
- 商业模式摘要
- 发展阶段 & 关键数据
- 融资需求

## 2. 痛点与机遇 (Problem)
- 行业痛点 (用数据说明严重性)
- 现有方案的不足
- 为什么是现在？(时机窗口)

## 3. 解决方案 (Solution)
- 产品/服务描述
- 核心功能与用户价值
- 技术架构 / 核心能力
- 产品路线图

## 4. 市场分析 (Market)
- TAM / SAM / SOM (带数据来源)
- 市场增长趋势
- 目标客户画像
- 市场进入策略

## 5. 商业模式 (Business Model)
- 收入模型 (订阅/交易/广告/...)
- 定价策略
- 单位经济模型 (CAC, LTV, 毛利率)
- 盈利时间线

## 6. 牵引力 (Traction)
- 关键里程碑时间线
- 核心指标 (用户数/营收/增长率)
- 标杆客户 / 案例
- 合作伙伴

## 7. 竞争分析 (Competition)
- 竞争格局图 (2x2 矩阵)
- 主要竞品对比表
- 差异化壁垒 / 护城河
- 为什么我们能赢

## 8. 团队 (Team)
- 核心团队成员 (姓名、职位、背景)
- 顾问 / 投资人
- 招聘计划

## 9. 财务计划 (Financials)
- 历史财务数据 (如有)
- 3-5 年财务预测
- 关键假设说明
- 盈亏平衡分析

## 10. 融资需求 (The Ask)
- 本轮融资金额
- 资金用途分配 (饼图)
- 预期估值 / 条款
- 里程碑对应关系
```

### 撰写原则

1. **数据驱动** — 每个论点配数据支撑，标注来源
2. **简洁有力** — 每段不超过 3-5 句，避免堆砌形容词
3. **投资人视角** — 回答 "为什么这个团队、这个时机、这个市场"
4. **诚实标注** — 缺失数据标记 `[需补充: xxx]`，不编造
5. **中英混排** — 专业术语保留英文 (TAM, LTV, CAC, SOM)

---

## Phase 3: 输出制品

### 3a. PDF 正式文档

使用 `pdf-creator` skill 生成正式 PDF:

```
/pdf-creator output/bp-{项目名}/bp-full.md
```

### 3b. Pitch Deck (PPTX)

使用 `ppt-creator` skill 生成 10 页演示文稿:

```
/ppt-creator 基于 output/bp-{项目名}/bp-full.md 生成投资人 Pitch Deck，10页结构:
1. 封面 (公司名+一句话)
2. 痛点 (Problem)
3. 方案 (Solution)
4. 市场 (Market Size TAM/SAM/SOM)
5. 产品 (Product Demo)
6. 牵引力 (Traction Metrics)
7. 商业模式 (Business Model)
8. 竞争 (Competition Matrix)
9. 团队 (Team)
10. 融资需求 (The Ask)
```

### 3c. Business Plan PDF (模板版)

如需正式模板格式，使用 `business-document-generator`:

```bash
# 生成数据文件
cat > /tmp/bp_data.json << 'EOF'
{
  "company_name": "{公司名}",
  "date": "{日期}",
  "mission": "{使命}",
  "vision": "{愿景}",
  "legal_structure": "{公司类型}",
  "business_stage": "{发展阶段}",
  "target_market": "{目标市场}",
  "total_addressable_market": "{TAM}"
}
EOF

# 生成 PDF
pip install pypdf reportlab 2>/dev/null
python3 ~/.claude/skills/ai-labs-claude-skills/dist/skills/business-document-generator/scripts/generate_document.py \
  business_plan /tmp/bp_data.json \
  --templates-dir ~/.claude/skills/ai-labs-claude-skills/dist/skills/business-document-generator/assets/templates \
  --output-dir output/bp-{项目名}
```

---

## Phase 4: 审查与交付

### 自查清单

| 检查项 | 标准 |
|--------|------|
| 执行摘要 | 2 分钟能读完，涵盖全貌 |
| 市场数据 | TAM/SAM/SOM 有来源引用 |
| 商业模式 | 有单位经济模型 (CAC < LTV/3) |
| 竞品分析 | 至少 3 个竞品 + 差异化矩阵 |
| 财务预测 | 3 年预测 + 关键假设透明 |
| 融资用途 | 金额与里程碑对应 |
| 团队 | 核心成员有相关经验 |
| 无编造数据 | 所有 `[需补充]` 已标注 |

### 交付物清单

```
output/bp-{项目名}/
  bp-full.md          # BP 全文 Markdown
  bp-full.pdf         # BP 正式 PDF
  pitch-deck.pptx     # 10 页 Pitch Deck
  business-plan.pdf   # 模板版 BP (可选)
  research-notes.md   # 研究数据汇总 (如有)
```

---

## 快速模式 vs 完整模式

| 模式 | 触发词 | 流程 | 产出 |
|------|--------|------|------|
| **快速** | "先出个框架"、"草稿" | Phase 0 → Phase 2 (默认数据) | bp-full.md |
| **标准** | "做BP"、"商业计划书" | Phase 0 → Phase 2 → Phase 3a+3b | md + pdf + pptx |
| **完整** | "完整BP"、"带研究的" | Phase 0 → 1 → 2 → 3 → 4 | 全部交付物 |

---

## Decision Flow

```
用户触发 /bp-creator
    |
    v
Phase 0: 问卷采集 (10 问)
    |
    ├── 有 NotebookLM? ──yes──> Phase 1a: 查询文档
    |                              |
    ├── 需要行业研究? ──yes──> Phase 1b: Deep Research
    |                              |
    v                              v
Phase 2: BP 正文撰写 <──── 整合研究数据
    |
    v
Phase 3: 多格式输出
    ├── /pdf-creator → bp-full.pdf
    ├── /ppt-creator → pitch-deck.pptx
    └── business-document-generator → business-plan.pdf (可选)
    |
    v
Phase 4: 自查 + 交付
```

## Resources

### 依赖的 Skills (已安装)

| Skill | 路径 | 用途 |
|-------|------|------|
| notebooklm | `~/.claude/skills/notebooklm/` | 文档查询 |
| ppt-creator | Plugin (daymade-skills) | PPTX 生成 |
| pdf-creator | Plugin (daymade-skills) | PDF 生成 |
| deep-research | Plugin (daymade-skills) | 行业研究 |
| business-document-generator | `~/.claude/skills/ai-labs-claude-skills/dist/skills/business-document-generator/` | 模板 PDF |

### references/

- `bp-outline-template.md` — BP 标准大纲模板 (可直接填充)
- `investor-pitch-tips.md` — 投资人视角的 BP 写作技巧
