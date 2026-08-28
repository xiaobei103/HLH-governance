# Git_Standard.md：HLH AI 软件工程版本管理标准

> 本文件定义 HLH AI Software Engineering Workflow v3.0 的 Git 版本管理标准。
>
> **所有正式项目必须使用 Git。**
>
> **所有重要变更必须可追踪、可回滚、可审查。**
>
> **Claude Code 不得绕过 Git 直接进行不可追踪的修改。**

---

## 1. 文档定位

本文件是 `01-Standards/` 下的 Git 版本管理标准。

### 本文件回答的问题

- 什么项目必须使用 Git？
- 项目什么时候初始化 Git？怎么初始化？
- 当前体系本体如何管理 Git？
- 新项目应该独立 Git 仓库，还是纳入父级仓库？
- Commit 应该怎么写？message 什么格式？
- 分支应该怎么用？什么时候建分支？什么时候合？
- Tag 什么时候使用？什么格式？
- 远程仓库什么时候连接？GitHub / Gitee / GitLab 如何选择？
- Claude Code 修改文件前后如何使用 Git？
- 如何防止提交密钥、客户数据、数据库文件？
- 出问题时如何回滚？

### 本文件不负责

- 具体代码实现 → `Coding_Workflow.md`
- 具体部署流程 → `Delivery_Standard.md`
- 数据库迁移细节 → `Database_Standard.md`
- CI/CD 细节 → `Delivery_Standard.md`
- 商业交付验收细节 → `Business_Workflow.md`、`Delivery_Standard.md`
- Claude Code 总行为规则 → `CLAUDE_MASTER.md`

---

## 2. Git 总原则

### 2.1 所有正式项目必须使用 Git

没有 Git 的项目不是正式项目，是草稿。Demo、Prototype、MVP、商用项目都必须有 Git。学习研究项目也建议使用 Git 记录过程。

### 2.2 所有重要修改必须 commit

任何修改了代码、配置、文档、模板、标准、规则的操作，都应该形成 commit。不攒一大堆修改再一次性提交。

### 2.3 每个 commit 只做一类变更

功能是功能，修复是修复，文档是文档，格式是格式。一个 commit 里同时出现 `feat` 和 `refactor` 和 `chore` 说明 commit 太粗。

### 2.4 Commit message 必须清晰说明目的

让人（和 6 个月后的自己）能一眼看出这个 commit 做了什么、为什么做。`update`、`fix`、`change` 这种信息等于没写。

### 2.5 不允许把无关修改混进同一个 commit

修了一个 Bug 顺手改了 5 个文件的格式——请分成两个 commit。如果在 commit 前发现混入了无关修改，先拆分再提交。

### 2.6 不允许提交密钥、真实 .env、客户隐私数据

这是不可协商的硬规则。`.env` 必须在 `.gitignore` 中。`API Key`、`Token`、密码、用户手机号、医疗信息、财务数据——一律不得进入 Git 历史。

### 2.7 不允许未经确认 push 远程仓库

Push 是 P3 操作。必须用户明确授权、每次单独确认。Claude Code 不得自动 push。

### 2.8 不允许未经确认改写历史

`reset --hard`、`rebase`、`push --force`、删除分支/tag——这些操作可能造成不可逆的历史丢失。必须用户明确授权。

### 2.9 不允许把备份当成 Git 的替代品

把代码复制到 `backups/` 文件夹不是版本管理。Git 是唯一正式的版本管理手段。备份可以辅助，但不能替代。

### 2.10 Claude Code 每次任务开始和结束都必须检查 git status

开始前确认工作树干净，结束后确认变更已提交。这是所有正式交付的硬性步骤。

---

## 3. 仓库类型选择

HLH 体系中存在三类 Git 管理方式，按场景选择。

### 3.1 体系本体仓库

**适用：** HLH AI Software Engineering Workflow v3.0 本体

**当前策略：**
- 整个 Workflow 根目录作为一个 Git 仓库
- 分支使用 `main`
- 所有 Workflow / Standards / CLAUDE / Templates / Prompts / Skills / MCP / Docs / Testing / Logs 等变更都进入该仓库
- 早期不急于连接远程仓库
- Push 必须人工确认

**适合内容：** 规范、模板、配置、文档、学习笔记——所有非业务代码的工程体系资产。

### 3.2 独立项目仓库

**适用：** AI Operating System、商业项目、求职作品集项目、长期维护项目、未来可能上传 GitHub/Gitee/GitLab 的项目

**策略：**
- 项目从模板复制到 `07-Projects/` 后，独立初始化 Git
- 项目有自己的 `.gitignore`、`README.md`、`CLAUDE.md`、`CHANGELOG.md`
- 项目 commit 与 Workflow 本体分离

**适用原因：**
- 方便单独展示（求职、客户演示）
- 方便单独部署
- 方便客户交付
- 避免体系仓库过大，混杂业务代码

### 3.3 父级仓库纳入管理

**适用：** 小型模板、文档体系、尚未正式立项的原型、早期实验

**策略：**
- 可先由 Workflow 本体仓库管理
- 一旦项目进入正式开发（立项、有明确边界），应评估是否拆成独立仓库

### 仓库选择规则

1. **正式长期项目优先独立仓库。** 独立仓库 = 独立的 Git 历史 = 独立的展示和交付能力。
2. **Workflow 本体不应长期塞入大量业务代码。** 本体是管理工程体系的，不是存项目的。
3. **学习实验不应污染正式项目仓库。** 学习和实验的内容放在 `99-Learning/` 或独立目录。
4. **不允许随意嵌套 Git 仓库。** 如确需嵌套（如 git submodule），必须在 README 或 Decision Log 中说明原因。
5. **如果出现嵌套 Git，必须记录。** 为什么嵌套、如何管理、如何更新。

---

## 4. Git 初始化规则

项目初始化 Git 前，必须确认以下 10 项：

| # | 确认项 | 为什么重要 |
|---|--------|------------|
| 1 | 项目名称 | 确定仓库的合理名称 |
| 2 | 项目类型 | 决定 Git 策略（独立/纳入） |
| 3 | 是否正式项目 | 正式项目 = 必须独立考虑 Git |
| 4 | 是否需要独立仓库 | 避免后期拆分麻烦 |
| 5 | 是否需要未来上传远程 | 影响公开/私有决策 |
| 6 | 是否包含敏感数据 | 必须先清理再 init |
| 7 | 是否已有 .gitignore | 没有 .gitignore 不 init |
| 8 | 是否已有 README.md | 第一 commit 应包含 README |
| 9 | 是否已有 CLAUDE.md | 正式项目必须有 |
| 10 | 是否已有 CHANGELOG.md | 建议第一次 commit 就创建空的 |

### 标准初始化流程

```
检查目录（确认在正确的项目根目录）
    ↓
确认是否需要独立仓库（独立 vs 纳入父级）
    ↓
创建 .gitignore（必须先创建，再 init）
    ↓
检查 secrets 和敏感文件（确认没有 .env、密钥、客户数据）
    ↓
执行 git init
    ↓
执行 git status（确认只包含该包含的文件）
    ↓
执行 git add .
    ↓
执行第一次 commit
    ↓
确认工作树干净
```

### 第一次 commit 推荐格式

**通用项目：**
```bash
git commit -m "chore: initialize project"
```

**Workflow 本体：**
```bash
git commit -m "chore: initialize HLH AI software engineering workflow"
```

### 初始化禁止

- 不允许没有 `.gitignore` 就 `git init` 正式项目
- 不允许把真实 `.env` 加入第一次 commit
- 不允许把数据库真实数据文件加入第一次 commit
- 不允许把客户数据加入第一次 commit
- 不允许把 `node_modules/` 加入 Git

---

## 5. 分支策略

### 5.1 当前个人阶段默认策略（Phase 1）

**当前推荐：** `main` 单分支 + 小步 commit

- 小型文档修改可直接在 `main` commit
- 小型 MVP 可直接在 `main` 频繁 commit
- 不急于引入复杂分支模型

**理由：** 当前主要是个人开发，过度分支会增加操作复杂度、降低 commit 频率。重点是保持小步 commit 和可回滚，而不是分支模型看起来专业。

### 5.2 正式项目阶段策略

当项目进入正式开发（多人协作 / 高风险修改 / 商业交付），推荐以下分支模型：

| 分支 | 用途 | 何时使用 |
|------|------|----------|
| `main` | 稳定版本 | 始终保持可运行、可交付 |
| `dev` | 开发整合分支（可选） | 多个 feature 需要整合时 |
| `feature/xxx` | 功能分支 | 多文件功能开发 |
| `fix/xxx` | 修复分支 | Bug 修复，特别是高风险修复 |
| `docs/xxx` | 文档分支 | 大规模文档重构 |
| `refactor/xxx` | 重构分支 | 超过 3 个文件的重构 |
| `release/x.y.z` | 发布分支（可选） | 正式发布前的冻结和测试 |

**使用场景：**
- 多文件功能开发 → `feature/`
- 数据库变更 → 必须独立分支
- 权限系统修改 → 必须独立分支
- 部署配置修改 → 必须独立分支
- 商业交付版本 → `release/`
- 多人协作 → `feature/` + `dev`

### 5.3 分支命名规则

```
feature/add-user-login
feature/customer-import-export
fix/customer-search-focus-loss
fix/login-token-refresh-race
docs/update-delivery-standard
docs/restructure-api-documentation
refactor/split-customer-service
refactor/extract-shared-validation
test/add-playwright-customer-flow
test/increase-service-coverage
release/v1.0.0
release/v1.1.0-beta
```

### 分支操作规则

1. **分支名称必须表达目的。** 不使用 `test`、`new`、`abc`、`temp` 等无意义名称。
2. **高风险任务必须考虑独立分支。** 数据库变更、权限变更、批量重构——这些改了很难回滚的操作，先在分支上做。
3. **未完成分支不得随意合并 `main`。** 合并前必须确认功能完成、Build 通过、Test 通过。
4. **分支合并前必须检查 Build / Test。** 不通过不合并。
5. **废弃分支应及时清理。** 合并后删除已合入的功能分支，保持分支列表整洁。

---

## 6. Commit 规范

### 6.1 Commit Message 格式

```
<type>: <short description>
```

### 6.2 Commit Type 清单

| Type | 用途 | 示例 |
|------|------|------|
| `feat` | 新增功能 | `feat: add user login with JWT authentication` |
| `fix` | 修复 Bug | `fix: resolve token refresh race condition` |
| `docs` | 文档修改 | `docs: define technology stack standard` |
| `chore` | 工程杂项、初始化、配置 | `chore: add .gitignore and .env.example` |
| `refactor` | 代码重构（不改变功能） | `refactor: extract shared validation logic` |
| `test` | 测试相关 | `test: add customer API regression tests` |
| `style` | 样式或格式修改 | `style: unify button border-radius tokens` |
| `build` | 构建相关 | `build: update Vite config for production` |
| `ci` | CI/CD 相关 | `ci: add GitHub Actions test workflow` |
| `perf` | 性能优化 | `perf: optimize customer list query with index` |
| `security` | 安全修复 | `security: prevent .env exposure via build output` |

### 6.3 Commit 内容规则

每个 commit 应该：
1. 只做一类变更（功能是功能，格式是格式）
2. 修改范围清晰（从 commit message 和 diff 即可判断影响面）
3. 可以独立回滚（不依赖"先 revert 后面 3 个 commit 再 revert 这个"）
4. 不混入无关格式化（格式调整独立 commit）
5. 不混入调试代码（`console.log`、注释掉的代码、`// TODO test`）
6. 不包含 secrets
7. 不包含客户隐私数据
8. 不包含数据库真实数据文件

### Commit 禁止

- ❌ 一个 commit 同时改功能、格式、依赖、文档、数据库——必拆
- ❌ commit message 写 `update`、`fix bug`、`change files`、`wip`——等于没写
- ❌ 未检查 `git diff` 就 commit
- ❌ 让 Claude Code 自己乱取含糊的 commit message
- ❌ 把"我改了"当 commit message

---

## 7. Claude Code 使用 Git 的规则

Claude Code 是本体系的核心编码工具，其 Git 行为必须严格约束。

### 7.1 任务开始前

**必须执行：**
```bash
git status
```

**目的：**
- 确认工作树是否干净
- 确认是否有用户未提交的改动
- 防止 Claude Code 的修改覆盖用户的工作

**如果存在未提交变更：**
1. 列出所有未提交文件
2. 询问用户这些改动是否属于当前任务
3. 不得擅自覆盖用户的未提交改动
4. 不得把用户的未提交改动悄无声息混入本次 commit

### 7.2 修改过程中

Claude Code 必须：
1. 只修改任务范围内文件
2. 不做无关重构
3. 不做无关格式化
4. 不删除用户的未提交改动
5. 如果影响范围扩大，必须停止并询问

### 7.3 Commit 前

**必须执行：**
```bash
git diff
git status
```

**必须确认：**
- 修改文件是否符合任务范围
- 是否有无关文件被意外修改
- 是否有 secrets（搜索 `API_KEY`、`SECRET`、`TOKEN`、`PASSWORD` 等关键词）
- 是否有真实 `.env`
- 是否有客户数据
- 是否有数据库真实文件
- 是否需要更新 README
- 是否需要更新 CHANGELOG

### 7.4 Commit 后

**必须输出：**
1. `commit hash`
2. `commit message`
3. 修改文件列表
4. 当前 `git status`（确认干净）
5. 回滚方式（`git revert <hash>`）

### Claude Code Git 禁止事项

Claude Code 不得：
- 未经确认 `git push`
- 未经确认 `git reset --hard`
- 未经确认 `git rebase`
- 未经确认改写历史
- 未经确认创建远程仓库
- 未经确认删除分支
- 未经确认删除 tag
- 自作主张拆分或合并 commit
- 执行 `git push --force` 及其任何等效操作

---

## 8. .gitignore 标准

所有正式项目必须在第一次 commit 前创建 `.gitignore`。

### 必须忽略（所有项目通用）

```gitignore
# Dependencies
node_modules/

# Build output
dist/
build/
.next/
out/

# Test coverage
coverage/

# Cache
.cache/
*.tsbuildinfo

# Environment files (REAL secrets)
.env
.env.local
.env.*.local

# Logs
*.log
logs/*.log

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/.history/
.idea/
*.swp
*.swo
*~
```

### 按需忽略（按项目类型添加）

```gitignore
# SQLite database files
data.db
*.sqlite
*.sqlite3

# User content
uploads/
exports/

# Backups and temp
backups/
tmp/
temp/

# Environment files (production)
.env.production
.env.development
```

### .gitignore 规则

- `.env.example` **应进入 Git**（模板，不含真实密钥）
- `.env` **不进入 Git**（含真实密钥）
- `logs/` 可保留 `.gitkeep`，但真实日志不进入 Git
- `backups/` 可保留说明文件，但真实备份一般不进入 Git
- SQLite 真实数据库文件默认不进入 Git，除非是明确的测试样例库且不包含真实数据
- 客户上传文件不进入 Git
- 导出文件不进入 Git，除非是脱敏示例
- 构建产物不进入 Git

---

## 9. 敏感信息与 Git

这是不可协商的安全底线。

### 禁止提交

| 类别 | 具体内容 |
|------|----------|
| 密钥文件 | `.env`、`*.pem`、`*.key`、`*.secret` |
| API 密钥 | `API_KEY`、`SECRET_KEY`、`ACCESS_TOKEN`、`REFRESH_TOKEN` |
| 密码 | `DATABASE_PASSWORD`、`JWT_SECRET`、`SMTP_PASSWORD` |
| 证书 | SSH Key、SSL 证书 |
| 客户数据 | 姓名、手机号、微信号、QQ 号、邮箱、地址 |
| 敏感信息 | 身份证号、医疗信息、财务数据、银行账号 |
| 私密内容 | 私聊记录、客户成交记录、未脱敏业务数据 |
| 数据文件 | 真实数据库文件、真实备份文件、生产配置 |

### 如果发现敏感信息已被提交

**必须立即执行以下步骤：**

1. **确认泄露范围。** 这个 commit 是本地还是已 push？有没有被 clone 或 fork？
2. **不继续追加 commit 掩盖。** 追加 commit 不能真正删除 Git 历史中的敏感数据。
3. **记录受影响 commit。** 哪些 commit 包含了敏感信息？
4. **评估是否需要清理历史。** 如果已 push 且仓库公开，必须清理。
5. **真实密钥必须作废并更换。** 一旦 push 到公开仓库，该密钥视为已泄露，必须立即更换。
6. **必要时使用安全工具清理历史。** 如 `git filter-branch` 或 `BFG Repo-Cleaner`。
7. **记录 Decision Log。** 什么泄露了、什么时候发现的、怎么处理的、如何防止再次发生。

> ⚠️ **注意：** 清理 Git 历史属于高风险操作，不得由 Claude Code 自动执行。

---

## 10. 远程仓库策略

### 10.1 当前阶段（Phase 1）

**默认策略：**
- 不急于创建远程仓库
- 不自动 push
- 不自动连接 GitHub / Gitee / GitLab
- 本地 Git 先稳定运行
- 核心规范完成后再决定远程策略

### 10.2 GitHub

**适用：** 学习项目、开源项目、求职作品集、海外生态展示、AI/Agent 技术展示

**注意：**
- 私有仓库优先用于未公开项目
- README 和演示材料要整理好再公开
- `.env` 和密钥绝对不能出现在公开仓库中
- 公开仓库的 commit 历史中不能有敏感信息

### 10.3 Gitee（码云）

**适用：** 国内访问便利、国内客户交付、国内展示备用、GitHub 镜像

**注意：**
- 适合作为国内备份或客户查看入口
- 规则与 GitHub 相同：不提交 secrets、不提交客户数据

### 10.4 GitLab

**适用：** 商业项目、企业协作、私有化部署、团队管理、后期 CI/CD

**注意：**
- 当前阶段先了解，不急于自建
- 自建 GitLab 需要服务器和维护成本

### 10.5 Push 规则

Push 之前必须逐条确认：

| # | 确认项 |
|---|--------|
| 1 | 远程仓库地址是什么 |
| 2 | 仓库是 public 还是 private |
| 3 | 是否包含 secrets |
| 4 | 是否包含客户数据 |
| 5 | README 是否适合公开 |
| 6 | Git 历史中是否有敏感信息 |
| 7 | 是否需要先清理历史 |
| 8 | 是否需要先创建远程仓库 |
| 9 | 是否需要设置 upstream |
| 10 | 用户是否已明确确认 push |

**禁止：**
- Claude Code 自动 push
- Claude Code 自动创建远程仓库
- Claude Code 自动将仓库设为 public
- Claude Code 自动 force push
- 未经检查直接 push 包含敏感信息的仓库

---

## 11. Tag 与版本规则

### 11.1 什么时候使用 Tag

| 场景 | Tag 格式示例 |
|------|-------------|
| v0.1 Prototype 完成 | `v0.1.0` |
| v0.2 MVP 完成 | `v0.2.0` |
| v0.3 Beta 完成 | `v0.3.0` |
| v1.0 Release 完成 | `v1.0.0` |
| 商业交付版本 | `v1.0.0-client-xxx` |
| 重要演示版本 | `v1.0.0-demo` |
| 简历作品集版本 | `v1.0.0-portfolio` |
| 重大稳定节点 | `v1.0.0`、`v2.0.0` |

### 11.2 Tag 前必须确认

| # | 确认项 |
|---|--------|
| 1 | 当前工作树干净 |
| 2 | Build 通过 |
| 3 | Test 通过或已说明风险 |
| 4 | README 已更新 |
| 5 | CHANGELOG 已更新 |
| 6 | 交付报告已完成 |
| 7 | 没有 secrets |
| 8 | 没有客户数据 |
| 9 | 版本号正确 |
| 10 | 用户已确认 |

### 11.3 禁止

- 未测试就 tag
- 未确认就 tag
- 商业交付版本没有 tag 或 commit 记录
- Tag 后继续修改同一版本却不更新版本号
- 未确认删除 tag
- Claude Code 自动创建或删除 tag

---

## 12. 回滚标准

### 12.1 文档或小修改回滚

**已提交内容回滚：**
```bash
git revert <commit-hash>
```

**未提交内容恢复：**
```bash
git restore <file>
```

**规则：**
- 优先使用 `git revert` 回滚已提交内容（保留完整历史）
- 未提交内容可用 `git restore`，但必须确认不会丢失用户的有意修改

### 12.2 功能回滚

回滚一个功能 commit 前必须确认：

1. 回滚哪个 commit
2. 是否影响后续 commit（依赖关系）
3. 是否影响数据库（功能可能改了 schema）
4. 是否影响配置
5. 是否影响部署
6. 是否需要更新 CHANGELOG

### 12.3 数据库相关回滚

数据库回滚必须遵守 `Database_Standard.md`。

**禁止：**
- 为了回滚 Git 直接删除数据库
- 为了修复直接清空数据表
- 没有备份就回滚真实数据
- Claude Code 自动执行生产数据库回滚

### 12.4 高风险 Git 操作权限

以下操作必须用户明确授权，Claude Code 不得自动执行：

| 操作 | 风险 | 权限 |
|------|------|------|
| `git reset --hard` | 不可逆丢失工作 | P3 |
| `git rebase` | 改写历史 | P3 |
| `git push --force` | 远程历史被覆盖 | P3 |
| 删除分支 | 可能丢失未合并代码 | P2 |
| 删除 tag | 版本标记丢失 | P2 |
| 清理 Git 历史 | 不可逆 | P3 |
| 修改远程仓库地址 | 影响协作 | P2 |

---

## 13. 大文件与二进制文件规则

### 默认不提交

| 类别 | 示例 |
|------|------|
| 媒体文件 | 视频文件（`.mp4`、`.mov`）、大型图片源文件（`.psd`、`.ai`） |
| 压缩包 | `.zip`、`.tar.gz`、`.rar` |
| 数据库 | `.db`、`.sqlite`、`.sqlite3`、`dump.sql` |
| 备份 | `backups/` 下的任何大文件 |
| 导出 | `exports/` 下的任何文件 |
| 依赖 | `node_modules/` |
| 构建产物 | `dist/`、`build/`、`.next/` |
| 安装包 | `.exe`、`.dmg`、`.pkg`、`.msi` |
| 日志 | `logs/` 下的任何日志文件 |

### 可以提交

- 小型示例图片（README 截图，建议 < 500KB）
- 脱敏样例数据（用于测试的假数据）
- 必要的配置模板
- `.env.example`
- `.gitkeep`（保留空目录结构）

### 如果必须管理大文件

1. 评估是否需要 Git LFS（Large File Storage）
2. 在 README 或 Decision Log 中说明原因
3. 不得直接把大量二进制文件 `git add .` 塞进仓库
4. 大文件变更频繁时考虑外部存储方案

---

## 14. CHANGELOG 与 Git 的关系

Git 是变更记录，CHANGELOG 是给人看的变更说明。两者互补，不可互替。

### CHANGELOG 应记录

- 新增功能（对应 `feat:` commits）
- 修复问题（对应 `fix:` commits）
- 破坏性变更（API 不兼容、数据库结构变更、配置方式改变）
- 数据库变更
- 配置变更
- 安全修复
- 交付版本号
- 已知问题

### 维护规则

1. **重要功能 commit 后应更新 CHANGELOG。** 不是每个 commit 都更新，但每个 `feat:` 和 `fix:` 原则上都应反映在 CHANGELOG 中。
2. **Release 前必须更新 CHANGELOG。** 这个版本做了什么，一条条写清楚。
3. **商业交付版本必须有 CHANGELOG。** 客户要知道你交付了什么。
4. **小型文档修改可不更新 CHANGELOG。** 如修改了一个 typo、调整了一句描述。
5. **CHANGELOG 不替代 Git，Git 也不替代 CHANGELOG。** 一个给机器看，一个给人看。

---

## 15. Git 与 Decision Log 的关系

以下 Git 相关的重大操作必须进入 Decision Log：

- 从父级仓库拆分为独立仓库
- 引入远程仓库（首次连接 GitHub/Gitee/GitLab）
- 将项目从 private 改为 public
- 清理 Git 历史（涉及敏感信息时）
- 删除重要分支
- 重大 tag 的创建（v1.0、商业交付）
- 仓库结构的重大调整
- Git 安全事故处理

### Decision Log 必须记录

- 日期
- 背景（为什么需要做这个操作）
- 可选方案
- 最终选择
- 选择理由
- 风险
- 后续复盘点

---

## 16. 多项目 Git 管理规则

HLH AI Software Engineering Workflow 会长期管理多个项目。以下规则防止仓库管理失控。

1. **Workflow 本体仓库只管理工程体系资产。** 规范、模板、配置、文档、学习笔记。
2. **正式业务项目应逐步独立仓库化。** 不长期塞在 Workflow 本体仓库中。
3. **`07-Projects/` 下项目进入正式开发前，必须决定 Git 策略。** 是独立初始化还是先纳入本体？决定后写在项目 CLAUDE.md 中。
4. **不允许多个正式项目长期混在一个仓库里。** 这不是"方便管理"，这是"不方便交付"。
5. **不允许复制项目后忘记处理 Git 历史。** 从模板复制出来的项目，如果模板目录内有 `.git/`，必须先处理（删除或重新 init）。
6. **不允许把客户项目和个人学习项目混在同一仓库。** 客户数据和个人实验绝对不能共存于一个 Git 仓库。
7. **不允许把客户数据提交到 Workflow 本体仓库。** 本体仓库不存储任何业务数据。
8. **项目归档时必须记录最后 commit 和状态。** `git log -1` 的结果写入归档文档。

---

## 17. Git 与 Claude Code 权限关系

Claude Code 的 Git 权限必须遵守 `permission-policy.md`。

| 操作 | 权限 | 说明 |
|------|------|------|
| `git status` | P0 | 可自动执行 |
| `git diff` | P0 | 可自动执行 |
| `git log --oneline` | P0 | 可自动执行 |
| `git add` | P1 | 需确认 |
| `git commit` | P1 | 需确认，message 必须清晰 |
| `git branch` | P1 | 需确认 |
| `git checkout / switch` | P1 | 需确认 |
| `git restore` | P1 | 需确认 |
| `git revert` | P1 | 需确认 |
| `git tag` | P2 | 需明确授权 |
| `git remote add` | P2 | 需明确授权 |
| `git pull` | P2 | 需明确授权 |
| `git push` | P3 | 禁止自动执行 |
| `git push --force` | P3 | 绝对禁止自动执行 |
| `git reset --hard` | P3 | 绝对禁止自动执行 |
| `git rebase` | P3 | 绝对禁止自动执行 |
| 删除分支 | P2 | 需明确授权 |
| 删除 tag | P2 | 需明确授权 |
| 清理历史 | P3 | 绝对禁止自动执行 |

### 核心要求

1. Claude Code **可以建议** Git 操作。
2. Claude Code **可以执行** 已授权的 P0/P1 Git 操作。
3. Claude Code **不拥有远程仓库最终控制权。** Push、创建仓库、公开仓库——这些权力永远属于人类用户。
4. **高风险 Git 操作（P2/P3）必须由用户单独、明确确认。** 一次授权只覆盖一次操作。
5. **所有 Git 操作必须写入交付报告。** Commit hash、message、回滚方式缺一不可。

---

## 18. Git 检查清单

### 18.1 任务开始前检查

- [ ] 当前目录是否正确（是否在项目根目录）
- [ ] 是否是 Git 仓库（`git status` 是否有输出）
- [ ] 当前分支是什么
- [ ] `git status` 是否干净
- [ ] 是否有用户未提交的改动
- [ ] 是否需要创建新分支
- [ ] 是否存在敏感文件风险（`.env` 是否存在、是否被 tracked）

### 18.2 Commit 前检查

- [ ] `git diff` 已逐文件检查
- [ ] 修改文件符合任务范围（没有不该改的文件）
- [ ] 没有无关格式化
- [ ] 没有 secrets（搜索了敏感关键词）
- [ ] 没有真实 `.env` 出现在 diff 中
- [ ] 没有客户数据
- [ ] 没有数据库真实文件
- [ ] Build / Test 已执行或已说明为何未执行
- [ ] README / CHANGELOG 已按需更新
- [ ] Commit message 清晰且符合规范

### 18.3 Push 前检查

- [ ] 用户已明确确认 push
- [ ] 远程仓库地址正确
- [ ] Public / Private 状态已确认
- [ ] 没有 secrets（再次确认）
- [ ] 没有客户数据
- [ ] README 适合公开（如果是 public 仓库）
- [ ] Git 历史中无敏感信息
- [ ] 分支正确（不是在错误分支上推送）
- [ ] Push 目的明确（为什么 push、push 到哪里）

---

## 19. 常见错误与处理

### 19.1 提交了不该提交的文件

**处理步骤：**
1. 立即停止当前操作。
2. 判断文件是否已经 push。
3. 如果未 push：删除不该提交的文件 → 重新 commit → 或使用 `git commit --amend`。
4. 如果已 push：评估泄露范围 → 密钥必须作废 → 必要时清理历史 → 记录安全事件。

### 19.2 Commit 混入了无关修改

**处理步骤：**
1. 未 push 时可拆分 commit（`git reset HEAD~1` 后重新分批 add 和 commit）。
2. 已 push 时谨慎处理，不要为"整洁"随意 rebase。
3. 记录原因，后续避免。

### 19.3 Claude Code 改错了文件

**处理步骤：**
1. 停止继续修改。
2. 查看 `git diff` 确认错误范围。
3. 判断是否可用 `git restore` 恢复。
4. 确认恢复操作不会覆盖用户的有意修改。
5. 回滚错误修改。
6. 重新限定修改范围后继续。

### 19.4 Build 失败但已经 commit

**处理步骤：**
1. 不得假装成功或在报告中隐瞒。
2. 新增一个 `fix:` commit 修复 Build 问题。
3. 或 `git revert` 问题 commit。
4. 交付报告必须说明失败情况和处理方式。

### 19.5 分支混乱

**处理步骤：**
1. 查看当前分支（`git branch`）。
2. 查看 `git status` 和 `git log`。
3. 不要立即 `reset` 或 `rebase`。
4. 先向用户输出当前情况和建议方案。
5. 等待用户确认后再操作。

---

## 20. 当前阶段默认策略

当前 HLH AI Software Engineering Workflow v3.0 处于 **Phase 1 — 规范搭建期**，Git 策略如下：

1. **Workflow 本体使用 `main` 分支。** 不引入复杂分支模型。
2. **Workflow 本体暂不 push 远程仓库。** 先本地稳定运行。
3. **每个标准文件独立 commit。** 一个文件一个 commit，message 清晰。
4. **每次 Claude Code 修改后必须输出 commit hash。** 这是交付报告的硬性要求。
5. **不使用复杂分支模型。** 当前单人开发，`main` + 小步 commit 足够。
6. **不使用 tag，直到核心 v0.1 规范完成。** 完成后打 `v0.1.0`。
7. **不把 `07-Projects/` 中未来正式项目长期混进本体仓库。** 进入正式开发前拆分。
8. **AI Operating System 启动时，应优先考虑独立仓库。** 它是第一个正式项目，应有独立的 Git 历史。
9. **求职作品集项目应整理后再上传 GitHub。** README、截图、演示视频准备好之后再 push。
10. **商业项目优先考虑私有仓库。** Push 前严格检查 secrets 和客户数据。

---

## 21. 禁止事项

| # | 禁止事项 | 原因 |
|---|----------|------|
| 1 | 禁止正式项目不用 Git | 没有 Git = 草稿，不是工程 |
| 2 | 禁止没有 .gitignore 就第一次 commit | 一旦提交了不该提交的文件，清理起来非常麻烦 |
| 3 | 禁止提交真实 .env | 密钥泄露，不可逆 |
| 4 | 禁止提交 API Key / Token / 密码 | 同上 |
| 5 | 禁止提交客户隐私数据 | 法律责任 + 职业道德 |
| 6 | 禁止提交真实数据库文件 | 数据泄露 + 仓库膨胀 |
| 7 | 禁止把 node_modules 提交进 Git | 仓库膨胀，依赖管理混乱 |
| 8 | 禁止一个 commit 混入多类变更 | 无法独立回滚，无法清晰追溯 |
| 9 | 禁止 commit message 写得含糊 | 6 个月后没人知道这个 commit 做了什么 |
| 10 | 禁止未经确认 push | P3 操作，必须用户亲自确认 |
| 11 | 禁止未经确认 force push | 远程历史被不可逆覆盖 |
| 12 | 禁止未经确认 reset --hard | 本地工作不可逆丢失 |
| 13 | 禁止未经确认 rebase | 历史被改写，难以追溯 |
| 14 | 禁止未经确认公开仓库 | 一旦公开，一切历史永久可查 |
| 15 | 禁止把备份当成 Git 的替代品 | 备份不能替代版本管理 |
| 16 | 禁止让 Claude Code 自动改写历史 | AI 不能执行不可逆的高风险 Git 操作 |

---

## 22. 与其他标准文件的关系

| 标准文件 | 与本文件的关系 |
|----------|----------------|
| `Tech_Stack_Standard.md` | 决定项目的技术栈，Git 管理技术栈的变更 |
| `Security_Standard.md` | 决定 secrets、权限、敏感数据的处理规则，Git 必须配合执行 |
| `Testing_Standard.md` | 决定 commit 前/merge 前的测试要求 |
| `Delivery_Standard.md` | 决定交付版本的 tag、CHANGELOG、commit 要求 |
| `Database_Standard.md` | 决定数据库变更时的 Git 分支策略和回滚方案 |
| `Dependency_Review_Standard.md` | 决定依赖变更是否允许，Git 记录依赖变更 |
| `Env_Secrets_Standard.md` | 决定 .env / .env.example 的管理方式 |
| `Logging_Monitoring_Standard.md` | 决定日志文件是否进入 Git |

本文件只定义版本管理规则。具体的安全策略、测试要求、数据库回滚、交付标准由对应文件补充。

---

## 23. 最终默认结论

1. **所有正式项目必须使用 Git。** Demo、Prototype、MVP、商用项目——无一例外。
2. **Workflow 本体当前使用 `main` 分支。** 单人开发阶段，小步 commit 优先于复杂分支模型。
3. **当前阶段不急于连接远程仓库。** 规范完善之后再决定 push 策略。
4. **小型个人阶段可以 `main` 单分支小步 commit。** 重点是 commit 质量和频率。
5. **正式项目和高风险任务应使用功能分支。** 数据库变更、权限变更、批量重构——在分支上做，验证后再合。
6. **每个 commit 必须清晰、独立、可回滚。** 做得到这三点才算合格。
7. **`.env`、密钥、客户数据、真实数据库不得进入 Git。** 这是不可协商的安全底线。
8. **Claude Code 每次任务开始和结束都必须检查 Git 状态。** 任务前确认干净，任务后确认已提交。
9. **Push、force push、reset --hard、rebase、tag、远程仓库操作都必须人工确认。** 这些不是 AI 可以自主决定的。
10. **Git 是工程安全底线，不是装饰品。** 没有 Git 的项目不要谈工程化。
