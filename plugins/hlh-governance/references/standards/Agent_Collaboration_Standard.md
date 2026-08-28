# Agent Collaboration Standard：HLH AI 软件工程 Agent 协作标准

> 本文件定义 HLH AI Software Engineering Workflow v3.2 的 AI Coding Agent 协作治理规则。
>
> 本文件是 Agent Workflow Rules Alignment（Phase 5）的核心产出。
>
> **本文件定义 Agent 之间的协作规则，不是 Agent Runtime 实现。**

---

## 1. 文档定位

本文件是 `01-Standards/` 下的 Agent 协作标准。

### 本文件回答的问题

- 什么是 Lifecycle Role？什么是 Specialty Role？两者如何分离？
- Architect / Builder / Auditor 的职责边界是什么？
- 什么是 Single Write Authority？如何执行？
- Agent 之间如何安全交接（Handoff Gate）？
- 什么情况下必须 STOP？
- Model（模型）和 Role（角色）和 Permission（权限）的关系是什么？

### 本文件不负责

- Agent Runtime 实现 → 属于平台/基础设施层
- Multi-Agent 调度器 → 属于未来平台能力
- MCP / Skills 的安装和配置 → 属于 Level 2 Protected Action
- 具体 Agent 的模型选择 → 模型属于执行配置，不是永久规则
- Claude Code Subagent 调用规则的历史来源 → legacy source repository 中的 `03-CLAUDE/CLAUDE_MASTER.md` §24；当前 Plugin Runtime 以 active Skills 与 repo-local policies 为准。
- AI Agent Collaboration Standard 的完整实现 → 本文件是治理标准，不是 Runtime

### 与其他文件的关系

| 文件 | 关系 |
|------|------|
| `HLH_AI_Workflow.md` | 定义 Agent 工作流概念（Product → Architect → Coding → Review） |
| `CLAUDE_MASTER.md` §24 | 定义 Subagents 使用规则（操作层面） |
| `permission-policy.md` | 定义 Protected Actions 边界（权限层面） |
| **本文件** | 定义 Agent 角色模型、写权限、交接规则（治理层面） |

---

## 2. 核心原则

### 2.1 Model ≠ Role ≠ Permission

| 概念 | 含义 | 示例 |
|------|------|------|
| **Model** | 执行 Agent 的 AI 模型 | Claude Code + DeepSeek v4 Pro, Codex + GPT-5.6 Sol |
| **Role** | Agent 在生命周期中的角色和职责 | Architect, Builder, Auditor |
| **Permission** | Agent 被允许执行的操作边界 | Read-only, File Construction, Protected Action |

**关键规则：**

- **Role 决定 Authority（权限）。**
- **Model 决定 Capability（能力）。**
- **Capability 不自动赋予 Permission。**
- **Model 与 Role 之间没有永久绑定。** Claude Code 可以是 Builder 也可以是 Auditor。Codex 可以是 Architect 也可以是 Builder。
- **Model 分配是执行配置，不是永久规则。**

```
Model (Claude Code)
    → Capability: 可以写文件、分析代码
    → 不自动 = Permission

Role (Builder)
    → Authority: 在授权范围内修改文件
    → 需要 + Permission (Write Authority granted)

Permission (Write Authority)
    → 由用户授权，不由 Model 或 Role 自动获得
```

### 2.2 Capability ≠ Permission

本文件继承并扩展 Phase 4 的 Capability ≠ Permission 原则：

| Layer | 文件 | 职责 |
|-------|------|------|
| **Capability** | Phase 4 Capability Selection Layer | "Agent 能做什么" |
| **Role** | 本文件 §3-4 | "Agent 的角色职责" |
| **Permission** | `permission-policy.md` | "Agent 被允许做什么" |

---

## 3. Lifecycle Role Model

### 3.1 Role 定义

Lifecycle Role 决定 Agent 在工程生命周期中的**权限级别和职责范围**。

| Role | 默认权限 | 职责 | 禁止 |
|------|----------|------|------|
| **Architect** | Read-only | Architecture Review, Boundary Design, Risk Analysis, Decision Support | 修改仓库、直接实施、越权修复 |
| **Builder** | Write Authority (authorized scope only) | Authorized Implementation, File Construction, Authorized Testing, Fix Execution | 自行扩大范围、修改冻结架构、自我承担最终 Audit |
| **Auditor** | Read-only | Final Review, Consistency Validation, Governance Validation | 直接修复、自动推进 Phase |

### 3.2 Role 分配规则

| # | 规则 |
|---|------|
| 1 | 每个 Work Package 只能有一个 Builder Agent |
| 2 | Architect 和 Auditor 默认是 Read-only |
| 3 | 同一个 Agent 不能同时承担 Builder 和 Auditor 角色 |
| 4 | 同一个 Agent 可以在不同 Work Package 中承担不同角色 |
| 5 | Role 由用户在授权时指定，不由 Agent 自行选择 |
| 6 | Agent 不得自行切换 Lifecycle Role |

### 3.3 Role 与 Work Package 的关系

```
Phase Start
    ↓
Architect (Read-only)
    → Architecture Review, Boundary Design
    → 产出：Architecture Decision, Scope Definition
    ↓
Builder (Write Authority)
    → Authorized Implementation
    → 产出：Modified Files
    ↓
Auditor (Read-only)
    → Final Review, Consistency Validation
    → 产出：Review Report, Recommendation
    ↓
Phase Complete
```

---

## 4. Specialty Role Model

### 4.1 Role 定义

Specialty Role 决定 Agent 的**专业领域**，不决定权限级别。

| Role | 专业领域 | 典型任务 |
|------|----------|----------|
| **Product** | 产品策略、商业验证 | Product requirements, business validation |
| **Architecture** | 系统设计、技术决策 | Architecture design, technology selection |
| **Coding** | 代码实现、文件建设 | Implementation, file construction, code generation |
| **Testing** | 测试策略、质量保证 | Test design, test execution, quality review |
| **Security** | 安全审查、风险评估 | Security audit, vulnerability assessment |
| **Deployment** | 部署、发布管理 | Deployment planning, release management |
| **Monitoring** | 运行监控、问题诊断 | Runtime monitoring, incident response |
| **Review** | 代码审查、交付审查 | Code review, delivery review |

### 4.2 Lifecycle Role × Specialty Role

|  | Architect (Lifecycle) | Builder (Lifecycle) | Auditor (Lifecycle) |
|--|----------------------|---------------------|---------------------|
| **Product** | Product architecture review | — | Product requirement validation |
| **Architecture** | System design (primary) | Architecture implementation | Architecture compliance audit |
| **Coding** | Code architecture review | Implementation (primary) | Code quality audit |
| **Testing** | Test strategy design | Test execution | Test coverage audit |
| **Security** | Security boundary design | — | Security compliance audit |
| **Deployment** | Deployment architecture | Deployment configuration | Deployment readiness audit |
| **Monitoring** | Monitoring design | Monitoring setup | Monitoring coverage audit |
| **Review** | — | — | Final delivery review |

**关键规则：**

- Lifecycle Role 决定"可以做什么级别的操作"
- Specialty Role 决定"在哪个领域执行"
- **Lifecycle Role 不能替代 Specialty Role。** "我是 Builder，所以我可以做 Security Review" — 这是错误的
- **Specialty Role 不能赋予 Write Authority。** "我是 Coding Specialist，所以我可以修改代码" — Coding 是 Specialty；Write Authority 需要 Builder Lifecycle Role + 用户授权

---

## 5. Single Write Authority

### 5.1 规则

同一个 Repository、同一个 Work Package、同一个时间窗口内，**只能存在一个拥有写权限的 Builder Agent**。

### 5.2 Write Authority 覆盖范围

| 操作 | 需要 Write Authority |
|------|---------------------|
| 修改已有文件 | ✅ |
| 创建新文件 | ✅ |
| 删除文件 | ✅ |
| 移动/重命名文件 | ✅ |
| 生成并写入文件 | ✅ |
| Git add / commit | ❌ (Level 2 Protected Action) |
| Git push | ❌ (Level 2 Protected Action) |

### 5.3 Write Authority 生命周期

```
Write Authority Granted (用户授权)
    ↓
Builder Agent 执行 Authorized Modifications
    ↓
Work Package Complete / Suspended
    ↓
Write Authority Released
    ↓
Git State Captured (git status --short)
    ↓
State Record Updated
    ↓
Handoff Summary Generated
    ↓
Write Authority 归还给用户
```

### 5.4 违规处理

| 违规 | 处理 |
|------|------|
| Builder 超出授权范围修改 | STOP — 报告越权修改 |
| 多个 Agent 同时修改 | STOP — 识别冲突，由用户决定 |
| Builder 自行 commit | STOP — commit 属于 Level 2，Buildder 无此权限 |

---

## 6. Handoff Gate

### 6.1 定义

Handoff Gate 是 Agent 之间安全交接工作上下文的标准流程。

### 6.2 标准流程

```
Work Package Closed / Suspended
    ↓
(1) Write Authority Released
    → Builder 确认不再修改文件
    ↓
(2) Git State Captured
    → git rev-parse HEAD
    → git status --short
    → git log -1 --oneline
    ↓
(3) State Record
    → 记录当前：HEAD, branch, working tree, staged, untracked
    ↓
(4) Handoff Summary
    → 已完成的工作
    → 未完成的工作
    → 已知风险
    → 下一步建议
    ↓
(5) Incoming Agent Validation
    → Incoming Agent 验证 Git 状态与 Handoff Summary 一致
    → 确认角色和权限边界
    ↓
(6) Authorization Check
    → 用户明确授权新 Agent 的 Role 和 Scope
    ↓
(7) New Agent Start
    → 新 Agent 以完整上下文启动
```

### 6.3 Clean Handoff vs Controlled Dirty Handoff

| 类型 | 条件 | 允许的操作 |
|------|------|-----------|
| **Clean Handoff** | Working tree clean, all work committed | 直接交接，新 Agent 从 clean state 开始 |
| **Controlled Dirty Handoff** | Working tree 有未提交的修改（授权范围内） | Handoff Summary 必须列出所有 uncommitted changes；新 Agent 验证后再继续 |

**Dirty Handoff 必填记录（每项变更）：**

| # | 字段 | 说明 |
|---|------|------|
| 1 | **File** | 文件路径 |
| 2 | **Git Status** | modified / staged / untracked / deleted |
| 3 | **Owner** | 变更来源（见下方 Owner 分类） |
| 4 | **Work Package** | 产生此变更的 Work Package ID |
| 5 | **Reason** | 为什么未 commit（例如：等待 Review / 等待下一阶段 / 需要用户确认） |
| 6 | **Action** | 建议新 Agent 如何处理（继续 / 审查 / 回滚 / 丢弃） |

**Owner 分类：**

| Owner | 说明 |
|-------|------|
| **Builder Agent output** | Builder Agent 在授权范围内产生的修改 |
| **User-owned change** | 用户手动修改的文件 |
| **Other identified source** | 其他已知来源（需在 Reason 中说明） |
| **Unknown** | 无法确定变更来源 — **必须触发 STOP** |

**关键规则：**

- **Staged ≠ Clean。** staged 文件必须在 Handoff Summary 中显式列出
- **Dirty Handoff 必须记录原因。** 为什么没有 commit？哪些文件未提交？
- **Dirty Handoff 中的 uncommitted 修改只能由新 Builder Agent 或用户处理。** Auditor 和 Architect 不能处理 dirty state
- **Owner = Unknown 必须 STOP。** 不得交接来源不明的修改

### 6.4 Handoff Summary 最小内容

| # | 字段 | 说明 |
|---|------|------|
| 1 | Work Package ID | 完成的工作包标识 |
| 2 | Current HEAD | git rev-parse HEAD |
| 3 | Branch | git branch --show-current |
| 4 | Working Tree State | clean / dirty (list uncommitted files) |
| 5 | Completed Work | 已完成的工作清单 |
| 6 | Incomplete Work | 未完成的工作和原因 |
| 7 | Known Risks | 已知风险和未解决问题 |
| 8 | Outgoing Agent Role | 交接方 Agent 的 Lifecycle Role |
| 9 | Incoming Agent Expected Role | 建议的接收方 Lifecycle Role |
| 10 | Next Step Recommendation | 建议的下一步操作 |

---

## 7. Role Transition Rules

### 7.0 角色转换四元组（所有转换必须确认）

**所有 Lifecycle Role 转换必须重新声明以下四元组。禁止 Role 名称自动推导 Permission。**

| # | 字段 | 说明 | 示例（Builder） | 示例（Auditor） |
|---|------|------|-----------------|-----------------|
| 1 | **Role** | 新的 Lifecycle Role | Builder | Auditor |
| 2 | **Scope** | 授权修改的文件/目录范围 | legacy source repository 中的 `01-Standards/`, `03-CLAUDE/`（历史示例） | Read-only over all project files |
| 3 | **Permission** | 权限级别 | Write Authority (scope-limited) | Read-only |
| 4 | **Authorization** | 授权来源 | User-authorized Phase 5B Implementation Prompt | User-authorized Phase 5C Governance Validation |

**规则：**

- **Role 名称不自动推导 Permission。** "我是 Builder"不是写权限的来源——用户授权才是
- **Permission 不由上一个 Role 继承。** Architect 的 Read-only 不意味着下一个 Builder 也是 Read-only
- **Scope 必须明确到文件/目录级别。** 不能是 "project scope" 这种模糊描述
- **Authorization 必须引用具体的授权文档或 Prompt。** 不能是 "之前授权过"

### 7.1 允许的转换

| 从 | 到 | 条件 |
|----|-----|------|
| Architect | Builder | 不同 Work Package，需用户重新授权 Role |
| Builder | Auditor | Write Authority 已释放，Working tree 状态已记录 |
| Auditor | Architect | 不同 Work Package，需用户重新授权 Role |
| Architect | Auditor | 直接允许（均为 Read-only） |

### 7.2 禁止的转换

| 从 | 到 | 原因 |
|----|-----|------|
| Builder | Builder (同 WP) | 违反 Single Write Authority |
| Builder | Auditor (同 WP) | 违反"不能自我 Audit"原则 |
| Auditor | Builder (同 WP) | Auditor 已看到审查结果，不能回头修改 |

### 7.3 同一 Agent 的角色切换

同一个 AI Agent（如 Claude Code）可以在不同 Work Package 中承担不同角色：

```
WP-A: Claude Code = Architect (Read-only)
    ↓ Handoff Gate
WP-B: Claude Code = Builder (Write Authority)
    ↓ Handoff Gate
WP-C: Claude Code = Auditor (Read-only)
```

**每次切换必须经过 Handoff Gate + 用户重新授权 Role。**

---

## 8. Exception Handling

### 8.1 Scope Creep（范围蔓延）

| 情况 | 处理 |
|------|------|
| Builder 发现需要修改授权范围外的文件 | STOP — 报告用户，等待范围扩展授权 |
| Builder 发现冻结决策需要修改 | STOP — Builder 不能修改冻结架构 |
| Architect 发现设计缺陷 | 记录为 Finding，建议修正，不直接修改 |

### 8.2 Ambiguous Authority（权限模糊）

| 情况 | 处理 |
|------|------|
| 不确定某个操作是否需要 Write Authority | STOP — 假设需要，向用户确认 |
| 不确定当前 Role 是否允许某个操作 | STOP — 假设不允许，向用户确认 |
| Handoff Summary 与实际 Git 状态不一致 | STOP — 由用户决定如何处理差异 |

### 8.3 Failed Handoff（交接失败）

| 情况 | 处理 |
|------|------|
| Working tree dirty 但 Handoff Summary 不完整 | STOP — 补全 Summary 后再交接 |
| Incoming Agent 发现未记录的修改 | STOP — 由原 Builder Agent 或用户处理 |
| Git 状态与 Handoff Summary 描述的 HEAD 不一致 | STOP — 可能发生了并发修改 |

---

## 9. Stop Conditions

以下情况 Agent 必须立即 STOP：

| # | 条件 | 触发角色 |
|---|------|----------|
| 1 | 任务需要超出授权范围的文件修改 | Builder |
| 2 | 任务需要修改冻结的架构决策 | Builder |
| 3 | 任务需要执行 Level 2 Protected Action | Any |
| 4 | 发现多个 Agent 同时拥有 Write Authority | Any |
| 5 | Git baseline 与预期不一致 | Any |
| 6 | Handoff Summary 与 Git 状态不一致 | Incoming Agent |
| 7 | 权限边界不明确 | Any |
| 8 | 发现未记录的 dirty working tree | Auditor |
| 9 | 被要求自行切换 Lifecycle Role | Any |
| 10 | 被要求同时承担 Builder + Auditor | Any |

---

## 10. 与现有治理体系的关系

### 10.1 继承链

```
HLH_AI_Workflow.md（最高原则）
    ↓
Agent_Collaboration_Standard.md（本文件 — Agent 协作治理）
    ↓
CLAUDE_MASTER.md（Claude Code 行为规则 — 操作层面）
    ↓
permission-policy.md（权限边界 — 执行层面）
```

### 10.2 规则优先级

| 冲突场景 | 优先级 |
|----------|--------|
| 本文件 vs CLAUDE_MASTER.md | 本文件 §3-7（Role/HWTO/Gate）优先 |
| 本文件 vs permission-policy.md | permission-policy.md（Protected Actions）优先 |
| 本文件 vs Phase 执行 Prompt | 两者均有效，更严格的规则优先 |
| 无法判断哪个更严格 | STOP，询问用户 |

### 10.3 对已有文件的补充

| 已有规则 | 本文件的补充 |
|----------|-------------|
| `CLAUDE_MASTER.md` §24 Subagents | 本文件 §3-4 定义 Role 模型（Subagents 规则的上层治理） |
| `HLH_AI_Workflow.md` Agent 流程 | 本文件 §6 定义 Handoff Gate（流程间的交接标准） |
| Phase 4 Capability ≠ Permission | 本文件 §2.2 扩展为 Model ≠ Role ≠ Permission |
| DL-045 Future AI Agent Collaboration Standard | **本文件实现了 DL-045 记录的 Future Governance Enhancement** |

---

## 11. 禁止事项

| # | 禁止事项 | 原因 |
|---|----------|------|
| 1 | 禁止永久绑定 Model 与 Role | Model 是执行配置，不是永久规则 |
| 2 | 禁止 Agent 自行切换 Lifecycle Role | Role 由用户授权指定 |
| 3 | 禁止同一 Agent 同时承担 Builder + Auditor | 违反职责分离原则 |
| 4 | 禁止 Builder 自行扩大授权范围 | 违反 Single Write Authority |
| 5 | 禁止跳过 Handoff Gate 直接交接 | 交接必须走完整流程 |
| 6 | 禁止 staged = clean | staged 文件必须在 Handoff Summary 中显式列出 |
| 7 | 禁止 Architect/Auditor 修改仓库 | Architect 和 Auditor 是 Read-only |
| 8 | 禁止用 Specialty Role 替代 Lifecycle Role | Coding Specialist ≠ Builder |
| 9 | 禁止 Model Capability 自动赋予 Permission | Capability ≠ Permission |

## 12. v3.2 Agent Runtime Evidence 与按需独立审计

### 12.1 Agent Runtime Evidence

当 Agent 的运行时配置可能影响任务判断、验证结果或交接时，应记录实际运行配置，而不是只记录请求配置：

| 字段 | 要求 |
|---|---|
| Requested Model | 用户或任务请求的模型；未知时标记为未提供 |
| Actual Model | 实际执行模型；无法确认时标记为 INCONCLUSIVE |
| Requested Reasoning | 请求的推理级别；未知时标记为未提供 |
| Actual Reasoning | 实际推理级别；无法确认时标记为 INCONCLUSIVE |
| Requested Capability | 请求使用的工具、Skill、Hook 或其他能力 |
| Actual Runtime Capability | 实际可用并被使用的能力 |

这些字段是运行时证据，不得固化为 Role 与具体 Model 的永久绑定，也不得将 Capability 当作 Permission。

### 12.2 Self-Verify 与 Independent Audit

每个 Work Package 都必须完成 Self-Verify，并记录范围、结果、未完成项和证据限制。

是否需要 Independent Audit，不对每个 Work Package 一律强制，而由以下因素决定：

1. 风险等级；
2. 证据复杂度和可复现性；
3. 是否涉及 Protected Action、外部副作用或跨边界变更；
4. 用户、阶段或治理规则的明确要求。

触发 Independent Audit 时，Auditor 必须与 Builder 独立，默认只读，不审查自己实施的 Work Package。未触发时，Completion Decision 仍必须基于 Self-Verify 和适用证据要求，不得仅凭 Builder 的口头结论。

---

*Agent Collaboration Standard — HLH AI Software Engineering Workflow v3.2 WP-1*
