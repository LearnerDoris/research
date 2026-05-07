---
title: AI 从业者行为 vs 股票反应数据集
date: 2026-04-30
tags:
  - 研究框架
  - AI
  - 事件驱动
  - 数据集
---

> 一句话：每行 = 一个 AI 行业事件 → 二级市场标的的传导对。强度分级基于 T+0 到 T+5 的价格反应幅度。

<iframe src="/research/reports-html/frameworks/AI-practitioner-vs-stocks.html" width="100%" height="600px" style="border:none;"></iframe>
<iframe src="/research/你的文件夹/你的文件.html" width="100%" height="600px" style="border:none;"></iframe>



## 数据集

按事件类型分组，组内按时间倒序。



### 产品发布

| 日期 | 主体 | 事件 | 标的 | 反应 | 方向 | 强度 |
|------|------|------|------|------|------|------|
| 2026-Q1 | Anthropic / Dario Amodei | Claude Cowork被点名为企业级AI杀手应用 | GOOGL / AMZN（投资人） | 持续支撑GOOGL/AMZN AI估值溢价 | 利好 | 中 |
| 2026-02-20 | Anthropic | Claude Code Security发布，自动扫描代码漏洞 | CRWD / NET / HACK | CRWD -8~10% / NET -8~10% / HACK ETF -9% | 利空 | 强 |
| 2026-02-06 | Anthropic | Claude Opus 4.6发布，强调金融研究/DD能力 | FDS / SPGI / MCO / NDAQ | FDS -10% / SPGI/MCO/NDAQ -5~8% | 利空 | 强 |
| 2026-02-03 | Anthropic | Claude Cowork企业版+行业插件发布 | TRI / LZ / RELX / IGV | TRI -15.83% / LZ -19.68% / RELX -14% / IGV -5.69% | 利空 | 极强 |
| 2025-08-07 | OpenAI / Sam Altman | GPT-5发布，被市场认为低于预期 | NVDA | NVDA从约$181进入6个月横盘（截至2026年初仍在$177） | 利空 | 中 |
| 2025-01-27 | DeepSeek | DeepSeek R1开源发布，宣称$5.6M训练成本 | NVDA / TSM / 半导体ETF | NVDA -16.9%（单日蒸发$589B市值，史上最大）/ Nasdaq -3.1% | 利空 | 极强 |

### 公开点评

| 日期 | 主体 | 事件 | 标的 | 反应 | 方向 | 强度 |
|------|------|------|------|------|------|------|
| 2026-Q1 | Sam Altman | X发文：'NVDA做最好的AI芯片，OpenAI将长期是巨大客户' | NVDA | NVDA当日+小幅，回应Reuters的'OpenAI不满NVDA新芯片'传闻 | 利好 | 中 |
| 2026-04-28 | Vinod Khosla | Fortune采访：详述2019年押注OpenAI的'地缘政治'逻辑 | NVDA / AVGO / TSM / ORCL | 无单日明显反应；强化'美国AI主权'框架 | 利好 | 中 |
| 2026-02 | Marc Benioff (CRM CEO) | 公开称'因AI不再增聘工程师/客服/律师' | CRM | CRM 2026 YTD -26%，道指第二差 | 利空 | 强 |
| 2025-Q4 | Andrej Karpathy | 公开使用并推荐Cursor作为日常代码工具 | Anysphere一级 / MSFT (GitHub竞品)间接 | Anysphere(Cursor)估值5个月内$10B→$29.3B | 利好 | 强 |
| 2025-Q3-Q4 | Sam Altman | 多次访谈强调'能源是AGI最大瓶颈' | OKLO / SMR / NNE / 铀矿股 | OKLO在Altman提及核能日通常+5-15% | 利好 | 强 |
| 2025-12 | Yann LeCun | 公开宣称'3-5年内LLM将被World Models取代' | META（间接） | 无显著T+0反应；但加剧Meta AI战略路线质疑 | 利空 | 弱 |
| 2025-07 | Sam Altman | X发文：OpenAI需把GPU从1M增至100M | NVDA / AVGO / AMD | NVDA当周+3-5%，催化夏季rally | 利好 | 强 |

### 投资行为

| 日期 | 主体 | 事件 | 标的 | 反应 | 方向 | 强度 |
|------|------|------|------|------|------|------|
| 2026-03 | Bezos / Cathay / HV / Greycroft | AMI Labs（LeCun）$1.03B at $3.5B pre | META（人才流失） | META短期无显著反应，但强化LeCun流失叙事 | 利好 | 弱 |
| 2026-02-24 | Andrej Karpathy | 参投MatX Series B（NVDA竞争性AI芯片） | NVDA（间接） | 无直接反应（MatX规模太小） | 利空 | 弱 |
| 2026-02 | GIC + Coatue | 领投Anthropic $30B Series G，估值$380B post-money | GOOGL / AMZN / NVDA | 三者均受益于'Anthropic估值锚' | 利好 | 强 |
| 2025-11-06 | Andrej Karpathy | 参投Inception Labs种子轮（扩散语言模型） | 无直接二级 | 推动diffusion LM作为研究方向的关注度 | 中性 | 弱 |
| 2025-07-15 | Mira Murati | Thinking Machines Lab a16z领投$2B种子，AMD战略参投 | AMD | AMD当周+3-4% | 利好 | 中 |
| 2021-11 / 2025-Q4 | Sam Altman | 个人累计投Helion Energy $375M+（核聚变） | OKLO / SMR / NNE | Helion每次相关新闻日，相关核能股+3-10% | 利好 | 强 |

### 人事/收购/战略

| 日期 | 主体 | 事件 | 标的 | 反应 | 方向 | 强度 |
|------|------|------|------|------|------|------|
| 2025-Q3 | OpenAI / Anthropic | Anthropic与GCP签大单，OpenAI拓展到GCP/Oracle/AWS | GOOGL / ORCL / AMZN | ORCL自2025年9月Oracle-OpenAI $300B披露后单日+43% | 利好 | 极强 |
| 2025-11-19 | Yann LeCun | 宣布离开Meta创办AMI Labs，新CAIO是Alexandr Wang | META | 事件前后META相对MAG7弱势，但无单日剧烈反应 | 利空 | 中 |
| 2025-11-03 | OpenAI | 宣布与AWS $38B基础设施合作 | AMZN | AMZN +1.10%当日，持续支持AI溢价 | 利好 | 中 |
| 2024-06 | Microsoft | Inflection AI核心团队（含Mustafa Suleyman）整体加入MSFT | MSFT | MSFT温和上涨；Inflection投资人（含Hoffman）获回报 | 利好 | 中 |
| 2023-11-20 | Microsoft (Satya) | 宣布雇佣被解雇的Altman和Brockman领导内部AI团队 | MSFT | MSFT premarket +1%+，事件后持续走强 | 利好 | 中 |

### 宏观/政策

| 日期 | 主体 | 事件 | 标的 | 反应 | 方向 | 强度 |
|------|------|------|------|------|------|------|
| 2025-09 | Oracle / Larry Ellison | 披露与OpenAI $300B五年合约 | ORCL | ORCL单日+43%（25年9月）；后回落约24% YTD 2026 | 利好 | 极强 |
| 2025-01-25 | Mark Zuckerberg | 宣布Meta 2025年AI capex $60-65B（远超分析师预期$51B） | NVDA / AVGO / META | NVDA / AVGO当周持续走强；META短期承压（capex超预期被看作压力） | 利好 | 强 |
| 2025-01-21 | Trump+Altman+Ellison+Son | Stargate $500B AI基础设施venture白宫宣布 | ORCL / NVDA / SoftBank / ARM | ORCL +7%（次日pre-market再+8%）/ NVDA +4% / 软银+11% | 利好 | 极强 |


## 事件详注

按强度倒序，仅列出强度为'极强'和'强'的事件。


**2025-01-21 · Trump+Altman+Ellison+Son · Stargate $500B AI基础设施venture白宫宣布**

- 标的：ORCL / NVDA / SoftBank / ARM
- 反应：ORCL +7%（次日pre-market再+8%）/ NVDA +4% / 软银+11%
- 滞后：T+0~1
- 注解：政府背书的AI infra叙事顶峰；ORCL从此进入AI股票主流。Musk公开质疑反而强化关注度

**2025-01-27 · DeepSeek · DeepSeek R1开源发布，宣称$5.6M训练成本**

- 标的：NVDA / TSM / 半导体ETF
- 反应：NVDA -16.9%（单日蒸发$589B市值，史上最大）/ Nasdaq -3.1%
- 滞后：T+0
- 注解：AI叙事最大单日重设：'低算力也能做强模型'瞬间击穿NVDA估值。Marc Andreessen公开赞为'最impressive的breakthrough'，加速恐慌

**2025-09 · Oracle / Larry Ellison · 披露与OpenAI $300B五年合约**

- 标的：ORCL
- 反应：ORCL单日+43%（25年9月）；后回落约24% YTD 2026
- 滞后：T+0
- 注解：单一合约驱动单日43%涨幅，史上罕见；但2026年随AI泡沫担忧大幅回调

**2025-Q3 · OpenAI / Anthropic · Anthropic与GCP签大单，OpenAI拓展到GCP/Oracle/AWS**

- 标的：GOOGL / ORCL / AMZN
- 反应：ORCL自2025年9月Oracle-OpenAI $300B披露后单日+43%
- 滞后：T+0
- 注解：AI实验室的多云策略=多家云厂同时受益；ORCL获得最大估值重设

**2026-02-03 · Anthropic · Claude Cowork企业版+行业插件发布**

- 标的：TRI / LZ / RELX / IGV
- 反应：TRI -15.83% / LZ -19.68% / RELX -14% / IGV -5.69%
- 滞后：T+0
- 注解：'AI替代SaaS'narrative首次形成可交易的板块sell-off。法律/数据/内容服务最受冲击

**2021-11 / 2025-Q4 · Sam Altman · 个人累计投Helion Energy $375M+（核聚变）**

- 标的：OKLO / SMR / NNE
- 反应：Helion每次相关新闻日，相关核能股+3-10%
- 滞后：T+0~5
- 注解：Altman'all liquid net worth'级别的押注，是该主题最强一级背书

**2025-01-25 · Mark Zuckerberg · 宣布Meta 2025年AI capex $60-65B（远超分析师预期$51B）**

- 标的：NVDA / AVGO / META
- 反应：NVDA / AVGO当周持续走强；META短期承压（capex超预期被看作压力）
- 滞后：T+0~5
- 注解：'capex竞赛升级'信号；hyperscaler表态历来是NVDA最有力短期催化剂

**2025-07 · Sam Altman · X发文：OpenAI需把GPU从1M增至100M**

- 标的：NVDA / AVGO / AMD
- 反应：NVDA当周+3-5%，催化夏季rally
- 滞后：T+0~5
- 注解：Altman的'数量级'叙事是NVDA最有效的口头利好；类似表态历次都引发短期反应

**2025-Q3-Q4 · Sam Altman · 多次访谈强调'能源是AGI最大瓶颈'**

- 标的：OKLO / SMR / NNE / 铀矿股
- 反应：OKLO在Altman提及核能日通常+5-15%
- 滞后：T+0~1
- 注解：Altman+核能已成为可重复交易的主题。叠加他个人对Helion投资$375M+，叙事极强

**2025-Q4 · Andrej Karpathy · 公开使用并推荐Cursor作为日常代码工具**

- 标的：Anysphere一级 / MSFT (GitHub竞品)间接
- 反应：Anysphere(Cursor)估值5个月内$10B→$29.3B
- 滞后：数月
- 注解：纯一级反应；二级映射弱（MSFT太大），但是研究员个人推荐能驱动估值的最强证据

**2026-02 · Marc Benioff (CRM CEO) · 公开称'因AI不再增聘工程师/客服/律师'**

- 标的：CRM
- 反应：CRM 2026 YTD -26%，道指第二差
- 滞后：持续
- 注解：罕见'CEO自我点评杀伤'：与Anthropic Cowork narrative形成共振，市场推断'CRM自己都不需要增长动力'

**2026-02 · GIC + Coatue · 领投Anthropic $30B Series G，估值$380B post-money**

- 标的：GOOGL / AMZN / NVDA
- 反应：三者均受益于'Anthropic估值锚'
- 滞后：T+0~5
- 注解：Anthropic估值大幅跳升=AI两强格局，GOOGL/AMZN持股价值大涨

**2026-02-06 · Anthropic · Claude Opus 4.6发布，强调金融研究/DD能力**

- 标的：FDS / SPGI / MCO / NDAQ
- 反应：FDS -10% / SPGI/MCO/NDAQ -5~8%
- 滞后：T+0
- 注解：Cowork+Opus 4.6组合拳，金融数据服务被点名替代。FactSet单日跌幅创纪录

**2026-02-20 · Anthropic · Claude Code Security发布，自动扫描代码漏洞**

- 标的：CRWD / NET / HACK
- 反应：CRWD -8~10% / NET -8~10% / HACK ETF -9%
- 滞后：T+0
- 注解：Anthropic-effect第三次精准打击，'AI产品=板块杀手'pattern已稳定
