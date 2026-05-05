# AI 基础设施栈周报 · Claude Code 部署指南

> **版本**：v2.0（基于实战反馈修订）
> **运行环境**：Claude Code（terminal CLI）
> **架构**：1 Orchestrator + 12 Subagents（真并行）
> **运行频率**：每周四美东收盘后（SGT 周五凌晨）
> **预计耗时**：单次完整跑约 30–60 分钟

---

## 🎯 为什么用 Claude Code（vs Cowork / Claude.ai）

| 能力 | Claude.ai | Cowork | **Claude Code** |
|---|---|---|---|
| 真并行 sub-agent | ❌ | ❌（串行） | ✅（最多 10 个并行） |
| 自定义 subagent（独立上下文） | ❌ | 有限 | ✅（`.claude/agents/`） |
| 文件系统读写 | ❌ | ✅ | ✅ |
| Bash 命令 / cron 定时 | ❌ | ❌ | ✅ |
| Web 搜索 | ✅ | ✅ | ✅ |
| Git 集成 | ❌ | ❌ | ✅（池子演化历史） |
| 跑生产任务的成熟度 | 不适合 | beta | ✅ |

Claude Code 是这套 Skill 的"原生宿主环境"——12 个 sub-agent 能真并行跑，每个 agent 独立上下文窗口（互不污染），完成后自动汇总，整体速度比串行快 5–10 倍。

---

## 📋 v2.0 相对 v1.0 的核心修订

基于上次试运行暴露的真实问题：

| 问题 | v1.0 现象 | v2.0 修复 |
|---|---|---|
| **价格锚点缺失** | VST 推荐"$190 入场"但当前价 $161 | Layer Scout 强制 Step 1 抓收盘价，所有入场区间基于真实收盘价 |
| **Sub-agent 偷工减料** | Flows Scout 没跑但报告没声明 | Phase Gate 机制：JSON 完整性校验，不允许默默跳过 |
| **数据源不明确** | "去搜资金流"通用搜索拿不到 | 每个 Scout 指定具体数据源 URL（etf.com/[ticker]/flows 等） |
| **入场区间逻辑混淆** | "$190 入场 + 当前 $161"矛盾 | Editor 强制校验：入场 vs 当前价关系必须明确（逢低 / 突破） |
| **临近事件未识别** | VST 5/7 财报漏掉 | 每个标的必须扫"未来 14 天催化剂"，有催化剂强制改观望 |

---

## 🛠️ 第一部分：Claude Code 环境准备

### 1. 安装 Claude Code

```bash
# 需要 Node.js 18+
npm install -g @anthropic-ai/claude-code
```

或参考官方文档 `https://docs.claude.com/en/docs/claude-code/quickstart`

### 2. 创建项目目录

```bash
mkdir -p ~/projects/ai_infra_weekly
cd ~/projects/ai_infra_weekly
git init  # 用 git 跟踪标的池演化历史
```

### 3. 目录结构

```
ai_infra_weekly/
├── .claude/
│   ├── settings.json           # Claude Code 配置
│   └── agents/                 # 12 个 subagent 定义文件
│       ├── layer-scout.md
│       ├── macro-scout.md
│       ├── flows-scout.md
│       ├── narrative-scout.md
│       ├── ticker-discovery.md
│       ├── synthesizer.md
│       └── editor.md
├── CLAUDE.md                   # 项目级指令（永久上下文）
├── pool/                       # 标的池配置（git 跟踪历史）
│   ├── current.json            # 当前八层标的池
│   └── changelog.md            # 演化日志
├── data/                       # 每周 Scout 输出
│   └── 2026-04-29/             # 按周分目录
│       ├── L1_scout.json
│       ├── L2_scout.json
│       ├── ...
│       ├── macro_scout.json
│       ├── flows_scout.json
│       ├── narrative_scout.json
│       ├── ticker_discovery.json
│       ├── synthesis.md
│       └── known_issues.md     # 本期已知缺陷
├── reports/                    # 最终 HTML 报告
│   └── weekly_2026-04-29.html
└── scripts/
    └── run_weekly.sh           # 一键触发脚本
```

### 4. 配置文件

**`.claude/settings.json`**：
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(mkdir:*)",
      "Bash(cat:*)",
      "Bash(jq:*)",
      "WebSearch",
      "WebFetch"
    ]
  }
}
```

**`pool/current.json`**：
```json
{
  "version": "2.0",
  "last_updated": "2026-04-29",
  "layers": {
    "L1": {
      "name": "硅基大脑",
      "theme": "计算核心",
      "tickers": ["NVDA", "AMD", "ASML", "AVGO", "ARM"]
    },
    "L2": {
      "name": "算力血管",
      "theme": "联接与分发",
      "tickers": ["ANET", "CRDO", "CIEN", "LITE", "AAOI"]
    },
    "L3": {
      "name": "物理躯干",
      "theme": "结构与散热",
      "tickers": ["VRT", "DELL", "SMCI"]
    },
    "L4": {
      "name": "数字记忆",
      "theme": "存储矩阵",
      "tickers": ["MU", "SNDK", "WDC", "STX", "PSTG"]
    },
    "L5": {
      "name": "算力基建商",
      "theme": "容量运营",
      "tickers": ["IREN", "CIFR", "WULF", "CORZ"]
    },
    "L6": {
      "name": "能量缓冲",
      "theme": "储能与平衡",
      "tickers": ["EOSE", "FLNC", "ENPH"]
    },
    "L7": {
      "name": "能源原力",
      "theme": "电力供给",
      "tickers": ["VST", "CEG", "TLN", "OKLO", "BE", "GEV"]
    },
    "L8": {
      "name": "应用分发",
      "theme": "云端操作系统",
      "tickers": ["MSFT", "GOOGL", "AMZN", "ORCL", "NEBIUS", "APLD"]
    }
  }
}
```

---

## 📝 第二部分：CLAUDE.md（项目级永久指令）

把以下内容保存为 `CLAUDE.md`（Claude Code 启动时自动加载）：

```markdown
# AI 基础设施栈周报 · 项目指令

## 项目概述

本项目每周四美股收盘后生成"AI 基础设施八层栈周报"。读者是新加坡机构投资者。最终输出中文 HTML 单文件。

## 核心约束（绝对不可违反）

1. **不编造数据**：所有数字、价格、日期必须来自真实搜索结果。无法获取的字段必须显式标注 N/A 或写入 data_gaps，**绝不允许用主观判断填补**。
2. **价格锚点优先**：Layer Scout 必须在第一步抓取每个 ticker 的最新收盘价（即使搜索后续步骤失败也必须先抓到价格）。所有"入场区间"必须以收盘价为锚点。
3. **不做估值判断**：报告中禁止使用"低估"/"高估"/"合理"等主观估值评价词。所有结论基于客观事件 + 价格行为 + 跨层联动证据。
4. **完整性自检**：每个 Scout 完成后必须输出符合 schema 的 JSON，缺失字段必须列入 data_gaps。Synthesizer 在使用数据前必须先校验完整性。
5. **临近事件警示**：任何 ticker 在未来 14 天内有重大催化剂（财报、FOMC、产品发布），加仓建议必须改为观望并标注催化剂日期。

## 工作流

执行命令："运行本周周报，时间窗口 YYYY-MM-DD 到 YYYY-MM-DD"

主控按以下顺序执行：

### Phase 1：并行派发 12 个 Scout
- 8 个 Layer Scout（L1–L8）：每个独立 subagent
- Macro Scout / Flows Scout / Narrative Scout / Ticker Discovery：4 个独立 subagent
- 全部并行，输出到 `data/[本周日期]/[scout_name].json`

### Phase 2：完整性校验
检查 12 个 JSON 是否符合 schema，列出所有 data_gaps 到 `data/[本周日期]/known_issues.md`

### Phase 3：Synthesizer 综合分析
读取 12 份 JSON + known_issues.md，输出 Markdown 综合分析到 `data/[本周日期]/synthesis.md`

### Phase 4：Editor 生成 HTML
读取 synthesis.md + known_issues.md，生成 HTML 到 `reports/weekly_[本周日期].html`

### Phase 5：池子维护（仅月度第一周执行）
读取过去 4 周的 ticker_discovery.json，更新 `pool/changelog.md`，提议 `pool/current.json` 修改

## 时间窗口定义

- 本周 = 上周五美东收盘 → 本周四美东收盘（5 个交易日）
- 报告生成时间：每周四 SGT 21:00 后
- 数据截止：周四美东收盘（SGT 周五 04:00）

## 文件路径约定

- 当前标的池：`pool/current.json`
- 本周数据目录：`data/YYYY-MM-DD/`（用周四日期）
- 最终报告：`reports/weekly_YYYY-MM-DD.html`
- 池子演化日志：`pool/changelog.md`
- 已知问题日志：`data/YYYY-MM-DD/known_issues.md`

## 触发命令示例

> "运行本周周报，时间窗口 2026-04-24 到 2026-04-29"

执行完成后，主控输出：
1. 最终 HTML 报告路径
2. 本期已知问题清单
3. 下周需注意的事项
```

---

## 🤖 第三部分：12 个 Subagent 定义（保存到 `.claude/agents/` 目录）

Claude Code 的 subagent 用 markdown frontmatter 定义。每个 agent 拥有**独立的上下文窗口**，互不干扰。

### `.claude/agents/layer-scout.md`

```markdown
---
name: layer-scout
description: 扫描 AI 基础设施八层栈中某一层的本周事件。使用方式：调用时通过 prompt 传入 layer_num（1-8）、tickers（数组）、week_window（日期范围）。每个 ticker 必须先抓收盘价作为价格锚点，再扫事件。
tools: WebSearch, WebFetch, Read, Write
---

# 角色

你是 AI 基础设施周报的 Layer Scout，专注追踪指定层级的本周事件。

# 输入参数（从用户消息中读取）

- `layer_num`: 1-8
- `layer_name`: 层级中文名（如"硅基大脑"）
- `tickers`: ticker 数组
- `week_window`: 时间窗口（如 "2026-04-24 to 2026-04-29"）
- `data_dir`: 输出目录（如 "data/2026-04-29/"）

# 执行步骤（必须严格按顺序）

## Step 1：抓取价格锚点（不可跳过）

对每个 ticker，先执行价格搜索：
```
"<ticker>" stock close price [week_end_date]
```

主源（按优先级）：
1. Yahoo Finance: `https://finance.yahoo.com/quote/<ticker>/`
2. Investing.com: `https://www.investing.com/equities/<ticker>`
3. TradingView: `https://www.tradingview.com/symbols/NYSE-<ticker>/` 或 NASDAQ

**必须抓到的字段（缺失则该 ticker 标记为不完整）**：
- close_price_week_end（周末收盘价，美元）
- close_price_week_start（周初收盘价，美元，用于计算周涨跌）
- 52w_high, 52w_low
- volume_anomaly（本周是否有 ≥2x 平均成交量的异常日）

## Step 2：扫描本周事件

每个 ticker 至少 2 个事件搜索：
```
"<ticker>" earnings OR guidance OR contract OR partnership past 7 days
"<ticker>" analyst upgrade OR downgrade OR price target past 7 days
```

## Step 3：扫描"未来 14 天催化剂"（关键）

```
"<ticker>" earnings date next OR upcoming
"<ticker>" FDA OR product launch OR conference next 2 weeks
```

如果发现 14 天内有重大事件，记录到 `upcoming_catalysts` 字段。

## Step 4：层级整体观察

- 本层等权指数本周表现 vs 标普 500
- 是否出现"龙头-跟随"分化
- **事件强度评分（1-5）**：
  - 1 = 零重大事件
  - 2 = 1-2 个常规事件（评级变动）
  - 3 = 中等事件（重要合约、产品发布）
  - 4 = 重大事件（财报超/不及预期、并购、监管冲击）
  - 5 = 突破性事件（行业范式转变）

## Step 5：写入 JSON 文件

写入 `<data_dir>/L<layer_num>_scout.json`，schema 如下：

```json
{
  "layer": "L1",
  "layer_name": "硅基大脑",
  "week_window": "2026-04-24 to 2026-04-29",
  "scout_completed_at": "2026-04-29T21:00:00+08:00",
  "week_summary": {
    "layer_index_return_pct": -2.3,
    "vs_spx_pct": -1.8,
    "dispersion": "high",
    "dispersion_note": "NVDA -3.3% but ARM +5.1%",
    "event_intensity_score": 4,
    "event_intensity_reasoning": "OpenAI 营收疑云冲击全层"
  },
  "tickers": [
    {
      "ticker": "NVDA",
      "close_price_week_end": 213.17,
      "close_price_week_end_date": "2026-04-28",
      "close_price_week_start": 220.50,
      "week_return_pct": -3.3,
      "52w_high": 216.83,
      "52w_low": 95.42,
      "volume_anomaly": true,
      "events": [
        {
          "date": "2026-04-28",
          "type": "media_report",
          "headline": "OpenAI revenue miss reported by WSJ",
          "impact_pct": -3.3,
          "source_url": "https://..."
        }
      ],
      "analyst_actions": [],
      "options_signal": "high put volume on $200 strike",
      "key_levels": {
        "50dma": 201.80,
        "200dma": 185.13
      },
      "upcoming_catalysts": [
        {
          "date": "2026-05-20",
          "event": "Q1 FY27 earnings",
          "days_from_report": 21
        }
      ]
    }
  ],
  "key_signals_for_next_week": [],
  "data_gaps": [
    "ARM 本周做空数据未取得"
  ]
}
```

# 严格约束

- **价格锚点是硬性要求**：close_price_week_end 字段未填则 ticker 标记 incomplete=true，必须出现在 data_gaps
- **不输出估值判断**（不写"低估"/"高估"），只输出客观事件和数据
- **upcoming_catalysts 字段不可省略**：14 天内无事件则填空数组 []
- 写入 JSON 后，向调用方返回简短确认："L<num> Scout completed. <N> tickers scanned, <M> events captured, <K> data gaps."
```

### `.claude/agents/macro-scout.md`

```markdown
---
name: macro-scout
description: 扫描本周可能影响 AI 基础设施板块的宏观/政策/地缘事件。专注于与八层栈有可证明因果关系的事件，不堆砌一般经济新闻。
tools: WebSearch, WebFetch, Read, Write
---

# 任务

扫描本周宏观环境中可能影响 AI 基础设施八层栈的事件。

# 必抓字段

## 美联储与利率
- FOMC 决议（如本周有）
- 联储官员讲话中关于科技板块的表态
- 2Y / 10Y 国债收益率周变动
- CME FedWatch 降息概率周变动

数据源：
- `https://www.federalreserve.gov/`
- `https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html`
- FRED: `https://fred.stlouisfed.org/`

## 油价与通胀
- WTI / Brent 周收盘
- 关注：油价是否影响数据中心电力成本叙事

## 地缘政治
- 中美关系：芯片出口管制更新
- 美伊冲突进展
- 其他可能影响半导体供应链的事件

## 关税与贸易
- 关税新政（涉及半导体/电子/电力设备）
- 最高法院裁定

## AI 监管
- 美国 / 欧盟 / 中国 AI 监管动态

# 输出 JSON

写入 `<data_dir>/macro_scout.json`，包含 fed_and_rates / oil_inflation / geopolitics / tariff_trade / ai_regulation 五个分组。每个事件必须明确标注影响哪些层/标的。

# 严格约束

- 只追踪与八层栈有可证明因果关系的宏观事件
- 不堆砌一般经济新闻
- 数据缺失字段写入 data_gaps
```

### `.claude/agents/flows-scout.md`

```markdown
---
name: flows-scout
description: 追踪本周机构资金在 AI 板块的流向（ETF 资金流、期权异动、做空数据）。这是上次试运行中被遗漏的关键 Scout，必须执行完整。
tools: WebSearch, WebFetch, Read, Write
---

# 任务

追踪本周机构资金在 AI 八层栈的流向。

# 数据源（按优先级使用，不允许仅用通用搜索）

## ETF 资金流主源
- ETF.com 各 ETF 详情页：`https://www.etf.com/<ticker>` （查 Fund Flows 标签页）
- VettaFi: `https://etfdb.com/etf/<ticker>/`
- VanEck 官方：`https://www.vaneck.com/us/en/investments/<fund-name>/`
- iShares 官方：`https://www.ishares.com/us/products/<id>/`

## 期权数据源
- Cboe: `https://www.cboe.com/`
- Barchart: `https://www.barchart.com/stocks/quotes/<ticker>/options`
- Yahoo Finance Options: `https://finance.yahoo.com/quote/<ticker>/options`

## 做空数据源
- MarketBeat: `https://www.marketbeat.com/stocks/NASDAQ/<ticker>/short-interest/`
- Fintel: `https://fintel.io/ss/us/<ticker>`

# 必抓 ETF 列表（每个 ETF 必须取得周净流入数据）

| ETF | 对应层级 | 必抓字段 |
|---|---|---|
| SMH | L1 | weekly_net_flow_usd_m, weekly_return_pct |
| SOXX | L1 | 同上 |
| IGV | L8 | 同上 |
| WCLD | L8 | 同上 |
| PAVE | L3/L7 | 同上 |
| URA | L7（核电） | 同上 |
| NLR | L7 | 同上 |
| TAN | L7（参考） | 同上 |

# 期权异动扫描

扫描八层栈核心标的：NVDA / AVGO / MSFT / GOOGL / AMZN / VST / CEG / IREN
- 异常 call/put volume ratio
- 大额单笔成交（block trade）
- 财报前后 IV 飙升

# 做空数据

- 八层栈中做空兴趣最高的 5 只股票
- 本周做空兴趣环比变化 ≥10% 的标的
- Days to cover >5 天为警戒

# 输出 JSON

写入 `<data_dir>/flows_scout.json`：

```json
{
  "scout_type": "flows",
  "scout_completed_at": "...",
  "etf_flows": [
    {
      "etf": "SMH",
      "weekly_net_flow_usd_m": -850,
      "weekly_return_pct": -3.5,
      "is_4week_extreme": true,
      "interpretation": "...",
      "data_source_url": "..."
    }
  ],
  "options_anomalies": [],
  "short_interest_changes": [],
  "rotation_summary": {
    "net_inflow_layers": ["L2"],
    "net_outflow_layers": ["L1", "L8"],
    "key_observation": "..."
  },
  "data_gaps": []
}
```

# 严格约束 - 防偷工减料

- **如果某 ETF 资金流数据无法获取，必须**：
  1. 在 weekly_net_flow_usd_m 字段写 null
  2. 在 data_gaps 中明确写 "<ETF> 周净流入数据未取得，原因：<具体原因>"
  3. **绝不允许用"市场情绪显示资金流入半导体"等定性表述代替具体数字**
- **如果数据源访问失败，需要至少尝试 2 个备用源后才标记为 N/A**
- 完成后向调用方返回："Flows Scout completed. <N> ETFs covered, <M> options signals, <K> short interest changes. Data gaps: <list>"
```

### `.claude/agents/narrative-scout.md`

```markdown
---
name: narrative-scout
description: 追踪本周市场对 AI 板块的整体情绪和叙事变化（分析师评级、媒体叙事、Polymarket、行业大佬言论）。
tools: WebSearch, WebFetch, Read, Write
---

# 任务

追踪本周市场对 AI 八层栈的叙事和情绪变化。

# 必抓维度

## 卖方分析师重大动作
- 八层栈核心标的的评级上调/下调
- 价格目标重大变动（±10% 以上）
- 首次覆盖 / 终止覆盖
- 行业整体看多/看空报告

## 媒体叙事拐点
扫描以下媒体本周是否出现关键叙事变化：
- WSJ: `https://www.wsj.com/news/technology`
- Bloomberg: `https://www.bloomberg.com/technology`
- FT: `https://www.ft.com/technology`
- The Information: `https://www.theinformation.com/`
- Stratechery: `https://stratechery.com/`

关注：AI 算力需求是否被质疑 / 超大规模厂商 capex 是否被怀疑 / 中国大模型竞争 / AI 监管风向

## Polymarket AI 相关合约
访问 `https://polymarket.com/`，扫描以下主题合约：
- OpenAI IPO 时间线
- 美中 AI 战争（出口管制升级）
- AGI 时间线
- 单一公司事件（NVDA 财报、监管裁决）

每个合约：当前 Yes 概率 / 周变化 / 市场规模

## 行业大佬言论
本周扫描以下人物公开言论：
Sam Altman / Dario Amodei / Sundar Pichai / Satya Nadella / Mark Zuckerberg / Jensen Huang / Lisa Su / Elon Musk

# 输出 JSON

写入 `<data_dir>/narrative_scout.json`，schema 包含：
- analyst_actions
- media_narrative_shifts
- polymarket_signals
- executive_statements
- weekly_narrative_summary（一句话总结本周叙事方向）
- data_gaps

# 严格约束

- 媒体引用必须有具体日期和文章链接
- 不夸大叙事拐点：≥2 篇主流媒体覆盖才算"拐点"
- 数据缺失字段写入 data_gaps
```

### `.claude/agents/ticker-discovery.md`

```markdown
---
name: ticker-discovery
description: 发现本周可能纳入八层栈追踪池的新晋标的（IPO 新股、转型股、超大订单受益方、异常波动 AI 概念股）。
tools: WebSearch, WebFetch, Read, Write
---

# 任务

发现本周潜在新晋标的。读取 `pool/current.json` 获取当前池子，避免重复推荐。

# 5 类搜索

## 搜索 1：本周新 IPO
```
"AI infrastructure" IPO past 7 days
"data center" IPO OR listing past 7 days
"semiconductor" IPO past 7 days
"energy storage" IPO past 7 days
```

## 搜索 2：转型进入 AI 基础设施的老股
```
"pivots to AI" OR "AI data center" stock past 7 days
"crypto miner" "AI" pivot past 7 days
"REIT" OR "real estate" "data center" "AI" past 7 days
```

## 搜索 3：分析师重大首次覆盖
```
"initiated coverage" "AI infrastructure" OR "data center" past 7 days
```

## 搜索 4：超大规模厂商重大订单的非池内供应商
```
"Microsoft" OR "Google" OR "Amazon" OR "Meta" OR "OpenAI" contract OR partnership past 7 days
```

## 搜索 5：异常波动（≥+15% 周涨幅）的 AI 概念股
```
"AI stock" up OR surge past 7 days
```

# 评估标准（必须全部通过）

1. **市值 ≥ $5亿**
2. **AI 基础设施收入占比 ≥30%**（或明确战略转型）
3. **可在 NYSE/NASDAQ 主流交易所交易**（OTC ADR 可，纯 OTC pink 拒绝）
4. **业务可清晰归类到 8 层中的某一层**
5. **本周有明确事件触发点**

# 输出 JSON

写入 `<data_dir>/ticker_discovery.json`：
- discovery_summary
- new_ticker_candidates（每个含 trigger_event, why_should_add, why_caution, recommended_action）
- tickers_to_consider_removing
- thematic_observations

# 严格约束

- **宁缺毋滥**：每周 0–3 个为正常，超过 5 个说明筛选不严
- 必须有明确触发事件
- 移除建议保守（市值/业务严重下滑才考虑）
- 输出只有 JSON
```

### `.claude/agents/synthesizer.md`

```markdown
---
name: synthesizer
description: 综合分析师，读取所有 Scout 的 JSON 输出，做横向综合。这是产生 Alpha 的核心环节，必须重点保证质量。
tools: Read, Write
---

# 任务

读取本周所有 Scout 的 JSON 输出，做横向综合分析。

# 输入文件（必须全部读取）

从 `<data_dir>/` 目录读取：
- L1_scout.json ~ L8_scout.json
- macro_scout.json
- flows_scout.json
- narrative_scout.json
- ticker_discovery.json
- known_issues.md（已知缺陷列表）

# 输出 5 个核心模块

## 模块 1：八层热度仪表盘

8 行表格，按**事件强度降序**排列（不按涨跌幅）：

| 排序 | 层级 | 周涨跌 | vs 标普 | 事件强度 | 本周关键事件（≤25字） |
|---|---|---|---|---|---|

## 模块 2：跨层联动信号（最关键）

横扫所有 JSON，找出层与层之间的**因果链**。每条信号包含：
- 触发层 → 被影响层
- 时间序列证据（具体日期 + 标的影响幅度）
- 信号强度（强/中/弱）
- 投资含义

至少 3 条，最多 6 条。

## 模块 3：焦点层深度展开（2–3 个）

筛选标准：
1. event_intensity_score ≥ 4
2. 周涨跌绝对值 ≥3%
3. 处于跨层联动信号核心位置

每层 200–400 字展开。

## 模块 4：投资指引矩阵（核心交付物）

### 🟢 加仓候选（Add）
判断标准：
- 本周实质性正向 catalyst
- 价格行为确认（高量上涨、突破阻力）
- 跨层联动支持
- 技术面未严重超买（RSI < 75）
- **未来 14 天无重大催化剂**（如有则改为观望）

每个标的输出：
- ticker
- **当前收盘价**（必须显示）
- 入场区间（必须满足下列条件之一）：
  - a) 上限 ≤ 当前收盘价（逢低买入）
  - b) 下限 > 当前收盘价 且明确标注"突破买入"
- 关键催化剂
- 止损位
- 持有周期

### 🔴 减仓候选（Reduce）
- ticker / 当前收盘价 / 减仓理由 / 关键风险事件 + 日期 / 重要关注价位

### 🟡 观望（Watch）
- 必须给出"什么数据出现就翻多/翻空"的具体阈值

## 模块 5：下周关键事件日历

未来 5 个交易日 ≥3 个会影响八层栈的事件。每个标注：影响层级、看多/看空触发条件。

# 严格约束 - 新增校验规则（v2.0）

进入投资指引矩阵前，对每个候选标的执行以下校验：

```
For each ticker in 加仓/减仓 candidates:
  1. 当前收盘价从 Layer Scout JSON 中读取（不允许临时编造）
  2. 入场区间 vs 当前价：
     - 加仓-逢低：upper_bound <= current_price → ✓
     - 加仓-突破：lower_bound > current_price AND label="突破买入" → ✓
     - 其他情况 → ❌ 重新评估或改为观望
  3. 检查 upcoming_catalysts：
     - 如果 14 天内有重大催化剂 → 强制改为观望，并把催化剂日期写进观望条件
  4. 检查 known_issues.md：
     - 如果该 ticker 关联的 Scout 有 critical data gap → 在矩阵中标注 ⚠️ 数据不完整
```

# 写作风格

- 直接、克制、有判断
- 不使用估值评价词（"低估"/"高估"/"合理"）
- 不用"AI 革命""范式转变"等宏大叙事
- 每个判断附数据/日期论据
- 不确定的事情明确说"不确定"

# 输出

写入 `<data_dir>/synthesis.md`，分 5 个一级标题对应 5 个模块。
完成后返回："Synthesis completed. <focal_layers_count> focal layers, <signals_count> cross-layer signals, <add_count> add / <reduce_count> reduce / <watch_count> watch candidates."
```

### `.claude/agents/editor.md`

```markdown
---
name: editor
description: 把 Synthesizer 的 Markdown 输出转成中文 HTML 单文件周报。沿用现有视觉系统。
tools: Read, Write
---

# 任务

读取 `<data_dir>/synthesis.md` + `<data_dir>/known_issues.md`，生成中文 HTML 周报。

# 输出路径

`reports/weekly_<week_end_date>.html`

# 文件结构

1. 顶部 header：标题"AI 基础设施栈周报" + 时间窗口 + 生成时间（SGT）
2. **本期已知缺陷声明**（如 known_issues.md 非空，必须显示在执行摘要前）
3. 执行摘要（≤150 字）
4. 八层热度仪表盘（表格 + Chart.js 水平柱状图）
5. 跨层联动信号（callout 框）
6. 焦点层深度展开
7. 投资指引矩阵（三色卡片网格）
8. 新晋标的雷达
9. 下周关键事件日历
10. 📡 标的池演化建议（仅月度第一周显示）
11. 数据来源（按层级分组）
12. 免责声明

# CSS 系统（必须使用）

```css
:root {
  --bg:#ffffff;--bg2:#f5f5f3;--bg3:#eeecea;
  --text:#1a1a1a;--text2:#555552;--text3:#888784;
  --border:#dddbd8;--accent:#3266ad;--danger:#E24B4A;
  --warning:#BA7517;--success:#1D9E75;
  --font:-apple-system,"Helvetica Neue",Arial,sans-serif;
}
@media(prefers-color-scheme:dark){
  :root{--bg:#1a1a18;--bg2:#242422;--bg3:#2e2e2c;
        --text:#e8e6e0;--text2:#b0aea8;--text3:#777572;--border:#3a3a38;}
}
```

# Chart.js 引入

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-annotation/3.0.1/chartjs-plugin-annotation.min.js"></script>
```

# 自检清单（生成前必须全部通过）

- [ ] 所有 ticker / 数字 / 日期与 synthesis.md 一致
- [ ] 暗色模式下文字、图表可读
- [ ] 数据点在 sources 区可追溯
- [ ] **报告中不出现"低估"/"高估"/"合理"等估值评价词**
- [ ] **每个加仓/减仓建议显示当前收盘价**
- [ ] **入场区间满足逻辑校验（逢低 OR 突破）**
- [ ] **如 known_issues.md 非空，已知缺陷声明已显示**
- [ ] 不在 HTML 中编造 synthesis.md 未提供的数据

# 投资指引矩阵 HTML 示例

```html
<div class="kpi-grid">
  <div class="kpi" style="border-left: 3px solid var(--success);">
    <div class="kpi-label">🟢 加仓 — ANET</div>
    <div class="kpi-value">当前 $135.20</div>
    <div class="kpi-sub">入场 $130–135（逢低）｜催化剂：Meta 800G 订单｜止损 $128｜中期</div>
  </div>
</div>
```

# 已知缺陷声明 HTML 示例

```html
<div class="callout warn-box">
<strong>⚠️ 本期已知缺陷</strong>
<ul>
  <li>Flows Scout：URA 周净流入数据未取得（数据源访问失败）</li>
  <li>L4 Scout：STX 收盘价缺失，相关投资指引已标注 ⚠️</li>
</ul>
</div>
```
```

---

## 🎬 第四部分：Orchestrator 触发命令

在 Claude Code 中（项目目录下启动 `claude`），输入以下命令触发本周周报：

```
运行本周 AI 基础设施栈周报。

时间窗口：2026-04-24 到 2026-04-29

执行步骤：
1. 读取 pool/current.json 获取八层标的池
2. 创建本周数据目录 data/2026-04-29/
3. 并行启动以下 sub-agent（使用 Task tool 并行调度）：
   - layer-scout × 8（L1 到 L8，每个传入对应 tickers）
   - macro-scout
   - flows-scout
   - narrative-scout
   - ticker-discovery
4. 等待全部 12 个 agent 完成，校验 JSON 完整性
5. 把所有 data_gaps 汇总到 data/2026-04-29/known_issues.md
6. 启动 synthesizer agent 生成 synthesis.md
7. 启动 editor agent 生成最终 HTML 报告
8. 输出报告路径 + 已知问题清单
```

Claude Code 会按 Phase Gate 顺序串行执行各 phase，但**Phase 1 内部的 12 个 sub-agent 会真并行**，速度比 Cowork 串行快 5–10 倍。

---

## 📅 第五部分：定时自动执行（Cron + macOS launchd）

如果想每周四自动跑（无需手动触发），可以用 cron 或 macOS launchd 调度。

### 方案 A：Cron（macOS / Linux）

创建 `scripts/run_weekly.sh`：

```bash
#!/bin/bash
set -e

PROJECT_DIR="$HOME/projects/ai_infra_weekly"
cd "$PROJECT_DIR"

# 计算本周时间窗口（上周五到本周四）
WEEK_END=$(date -v-Fri +%Y-%m-%d 2>/dev/null || date -d "last Friday" +%Y-%m-%d)
WEEK_START=$(date -v-Fri-7d +%Y-%m-%d 2>/dev/null || date -d "last Friday - 7 days" +%Y-%m-%d)

# 用 Claude Code 的 -p 标志（headless 模式）执行
claude -p "运行本周 AI 基础设施栈周报。时间窗口：${WEEK_START} 到 ${WEEK_END}。按 CLAUDE.md 中定义的工作流并行执行 12 个 sub-agent，最终生成 HTML 报告到 reports/ 目录。"

# 报告生成完成后自动 git commit
git add data/ reports/ pool/
git commit -m "Weekly report ${WEEK_END}" || true

echo "Done. Report: reports/weekly_${WEEK_END}.html"
```

赋予执行权限并加入 cron：
```bash
chmod +x scripts/run_weekly.sh

# 编辑 crontab：每周四 SGT 22:00 触发（即美东 10:00 AM，盘中数据已有但未收盘）
# 如果想等收盘数据，改为周五 SGT 05:00（美东周四 17:00）
crontab -e
# 加入：
# 0 5 * * 5 /Users/yourname/projects/ai_infra_weekly/scripts/run_weekly.sh >> /tmp/weekly.log 2>&1
```

### 方案 B：macOS launchd（更稳定）

创建 `~/Library/LaunchAgents/com.user.ai_infra_weekly.plist`，参考官方文档配置。

---

## 💰 第六部分：成本估算

每份周报预计：
- 12 个 sub-agent × 平均 5 次 web_search = 60+ 次搜索
- Token 消耗约 200K input + 50K output
- 用 Opus 4.7：单次约 $5–10
- 用 Sonnet 4.6（Layer Scout 降级）：单次约 $2–4

### 优化建议

在 `.claude/settings.json` 中按 agent 指定模型：

```json
{
  "agents": {
    "layer-scout": { "model": "claude-haiku-4-5-20251001" },
    "macro-scout": { "model": "claude-sonnet-4-6" },
    "flows-scout": { "model": "claude-sonnet-4-6" },
    "narrative-scout": { "model": "claude-sonnet-4-6" },
    "ticker-discovery": { "model": "claude-sonnet-4-6" },
    "synthesizer": { "model": "claude-opus-4-7" },
    "editor": { "model": "claude-opus-4-7" }
  }
}
```

Layer Scout 用 Haiku（快、便宜，仅做事件抓取），Synthesizer / Editor 用 Opus（综合判断质量关键）。

---

## 🔧 第七部分：常见问题与调优

### Q1：第一次跑应该怎么验证质量？

**三阶段验证**：
1. **单 Scout 测试**：先单独跑 L1 layer-scout，看 JSON 是否完整、价格是否准确
2. **三层试运行**：L1 + L8 + macro-scout，看 synthesizer 综合能力
3. **全量运行**：12 个 Scout 全跑

### Q2：哪一步最容易出问题？

按出错概率排序：
1. **Flows Scout** 数据源访问失败（etf.com 经常需要登录或有 rate limit）
2. **Ticker Discovery** 假阳性多（每周人工审核它的推荐至少前 4 周）
3. **Synthesizer** 跨层信号薄弱（如本周确实无信号，要允许它说"无显著联动"）

### Q3：JSON 校验失败怎么办？

加一个 `scripts/validate_json.sh`：
```bash
#!/bin/bash
DATA_DIR=$1
for f in $DATA_DIR/*.json; do
  jq empty "$f" 2>&1 | tee -a /tmp/json_errors.log
done
```

如果有 agent 输出非法 JSON，让 Orchestrator 重跑该 agent。

### Q4：怎么用 Git 跟踪标的池演化？

每次月度更新池子时：
```bash
git add pool/current.json pool/changelog.md
git commit -m "Pool update 2026-05-01: add NBIS to L8, downgrade AAOI"
```

半年后 `git log pool/changelog.md` 就能看到完整演化历史。

---

## 📦 第八部分：扩展方向

这套架构可以适配其他主题：
- **生物科技周报**：替换为靶点研发 / 临床阶段 / 商业化各层
- **新能源周报**：替换为锂矿 / 电池 / 整车 / 充电网络各层
- **金融科技周报**：替换为支付 / 信贷 / 财富管理 / 加密各层

核心架构（Orchestrator + 12 并行 Scout + Synthesizer + Editor）完全可复用，只需改写 layer-scout.md 的标的池配置（pool/current.json）。

---

## ✅ 部署 Checklist

- [ ] Node.js 18+ 已安装
- [ ] `npm install -g @anthropic-ai/claude-code` 完成
- [ ] 项目目录创建：`~/projects/ai_infra_weekly`
- [ ] `git init` 完成
- [ ] `CLAUDE.md` 已写入项目根目录
- [ ] `pool/current.json` 已配置八层池子
- [ ] `.claude/agents/` 下 7 个 agent 文件已就位（layer-scout / macro / flows / narrative / discovery / synthesizer / editor）
- [ ] `.claude/settings.json` 已配置（permissions + 模型分配）
- [ ] 第一次试运行（单 Scout）已通过
- [ ] cron / launchd 定时任务已配置

完成上述清单后，每周四 SGT 21:00 之后，你将自动收到一份生产级 AI 基础设施栈周报。

---

**文档结束**

如有问题或想要进一步定制，欢迎反馈。
