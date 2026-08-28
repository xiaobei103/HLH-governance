# Project Classification Standard：HLH AI 软件工程项目分类标准

> 本文件定义 HLH AI Software Engineering Workflow v3.1 的项目分类标准。
>
> 项目分类是 Template Selection Capability 的基础。
>
> 本文件用于在项目启动前判断项目类型、复杂度、和适合的模板方向。
>
> **本文件不推荐在不理解项目需求的情况下盲目选择模板。**

---

## 1. 文档定位

本文件是 `01-Standards/` 下的项目分类标准。

### 本文件回答的问题

- 这个项目属于什么类型？（Prototype？Business Application？AI Product？）
- 这个项目的用户规模和数据生命周期是什么？
- 这个项目需要多深的 AI 能力？（No AI？AI Assistant？Agent？）
- 这个项目的部署要求是什么？（本地？内网？生产环境？）
- 这个项目的复杂度级别是什么？
- 根据分类结果，适合什么模板方向？
- 什么情况下应该升级模板？（从 Prototype 到 Production SaaS 的迁移条件）

### 本文件不负责

- 历史项目模板来源 → legacy source repository 的 `02-Project-Templates/`（historical project-template source，不属于当前 Plugin Runtime）
- 具体技术栈选择细节 → `Tech_Stack_Standard.md`
- 具体数据库选型 → `Database_Standard.md`
- 历史项目的 CLAUDE.md 配置来源 → legacy source repository 的 `03-CLAUDE/`（historical CLAUDE source，不属于当前 Plugin Runtime）
- 模板的自动初始化或自动推荐 → 未来 Template Selector Skill（Phase 2+）

---

## 2. 分类流程

```
Project Requirement（项目需求）
    ↓
Project Classification（项目分类 — 本文件）
    ↓
Complexity Assessment（复杂度评估）
    ↓
Template Recommendation（模板推荐）
    ↓
Architecture Validation（架构验证）
```

**原则：**

1. **分类必须走完整流程。** 不能跳过分类直接选模板。
2. **分类必须在 Coding 开始前完成。** 不可以在写了一半代码后说"我觉得应该换个模板"。
3. **分类结果必须记录。** 每个新项目启动时，应在项目文档中记录分类结论和推荐模板。
4. **分类不是一次性的。** 项目从 Prototype 演进到 Production 时，需重新分类并评估模板迁移。
5. **分类不替代模板实现。** 本文件只定义分类标准，不创建模板目录或模板代码。

---

## 3. 分类维度

### 3.1 Project Type（项目类型）

项目的核心目的和最终形态。

| 类型 | 说明 | 典型特征 |
|------|------|----------|
| **Prototype** | 快速验证想法、MVP、Demo | 需求未定、快速迭代、可能抛弃、不追求生产质量 |
| **Business Application** | 企业内部系统、CRM、管理后台 | 明确业务需求、有限用户群、内部部署 |
| **Production SaaS** | 对外服务的 SaaS 产品 | 多租户、SLA、生产级可靠性、持续迭代 |
| **AI Product** | 以 AI 为核心卖点的产品 | AI 是核心功能、AI 工作流、模型调用、AI 扩展能力 |
| **Agent** | 自主或半自主执行任务的 AI Agent | 独立运行、工具调用、任务编排、无人值守时段 |
| **Website** | 官网、落地页、内容型站点 | 静态为主、内容展示、SEO、无需复杂后端 |

**原则：**

- **不清楚项目最终形态时，从 Prototype 开始。** 不在一开始就按 Production SaaS 架构。
- **Business Application 不等于 Production SaaS。** 企业内部 10 人用的 CRM 不需要多租户架构。先明确是内部系统还是对外产品。
- **AI Product 的关键判断：AI 是核心功能，还是辅助功能？** 如果去掉 AI 产品还能正常工作，那可能不是 AI Product。
- **Agent 的关键判断：是否需要自主决策和独立执行？** 如果只是"用户点一下，AI 回复一下"，那是 AI Assistant，不是 Agent。
- **Website 不包含复杂业务逻辑。** 如果网站需要用户登录、数据持久化、复杂交互，那应该归类为 Business Application 或 Production SaaS。

### 3.2 User Scale（用户规模）

| 级别 | 说明 | 典型场景 |
|------|------|----------|
| **Personal** | 单人使用 | 个人工具、效率工具、本地 Agent |
| **Small Team** | 2–50 人 | 小团队内部系统、部门工具、创业团队早期产品 |
| **External Users** | 50–数千外部用户 | SaaS 产品、对外服务平台 |
| **Large Scale** | 数千–数万+ 用户 | 大规模 SaaS、高并发平台、C 端产品 |

**原则：**

- **Personal 和 Small Team 不需要高并发架构。** 不要为 3 个人用的内部工具上 Redis + 消息队列。
- **External Users 意味着 SLA 和可靠性要求。** 用户不会等你重启服务器。
- **Large Scale 意味着架构复杂度全面提升。** 数据库、缓存、部署、监控全部需要考虑规模化。
- **不确定用户规模时，按当前已知的最小规模设计。** 预留扩展点，但不过度设计。

### 3.3 Data Lifecycle（数据生命周期）

| 级别 | 说明 | 典型场景 |
|------|------|----------|
| **Temporary Data** | 数据可丢弃、不需要迁移 | MVP 验证、一次性工具、Demo |
| **Business Data** | 数据是业务资产、需要保留和备份 | CRM 数据、订单数据、业务记录 |
| **Long-term Data Asset** | 数据是长期资产、需要迁移和演进 | AI 训练数据、用户行为数据、知识库、审计记录 |

**原则：**

- **Temporary Data 可以用 SQLite。** MVP 阶段的数据如果明确可丢弃，不需要 PostgreSQL。
- **Business Data 必须考虑备份、迁移、恢复。** 数据丢了 = 业务受损。
- **Long-term Data Asset 必须从第一天就考虑 Schema 演进的长期影响。** 数据模型的可扩展性、迁移的可回滚性、数据的可审计性。
- **Data Lifecycle 决定了数据库选型的最低标准。**见 `Complexity Assessment`。

### 3.4 AI Complexity（AI 复杂度）

| 级别 | 说明 | 典型场景 |
|------|------|----------|
| **No AI** | 不涉及 AI | 传统 CRUD、静态网站、纯管理系统 |
| **AI Assistant** | AI 作为辅助功能 | ChatGPT 式对话、AI 文案生成、AI 搜索 |
| **AI Workflow** | AI 参与多步骤业务流程 | AI 分析 + 人工审批、多步 Prompt 编排、Workflow 引擎 |
| **AI Agent Execution** | AI 自主执行任务 | Web Research Agent、Content Agent、Code Agent、Multi-Agent |

**原则：**

- **AI 复杂度决定了是否需要 PostgreSQL、AI 扩展接口、Agent 框架。**
- **No AI 项目不要引入 AI 依赖。** 不要为了"未来可能需要 AI"在传统 CRUD 项目里预埋 AI 基础设施。
- **AI Assistant 不等于 AI Product。** 一个 CRM 加了 AI 对话不自动变成 AI Product。
- **AI Agent Execution 是最高 AI 复杂度。** 涉及自主决策、工具调用、安全边界、人工兜底。不要在 Phase 1 就上 Agent。
- **AI 能力应逐级演进：** Prompt → Workflow → Skills → MCP → Subagents → Multi-Agent。不一步跳到最高级。

### 3.5 Deployment Requirement（部署要求）

| 级别 | 说明 | 典型场景 |
|------|------|----------|
| **Local** | 本地运行、单机部署 | 本地工具、个人 Agent、MVP 验证 |
| **Internal** | 内网部署、企业内部服务器 | 企业内部系统、部门工具 |
| **Production** | 公网生产环境 | SaaS 产品、对外服务、商业交付 |

**原则：**

- **Local 部署不需要 Docker、不需要 CI/CD、不需要云服务。** 不要为一个本地工具引入生产级部署复杂度。
- **Internal 部署需要考虑企业环境。** 客户有没有服务器？能不能装 Docker？IT 部门允不允许？
- **Production 部署必须有完整的部署文档、回滚方案、监控、备份。** 见 `Delivery_Standard.md`。
- **部署级别决定了模板的基础设施复杂度选择。**

---

## 4. 复杂度评估

### 4.1 复杂度级别定义

基于以上五个维度的组合，项目复杂度分为三个级别：

| 复杂度 | 说明 | 五个维度的典型组合 |
|--------|------|-------------------|
| **Low** | 轻量项目 | Prototype、Personal/Small Team、Temporary Data、No AI、Local |
| **Medium** | 常规商业项目 | Business Application、Small Team/External Users、Business Data、No AI/AI Assistant、Internal/Production |
| **High** | 生产级 AI 项目 | Production SaaS/AI Product/Agent、External Users/Large Scale、Long-term Data Asset、AI Workflow/Agent Execution、Production |

**注意：** 五个维度不是都必须达到对应级别。关键维度（AI Complexity、Data Lifecycle、Deployment Requirement）的权重更高。

### 4.2 模板匹配

| 项目特征 | 推荐模板 | 理由 |
|----------|----------|------|
| **Prototype** | `quick-sqlite-template` | 零部署、快速验证、数据可丢弃、单机运行。Local-first 最轻量方案。 |
| **Business Application** | `react-nest-mysql-template` | 国内商用最熟悉的数据库、NestJS 模块化结构适合长期维护、React 管理后台成熟。 |
| **Production SaaS** | `react-nest-postgres-template` | PostgreSQL 适合生产级数据场景、NestJS 支持复杂业务模块化、适合多租户和长期迭代。 |
| **AI Product** | `ai-product-postgres-template` | PostgreSQL + pgvector 支持 AI 数据场景、NestJS 适合多模块 AI 系统、预留 AI 扩展接口。 |
| **Agent** | `agent-production-template` | Node.js + TypeScript Agent、独立运行、工具调用、任务编排、安全边界明确。 |
| **Website** | `website-project-template` | 静态站点、无需后端和数据库、纯内容展示、可选 SSG。 |

**原则：**

- **模板匹配不是自动的。** 分类结果是推荐方向，不是强制命令。最终选择需要人工确认。
- **一个项目可能跨越多个模板阶段。** Prototype → Business Application → Production SaaS 是正常的演进路径。
- **不匹配时不要强行选择。** 如果推荐模板明显不适合当前项目，先重新检查分类是否正确。

---

## 5. Simple First 原则

### 5.1 核心声明

**HLH Workflow 不默认选择最高级技术。**

模板选择和技术栈选择遵循 **Simple First** 原则：

1. **简单问题使用简单方案。** Local 个人工具 → SQLite + Express。不需要 Docker、不需要 PostgreSQL、不需要 CI/CD。
2. **复杂问题使用匹配的生产级方案。** Production SaaS → PostgreSQL + NestJS + Docker。不为省事用 SQLite 硬抗。
3. **不为了"未来可能需要"提前引入复杂度。** 今天的 Prototype 不需要明天的 K8s 集群。
4. **不为了"显得高级"选择重架构。** 3 人小团队的 CRM 不需要微服务。

### 5.2 模板选择应基于

| 因素 | 问自己 |
|------|--------|
| **项目生命周期** | 这是一个用一周就丢的 Demo，还是持续维护数年的产品？ |
| **数据要求** | 数据可丢弃、需要备份、还是长期资产需要迁移演进？ |
| **用户规模** | 1 个人、50 个人、还是未知的外部用户？ |
| **AI 复杂度** | 不需要 AI、辅助性 AI、还是 AI 是核心功能？ |
| **部署要求** | 本地跑就行、内网部署、还是需要公网生产环境？ |

### 5.3 升级条件

从简单模板升级到复杂模板，必须同时满足：

1. **当前模板已无法满足明确的业务需求。** 不是因为"我觉得以后需要"。
2. **升级目标模板的技术要求已理解并能承担。** PostgreSQL 的运维、Docker 的配置、CI/CD 的搭建——这些都要有人负责。
3. **升级有明确的迁移方案和回滚方案。** 见 `Database_Standard.md` 和 `Delivery_Standard.md`。
4. **升级已获得用户单独授权。** 技术栈变更属于 P2 高风险，见 `Tech_Stack_Standard.md` §11。

**常见升级路径：**

```
quick-sqlite-template（Prototype）
    ↓ 验证需求、明确业务后
react-nest-mysql-template（Business Application）
    ↓ 需要对外服务、SLA、复杂数据后
react-nest-postgres-template（Production SaaS）
    ↓ AI 成为核心功能、需要 AI 扩展后
ai-product-postgres-template（AI Product）
```

**原则：** 不是每个项目都要走完这条路径。大多数项目停在 Business Application 就足够了。

---

## 6. 推荐输出格式

当未来 Template Selector 或人工分类完成后，输出应包含以下结构：

```
Project Classification:  [项目类型] / [用户规模] / [数据生命周期] / [AI 复杂度] / [部署要求]
Recommended Template:   [模板名称]
Reason:                 [为什么推荐这个模板：3-5 句话说明关键匹配点]
Risk:                   [当前分类下需要注意的风险：技术风险、运维风险、迁移风险]
Migration Boundary:     [如果未来需要升级，可能的升级路径和触发条件]
```

### 示例

```
Project Classification:  Business Application / Small Team / Business Data / AI Assistant / Internal
Recommended Template:   react-nest-mysql-template
Reason:                 内部 CRM 系统，小团队使用，MySQL 是国内商用最熟悉的数据库。
                        需要 AI 辅助文案生成，但 AI 不是核心功能。
                        NestJS 模块化适合长期维护和功能迭代。
Risk:                   AI 功能引入后需注意数据安全和用户隐私。
                        MySQL 的 AI 扩展能力有限，如果未来 AI 成为核心功能需评估迁移。
Migration Boundary:     如果未来需要对外 SaaS 服务或 AI 成为核心功能 →
                        评估迁移到 react-nest-postgres-template 或 ai-product-postgres-template。
```

---

## 7. 分类决策记录

每个新项目启动时的分类决策应记录以下内容：

| # | 记录项 | 说明 |
|---|--------|------|
| 1 | 分类日期 | 什么时候做的分类 |
| 2 | 项目名称 | 项目标识 |
| 3 | Project Type | Prototype / Business Application / Production SaaS / AI Product / Agent / Website |
| 4 | User Scale | Personal / Small Team / External Users / Large Scale |
| 5 | Data Lifecycle | Temporary Data / Business Data / Long-term Data Asset |
| 6 | AI Complexity | No AI / AI Assistant / AI Workflow / Agent Execution |
| 7 | Deployment Requirement | Local / Internal / Production |
| 8 | 复杂度级别 | Low / Medium / High |
| 9 | 推荐模板 | 模板名称 |
| 10 | 推荐理由 | 3-5 句关键匹配说明 |
| 11 | 风险和限制 | 当前分类下的注意事项 |
| 12 | 未来升级路径 | 什么条件下需要重新分类和模板迁移 |

---

## 8. 与其他标准文件的关系

| 标准文件 | 与本文件的关系 |
|----------|----------------|
| `Tech_Stack_Standard.md` | 定义技术栈选择原则。项目分类决定了技术栈方向。 |
| `Database_Standard.md` | 定义数据库选型标准。Data Lifecycle 和 User Scale 影响数据库选择。 |
| `Delivery_Standard.md` | 定义交付标准。Deployment Requirement 影响交付方式。 |
| `Security_Standard.md` | 定义安全标准。用户规模和部署要求影响安全级别。 |
| `template-registry.md` | Template Registry 记录模板能力。本文件的分类结果指向 Registry 中的对应模板。 |

---

## 9. 禁止事项

| # | 禁止事项 | 原因 |
|---|----------|------|
| 1 | 禁止不分类直接选模板 | 不了解项目就选模板 = 凭感觉做工程决策 |
| 2 | 禁止所有项目默认选最重模板 | 违反 Simple First 原则；增加不必要的复杂度 |
| 3 | 禁止把 SQLite Demo 当正式商业项目 | 见 `Database_Standard.md` §3.3 和 §15 |
| 4 | 禁止在开发中途随意更换模板 | 模板变更 = 架构变更 = P2 高风险 |
| 5 | 禁止为不需要 AI 的项目引入 AI 模板 | AI 基础设施增加复杂度、成本和维护负担 |
| 6 | 禁止跳过复杂度评估直接进入开发 | 没有评估就没有对风险的认知 |
| 7 | 禁止把分类结果当成不可更改的判决 | 项目演进时需重新分类和评估模板迁移 |

---

## 10. 当前阶段默认结论

1. **项目分类是模板选择的前置条件。** 必须先分类，后选模板。
2. **Simple First 是核心原则。** 不默认选择最重技术栈。
3. **分类维度覆盖项目类型、用户规模、数据生命周期、AI 复杂度、部署要求。** 五个维度综合决定复杂度。
4. **模板匹配是推荐方向，不是强制命令。** 最终选择需人工确认。
5. **分类不是一次性的。** 项目从 Prototype 演进到 Production 时需重新分类。
6. **当前 Phase 1 只建立分类标准和模板注册。** 不实现 Template Selector、不创建 AI Product Template。
7. **Template Registry（`template-registry.md`）是分类结果的具体映射。** 分类标准 + Registry = Template Selection Capability 的基础。

---

*Project Classification Standard — HLH AI Software Engineering Workflow v3.1 Phase 1*
