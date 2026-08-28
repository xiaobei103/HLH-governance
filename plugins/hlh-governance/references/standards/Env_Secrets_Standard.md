# Env_Secrets_Standard.md：HLH AI 软件工程环境变量与密钥管理标准

> 本文件定义 HLH AI Software Engineering Workflow v3.0 的环境变量与密钥管理标准。
>
> **所有正式项目必须区分 `.env.example` 与真实 `.env`。**
>
> **真实密钥不得进入 Git、Prompt、日志、交付报告或公开文档。**
>
> **Claude Code 默认不得读取、修改、提交真实密钥。**

---

## 1. 文档定位

本文件是 `01-Standards/` 下的环境变量与密钥管理标准。

### 本文件回答的问题

- 什么是环境变量？什么是密钥？
- `.env` 和 `.env.example` 有什么区别？各自什么规则？
- 哪些配置可以进入 Git？哪些绝对不能？
- Claude Code 是否可以读取真实 `.env`？
- 新增、修改、删除环境变量时应该怎么做？
- 数据库连接串如何管理？
- API Key 和 Token 如何管理？
- 前端和后端的环境变量规则有什么不同？
- 本地开发、测试环境、生产环境如何区分配置？
- 交付项目时如何处理密钥？
- 密钥泄露后如何处理？

### 本文件不负责

- 具体认证代码实现 → `Security_Standard.md`
- 具体部署脚本 → `Delivery_Standard.md`
- 具体数据库迁移 → `Database_Standard.md`
- 具体安全事件法律处理 → `Security_Standard.md`
- 依赖安全审查 → `Dependency_Review_Standard.md`
- 日志安全策略 → `Logging_Monitoring_Standard.md`

---

## 2. 总原则

### 2.1 真实密钥永不进入 Git

API Key、Token、密码、数据库连接串——任何能在 Git 历史中找到的密钥，都应视为已被泄露。`.gitignore` 中必须有 `.env`，提交前必须检查 `git diff`。

### 2.2 .env.example 可以进入 Git，但只能写占位符

`.env.example` 是给下一个接手项目的人看的说明书。它告诉别人"你需要配置这些变量"，但不告诉别人"真实值是什么"。占位符示例：`DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"`。

### 2.3 .env 默认不得被 Claude Code 读取

Claude Code 的上下文可能被日志、被存储、被分析。真实密钥不应进入 Claude Code 的上下文。Claude Code 默认只读取 `.env.example`。

### 2.4 API Key 不得写入源码

全局搜索 `API_KEY`、`SECRET`、`TOKEN`、`PASSWORD` 不应在源码中发现硬编码。所有密钥走环境变量。

### 2.5 Token 不得写入源码

JWT Secret、OAuth Secret、Access Token、Refresh Token——一律通过环境变量注入。

### 2.6 数据库密码不得写入源码

`DATABASE_URL` 完整连接串或拆分的 `DATABASE_PASSWORD` 都走环境变量。

### 2.7 生产配置不得写入公开文档

README、CHANGELOG、交付报告、公开 Wiki——任何可能被公开看到的文档中不得包含生产环境真实配置。

### 2.8 交付报告不得暴露密钥

报告中如需说明配置变更，引用变量名（如"新增了 `JWT_SECRET` 环境变量"），不引用变量值。

### 2.9 真实密钥由用户手动配置

Claude Code 可以告诉用户"请在 `.env` 中配置 `OPENAI_API_KEY=你的Key`"，但不能替用户填写真实的 Key 值。

### 2.10 密钥泄露必须立即作废和更换

一旦怀疑密钥泄露（提交 Git、粘贴聊天、截图发送），立即作废旧密钥、生成新密钥、更新所有使用该密钥的环境。不要抱侥幸心理。

---

## 3. 术语定义

### 3.1 环境变量

项目运行时由操作系统或运行环境注入的配置项，用于区分开发、测试、生产等不同环境，或用于注入不便于写死在代码中的配置。

**示例：** `PORT`、`DATABASE_URL`、`NODE_ENV`、`API_BASE_URL`、`REDIS_URL`

### 3.2 密钥

用于访问受保护资源的敏感凭证。密钥一旦泄露，攻击者可以冒充身份、访问数据、消耗配额、执行操作。

**示例：** `API_KEY`、`ACCESS_TOKEN`、`REFRESH_TOKEN`、`JWT_SECRET`、`SESSION_SECRET`、`DATABASE_PASSWORD`、`SMTP_PASSWORD`、`CLOUD_SECRET_KEY`

### 3.3 .env（真实环境变量文件）

包含本地或生产环境真实配置的文件。**不进入 Git。不公开。不粘贴进聊天记录。** Claude Code 默认不得读取，除非用户明确授权。

### 3.4 .env.example（环境变量示例文件）

用于说明项目需要哪些环境变量的模板文件。**可以进入 Git。只写占位符，不写真实值。** 必须随新增或删除环境变量而同步更新。

---

## 4. 文件分类规则

### 4.1 可以进入 Git 的文件

- `.env.example`
- `.env.template`
- `README` 中的配置说明（只含变量名和用途，不含真实值）
- `docs/setup.md` 中的环境变量说明
- 脱敏后的配置示例
- Docker 示例配置（`docker-compose.example.yml`）
- CI 示例配置（`.github/workflows/ci.example.yml`）

**规则：** 这些文件只能包含占位符（如 `your-api-key`、`replace-with-real-value`），不得包含真实凭证。凡涉及真实密钥，一律不得进入。

### 4.2 默认禁止进入 Git 的文件

| 文件 | 原因 |
|------|------|
| `.env` | 含真实密钥 |
| `.env.local` | 本地覆盖配置，可能含密钥 |
| `.env.production` | 生产环境密钥 |
| `.env.development` | 开发环境密钥（如果含真实 API Key） |
| `.env.test` | 测试环境配置（如果含真实密钥） |
| `secrets.json` | 密钥文件 |
| `credentials.json` | 凭证文件 |
| `service-account.json` | GCP/AWS 等服务账号密钥 |
| `private-key.pem` | 私钥 |
| `id_rsa`、`id_ed25519` | SSH 私钥 |
| `cookies.txt` | 浏览器 Cookie |
| `token.txt` | 保存的 Token |

### 4.3 需要谨慎判断的文件

| 文件 | 判断标准 |
|------|----------|
| Docker Compose 环境配置 | 如果包含真实密钥 → 不进 Git；如果只有占位符 → 可以进 Git |
| CI/CD 配置（`.github/workflows/`） | secrets 只能用平台 secrets 功能引用，不能写死 |
| 云服务配置（`terraform.tfvars` 等） | 包含真实密钥的不进，只有模板的可以进 |
| 数据库连接配置 | 真实连接串不进 Git，示例连接串可以 |
| 邮件服务配置 | 真实 SMTP 密码不进 Git |
| 第三方 API 配置 | 真实 Key 不进 Git |

**规则：** 凡不确定的，默认不进 Git。宁可多一步手动配置，也不少一份安全保障。

---

## 5. .gitignore 要求

所有正式项目的 `.gitignore` 必须包含以下内容：

```gitignore
# Environment — REAL secrets (never commit)
.env
.env.local
.env.*.local
.env.production
.env.development
.env.test

# Keys and certificates
*.pem
*.key
secrets.json
credentials.json
service-account.json

# Saved credentials
cookies.txt
token.txt
```

按项目实际情况追加：

```gitignore
# Database (real data files)
*.sqlite
*.sqlite3
data.db

# User content
uploads/
exports/

# Backups
backups/

# Logs
logs/*.log
```

### .gitignore 规则

1. `.env.example` **不得被忽略。** 这是必须进入 Git 的模板文件。
2. `.env.template` **不得被忽略。** 同上。
3. 真实 `.env`（任何包含真实密钥的 env 文件）**必须被忽略。**
4. 真实数据库文件默认忽略（SQLite `.db` 文件不进 Git）。
5. 客户上传文件默认忽略。
6. 备份文件默认忽略。
7. 日志文件默认忽略。
8. **修改 `.gitignore` 后必须执行 `git status` 检查是否还有敏感文件未被忽略。**

---

## 6. 环境变量命名规范

### 推荐命名

**通用配置：**
```
NODE_ENV          # 运行环境：development / production / test
PORT              # 服务端口
APP_NAME          # 应用名称
APP_URL           # 应用访问地址
API_BASE_URL      # API 基础路径
```

**数据库配置：**
```
DATABASE_URL      # 完整数据库连接串（推荐，Prisma 默认）
DATABASE_HOST     # 数据库主机地址
DATABASE_PORT     # 数据库端口
DATABASE_USER     # 数据库用户名
DATABASE_PASSWORD # 数据库密码
DATABASE_NAME     # 数据库名称
```

**认证配置：**
```
JWT_SECRET        # JWT 签名密钥
SESSION_SECRET    # Session 加密密钥
AUTH_SECRET       # 通用认证密钥（NextAuth 等）
```

**外部 API 配置：**
```
OPENAI_API_KEY    # OpenAI API 密钥
CLAUDE_API_KEY    # Anthropic Claude API 密钥
DEEPSEEK_API_KEY  # DeepSeek API 密钥
ZHIPU_API_KEY     # 智谱 API 密钥
TAVILY_API_KEY    # Tavily 搜索 API 密钥
FIRECRAWL_API_KEY # Firecrawl 爬取 API 密钥
```

**邮件配置：**
```
SMTP_HOST         # SMTP 服务器地址
SMTP_PORT         # SMTP 端口
SMTP_USER         # SMTP 用户名
SMTP_PASSWORD     # SMTP 密码
```

**缓存配置：**
```
REDIS_URL         # Redis 完整连接串
REDIS_HOST        # Redis 主机
REDIS_PORT        # Redis 端口
REDIS_PASSWORD    # Redis 密码
```

### 命名规则

1. **使用大写字母和下划线。** `DATABASE_URL` 而非 `databaseUrl`。
2. **名称必须表达用途。** 看到名字就知道这个变量是干什么的。
3. **不使用模糊名称。** ❌ `KEY`、`TOKEN`、`PASSWORD`——不知道是哪个 Key、哪个 Token。
4. **不在变量名中暴露过多业务隐私。** 变量名本身不应是敏感信息。
5. **不在前端变量中暴露后端密钥。** 见第 7 节。

---

## 7. 前端环境变量规则

前端环境变量会被打包到浏览器端代码中，因此安全要求更严格。

### 规则

1. **任何会被前端打包的变量不得包含真正密钥。** 假设浏览器端的所有代码都是公开的。
2. **Vite 中 `VITE_` 前缀变量会暴露给前端。** 不在 `VITE_` 变量中放密钥。
3. **Next.js 中 `NEXT_PUBLIC_` 前缀变量会暴露给前端。** 同上。
4. **前端只能保存公开配置。** 如 API 地址、应用名称、版本号、功能开关。
5. **前端不得保存数据库连接串。** 数据库永远不直接暴露给浏览器。
6. **前端不得保存 API Key。** 所有第三方 API 调用通过后端代理。
7. **前端不得保存管理员密钥。** 权限判定永远在后端。
8. **前端不得保存支付密钥。** 支付流程永远在后端或使用支付 SDK 的客户端 Token（非 Secret）。
9. **前端不得保存云服务 Secret。** 文件上传等操作使用预签名 URL，不暴露 Secret。
10. **前端权限判断不能替代后端权限判断。** 前端的路由守卫是 UX，后端的鉴权是安全。

### 允许示例

```env
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_NAME=Medical CRM
VITE_APP_VERSION=0.2.0
VITE_ENABLE_AI_FEATURES=false
```

### 禁止示例

```env
VITE_DATABASE_URL=postgresql://...     ❌ 绝不
VITE_JWT_SECRET=my-super-secret        ❌ 绝不
VITE_OPENAI_API_KEY=sk-abc123...       ❌ 绝不
VITE_ADMIN_TOKEN=admin-token-xxx       ❌ 绝不
```

---

## 8. 后端环境变量规则

后端可以读取敏感环境变量，但必须安全地管理和使用。

### 规则

1. **只在服务端读取敏感变量。** 使用 `process.env`（Node.js）或等效机制，不将值传给前端。
2. **不把敏感变量返回给前端。** API 响应中不得出现密钥、Token、密码哈希等字段。
3. **不把敏感变量写进日志。** 见 `Security_Standard.md` 第 12 节。
4. **不把敏感变量写进错误信息。** 异常消息中不暴露数据库连接串或 API Key。
5. **不把敏感变量写进交付报告。** 报告中引用变量名，不引用变量值。
6. **启动时可以检查变量是否存在，但不得打印真实值。** 用 `if (!process.env.DATABASE_URL) throw Error(...)`，不要 `console.log(process.env.DATABASE_URL)`。
7. **缺少必填变量时应给出清晰的错误提示。** "Missing required environment variable: DATABASE_URL" 是好的。静默失败或含糊报错是坏的。
8. **不得在代码中写死默认真实密钥。** 开发环境的默认值可以是 `dev-secret-do-not-use-in-production`，不能是真实的生产密钥。
9. **测试环境应使用测试密钥或占位值。** 单元测试和集成测试不依赖真实的第三方 API Key。
10. **生产密钥必须由部署环境单独配置。** 不在代码仓库的任何位置存储生产凭证。

---

## 9. 数据库连接变量规则

数据库连接信息属于高度敏感配置。

### 规则

1. **`DATABASE_URL` 不得进入 Git。** 已包含用户名、密码、主机、端口、数据库名的完整连接串极其敏感。
2. **生产 `DATABASE_URL` 不得写进 README。** README 中如果需要示例，使用占位符格式。
3. **交付报告不得暴露 `DATABASE_URL`。** 可写"数据库连接已配置"，不写连接串本身。
4. **开发环境可使用本地示例值。** 如 `postgresql://postgres:postgres@localhost:5432/myapp_dev`。
5. **测试环境应使用测试数据库。** 独立于开发和生产，数据可随时重建。
6. **生产环境必须使用生产密钥管理方式。** 服务器环境变量、Docker secrets、云平台密钥管理服务。
7. **Claude Code 不得自动连接生产数据库。** 这是 S3 级禁止操作。
8. **数据库连接变更必须记录风险。** 在交付报告中说明。
9. **数据库迁移前必须确认连接的是哪个环境。** 避免在错误的环境中执行 migration。
10. **SQLite 真实数据文件默认不得进入 Git。** 已在 `.gitignore` 中。

### .env.example 数据库示例

```env
# PostgreSQL
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"

# MySQL
DATABASE_URL="mysql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"

# SQLite
DATABASE_URL="file:./data.db"
```

---

## 10. AI 服务密钥规则

AI 服务密钥是高频使用的敏感凭证，需要特别管理。

### 适用的 AI 服务密钥

`OPENAI_API_KEY`、`CLAUDE_API_KEY`、`DEEPSEEK_API_KEY`、`ZHIPU_API_KEY`、`GEMINI_API_KEY`、`TAVILY_API_KEY`、`FIRECRAWL_API_KEY`、`EXA_API_KEY`

### 规则

1. **AI API Key 不进入 Git。** 每次提交前确认。
2. **AI API Key 不写进 Prompt。** Prompt 可能被 AI 服务商记录和存储。
3. **AI API Key 不写进 README。** README 中如果需要提及，写"需要配置 OPENAI_API_KEY"。
4. **AI API Key 不写进交付报告。** 报告中说"已配置 AI API Key"，不说 Key 值。
5. **AI API Key 不写进前端代码。** AI 调用永远通过后端代理。
6. **AI API Key 只在后端或本地安全环境读取。** Node.js 服务端、本地脚本——不暴露到浏览器。
7. **客户项目使用 AI 服务时必须明确数据边界。** 客户数据是否会被发送到 OpenAI/Claude 等外部服务？必须告知客户。
8. **不得把客户真实数据随意发给外部 AI API。** 除非客户明确知晓并同意。
9. **Claude Code 不得为了调试要求用户粘贴真实 Key。** 调试时使用测试 Key 或确认 Key 已配置即可。
10. **AI Key 泄露后必须立即作废并更换。** 各 AI 平台后台均可操作。

---

## 11. 外部服务凭证规则

### 适用服务

GitHub、Gitee、GitLab、阿里云、腾讯云、Vercel、飞书、微信、邮箱、支付平台、股票软件、数据服务 API

### 规则

1. **外部服务 Token 不进入 Git。** Personal Access Token、OAuth Token、API Secret 一律不进仓库。
2. **外部服务 Token 不写进文档。** 文档中说明"需要配置 XX_TOKEN"，不写 Token 值。
3. **外部服务 Token 不交给 Claude Code 自动保存。** Claude Code 不知道这些 Token 会被存在哪。
4. **外部服务登录状态不得让 Claude Code 无边界操作。** 登录了 GitHub ≠ Claude Code 可以自动 push。
5. **GitHub Token 不得默认允许 push / merge。** Token 权限应限制在只读或最小范围。
6. **云服务密钥不得用于自动部署，除非有明确授权。** 每一次部署都需确认。
7. **支付平台密钥属于最高风险。** 一旦泄露可能造成直接经济损失。必须人工管理。
8. **股票交易相关凭证属于最高风险。** 涉及真实资金，绝不可让 AI 自动操作。
9. **邮箱、微信、飞书等账号访问必须明确授权范围。** 只读？可发送？每次操作都要确认。
10. **不得自动群发、自动支付、自动交易。** S3 级禁止，不可协商。

---

## 12. 新增环境变量流程

```
提出变量需求（什么功能需要这个变量）
    ↓
说明变量用途（这个变量用于什么？为什么不能用已有变量？）
    ↓
判断是否敏感（是密钥还是普通配置？）
    ↓
确定变量命名（遵循第 6 节命名规范）
    ↓
修改 .env.example（添加变量名 + 占位符示例值）
    ↓
更新 README 或 docs/setup.md（让下一个接手的人知道怎么配置）
    ↓
用户手动配置真实 .env（Claude Code 不参与这一步）
    ↓
运行 Build / Test 或说明原因
    ↓
交付报告记录（新增了什么变量、用途、是否敏感）
```

### 每次新增变量必须说明

| # | 说明项 | 示例 |
|---|--------|------|
| 1 | 变量名 | `TAVILY_API_KEY` |
| 2 | 是否敏感 | 是 — API Key |
| 3 | 用途 | 用于 Web Research Agent 的搜索功能 |
| 4 | 使用位置 | `backend/src/modules/agent/tavily.service.ts` |
| 5 | 示例值 | `tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| 6 | 是否前端可见 | 否，仅后端使用 |
| 7 | 是否生产环境需要 | 是 |
| 8 | 缺失时项目如何表现 | Agent 搜索功能不可用，其他功能正常 |
| 9 | 是否影响部署 | 是，生产环境需手动配置该变量 |
| 10 | 是否需要用户手动配置 | 是 |

---

## 13. 修改环境变量流程

修改环境变量属于中高风险（P1–P2）。

### 修改前必须确认

| # | 确认项 |
|---|--------|
| 1 | 为什么要修改？（改名？改默认值？改变量类型？） |
| 2 | 是否影响已有部署？（已部署的环境需要同步更新） |
| 3 | 是否影响本地开发？（其他开发者的本地 .env 需要更新） |
| 4 | 是否影响测试？（测试环境的变量是否需要同步修改） |
| 5 | 是否影响 CI/CD？（CI 配置中的 secrets 是否需要更新） |
| 6 | 是否影响生产环境？（生产密钥是否需要更换） |
| 7 | 是否需要兼容旧变量？（过渡期是否两个变量名都支持） |
| 8 | 是否需要迁移文档？（README、setup 文档、交付报告） |
| 9 | 是否需要更新交付说明？ |
| 10 | 是否有回滚方式？（如果新变量有问题，能否退回到旧方式） |

### 禁止

- ❌ 直接改变量名但不更新文档 — 下一个接手的人不知道怎么配置
- ❌ 删除变量但不检查使用位置 — 代码中可能还在引用
- ❌ 修改生产变量但不通知用户 — 生产环境可能因配置缺失而崩溃
- ❌ 修改数据库连接但不确认环境 — 可能意外连到生产数据库
- ❌ 修改 AI Key 变量但不说明影响 — AI 功能可能静默失效

---

## 14. 删除环境变量流程

删除环境变量前必须逐项确认：

| # | 确认项 |
|---|--------|
| 1 | 是否仍被代码引用？（全局搜索变量名） |
| 2 | 是否仍被脚本引用？（`package.json` 的 scripts、`scripts/` 目录） |
| 3 | 是否仍被部署配置引用？（Docker、CI/CD、云平台） |
| 4 | 是否仍被文档引用？（README、`docs/setup.md`） |
| 5 | 是否仍被测试引用？（测试中是否设置了该变量） |
| 6 | 是否影响旧版本？（老版本的代码是否还需要这个变量） |
| 7 | 是否影响客户部署？（客户的环境变量是否需要同步清理） |
| 8 | 是否需要保留兼容期？（先标记 deprecated，N 个版本后再删除） |
| 9 | 是否需要更新 `.env.example`？（从模板中移除） |
| 10 | 是否需要更新 CHANGELOG？（记录删除和原因） |

### 规则

- 不得随意删除环境变量。每一个变量都可能有依赖方。
- 删除变量必须先搜索所有引用并逐条确认。
- 删除变量必须更新文档（`.env.example`、README、setup 文档）。
- 删除变量必须说明回滚方式（如果删除后有功能异常，如何快速恢复）。
- 删除变量必须写入交付报告。

---

## 15. Claude Code 权限规则

### Claude Code 默认允许（P0–P1）

- 读取 `.env.example`
- 修改 `.env.example`（添加/更新占位符）
- 更新 README 中的环境变量说明
- 更新 `docs/setup.md` 中的变量说明
- 检查 `.gitignore` 是否忽略了 `.env`
- 说明用户需要手动配置哪些变量及其用途

### Claude Code 必须确认后才能（P2）

- 读取真实 `.env`（用户必须明确授权并确认风险）
- 修改真实 `.env`（极其罕见，必须每次单独确认）
- 查看本地数据库连接串
- 修改部署环境变量说明（避免误指导生产配置）
- 修改 CI/CD 环境变量说明
- 修改 Docker 环境配置
- 修改云服务相关配置

### Claude Code 禁止自动（P3）

- 提交真实 `.env` 到 Git
- 在任何输出中打印真实密钥
- 把密钥写进交付报告
- 把密钥写进 Prompt
- 把密钥写进日志
- 自动读取浏览器 Cookie
- 自动读取 SSH Key
- 自动保存外部账号 Token
- 自动修改生产环境变量

---

## 16. 交付项目中的密钥处理

### 交付时必须做到

| # | 要求 |
|---|------|
| 1 | 交付 `.env.example`（完整的变量模板） |
| 2 | 不交付真实 `.env`（不发送、不压缩、不截图） |
| 3 | 提供环境变量配置说明（README 或独立的 `docs/setup.md`） |
| 4 | 说明哪些变量必须填写（必填 vs 可选） |
| 5 | 说明变量用途（每个变量是干什么的） |
| 6 | 说明示例格式（让客户知道应该填什么格式的值） |
| 7 | 说明缺失变量时的影响（哪些功能会不可用） |
| 8 | 由客户或用户手动配置真实密钥 |
| 9 | 交付报告不得包含真实密钥 |

### 接单项目特别注意事项

- 不要要求客户把永久密钥直接发送给你，除非绝对必要。
- 如果必须使用客户密钥，优先让客户创建**临时密钥**或**只读密钥**。
- 项目完成后**建议客户更换密钥**（尤其是给了你密钥的客户）。
- **不保存客户密钥**到你任何长期存储中。
- **不把客户密钥写入你的代码仓库。**

---

## 17. 本地开发环境规则

1. **每个项目使用自己的 `.env`。** 不多个项目共用一个混乱的 `.env` 文件。
2. **不把 `.env` 放到桌面或随意目录。** `.env` 只存在于项目根目录中。
3. **不把 `.env` 发给 AI。** 如 Claude Code 需要了解配置结构，让它读 `.env.example`。
4. **不把 `.env` 通过聊天工具发给他人。** 微信、飞书、邮件——都不安全。
5. **不把 `.env` 压缩进交付包。** 交付前检查压缩包内容。
6. **不把 `.env` 截图发出。** 截图 = 明文 = 可被 OCR = 可被转发。
7. **不把生产密钥用于本地随意测试。** 本地测试用测试 Key，不要拿生产 Key 做实验。
8. **不在公共电脑保存密钥。** 网吧、图书馆、共享电脑——不配置真实密钥。
9. **不在不可信项目中使用真实密钥。** GitHub 上 clone 下来的陌生项目，先审查再配置 Key。
10. **定期检查本地 `.env` 是否仍被 `.gitignore` 忽略。** 执行 `git status` 确认。

---

## 18. 生产环境变量规则

生产环境变量属于 S3 最高风险级别。

### 规则

1. **生产变量不得写入 Git。** 任何形式都不行。
2. **生产变量不得写入 README。** 即使 README 是私有的。
3. **生产变量不得写入交付报告。** 报告引用变量名，不引用值。
4. **生产变量不得交给 Claude Code 自动修改。** 这是 S3 禁止操作。
5. **生产变量应由部署平台或服务器安全管理。** Docker secrets、K8s secrets、云平台密钥管理、服务器环境变量。
6. **修改生产变量前必须备份或记录原值。** 以便回滚。
7. **修改生产变量必须有回滚方案。** 如果新值导致服务异常，如何快速恢复原值。
8. **修改生产变量必须明确维护窗口。** 影响范围最小的时段操作。
9. **修改生产变量必须由用户确认。** Claude Code 不参与。
10. **修改生产变量后必须验证服务是否正常。** 检查：服务是否启动、核心功能是否可用、日志是否有异常。

---

## 19. 测试环境变量规则

测试环境应使用独立于开发和生产环境的配置。

### 规则

1. **测试环境不得连接生产数据库。** 测试可能产生脏数据、可能清空数据、可能高负载。
2. **测试环境不得使用真实客户数据。** 使用脱敏假数据或专用的测试数据集。
3. **测试环境应使用测试 API Key。** 各平台通常提供 test mode 或 sandbox key。
4. **测试环境应使用测试数据库。** 独立于开发和生产，可随时重建。
5. **测试环境变量应与开发环境区分。** 通过 `NODE_ENV=test` 或 `.env.test` 区分。
6. **自动测试不得依赖真实外部账号。** 不要求测试环境登录真实的微信、邮箱。
7. **测试失败不得通过修改真实密钥解决。** 测试应该自包含，不依赖外部密钥的正确性。
8. **E2E 测试应避免在日志或截图中暴露敏感凭证。**
9. **测试日志不得输出密钥。** 测试的 `console.log` 也不放过。
10. **CI 测试如需密钥，必须使用平台 secrets 管理。** CI 的 env 配置中不能写死密钥。

---

## 20. CI/CD Secrets 规则

如果未来使用 CI/CD（GitHub Actions、GitLab CI 等），必须遵守以下规则。

### 规则

1. **CI/CD secrets 不写进仓库。** 任何 CI 配置文件（`.yml`、`.yaml`）中不写死密钥。
2. **CI/CD secrets 使用平台 secrets 功能。** GitHub Secrets、GitLab Variables——用平台提供的加密存储。
3. **CI/CD 日志不得打印 secrets。** CI 运行日志中可能泄露——配置时确保 echo 模式不暴露。
4. **Pull Request 不应暴露 secrets。** PR 触发的 CI 不应让外部贡献者访问 secrets。
5. **第三方 Action / Plugin 必须审查。** 很多 CI 安全事件来自恶意或漏洞第三方 Action。
6. **不给 CI/CD 超出必要的权限。** 构建不需要生产数据库密码。
7. **部署密钥必须限制权限。** 只允许部署到指定环境、指定分支。
8. **GitHub Token 不得默认给写权限。** CI 中的 `GITHUB_TOKEN` 权限范围应限制。
9. **生产部署必须人工确认或受保护分支。** 不能 push 就自动部署生产。
10. **CI/CD secrets 变更必须记录。** 记录在 Decision Log 中。

### 当前阶段

- **不急于配置 CI/CD。** 先跑通本地 Build + Test + Git 全流程。
- **不急于配置自动部署。** 手动部署流程稳定后再考虑自动化。
- **先建立本地标准和文档。** CI/CD 的 secrets 管理以本文件为原则基础。

---

## 21. 密钥泄露处理流程

### 密钥泄露的常见形式

- 密钥被提交到 Git（本地或远程）
- 密钥被写入 README 或文档
- 密钥被写入日志
- 密钥被粘贴进聊天记录（微信、飞书、Slack）
- 密钥被写进交付报告
- 密钥被截图发送
- 密钥进入公开仓库（GitHub public repo）
- 密钥被客户或第三方误传

### 标准处理流程

```
发现泄露
    ↓
立即停止继续传播（删除消息、撤回文件、停止分享）
    ↓
确认泄露范围（本机？Git？公开？几个人看到了？）
    ↓
确认是否已 push 或公开（git log / GitHub 检查）
    ↓
作废泄露密钥（在各平台后台立即 revoke / delete）
    ↓
生成新密钥（在平台后台创建新的 Key / Secret）
    ↓
更新本地和生产配置（替换所有使用旧密钥的地方）
    ↓
检查 Git 历史（确认密钥在哪些 commit 中出现）
    ↓
必要时清理 Git 历史（如果已 push 到公开仓库，必须清理）
    ↓
记录安全事件（时间、原因、影响范围、处理措施）
    ↓
复盘并补充规则（为什么泄露？现有标准为什么没防住？）
```

### 处理要求

1. **泄露密钥必须立即更换。** 不要抱有"可能没人看到"的侥幸心理。作废只需要 1 分钟。
2. **不要只删除文件就以为安全。** 如果已进入 Git 历史，删除文件不能删除历史。
3. **如果已经 push 到公开仓库，必须按公开泄露处理。** 任何 clone/fork 过的人都有历史。
4. **Git 历史清理属于高风险操作，不得由 Claude Code 自动执行。** 需要用户手工操作。
5. **必须记录 Decision Log 或安全事件记录。** 便于事后追溯和改进流程。

---

## 22. .env.example 标准模板

以下是项目 `.env.example` 的通用模板。真实项目应删除不需要的变量，保留项目实际需要的。

```env
# ============================
# Application
# ============================
NODE_ENV=development
PORT=3000
APP_NAME=your-app-name
APP_URL=http://localhost:3000

# ============================
# Frontend (Vite / Next.js)
# ============================
VITE_API_BASE_URL=http://localhost:3000/api
# NEXT_PUBLIC_API_URL=http://localhost:3000/api

# ============================
# Database (choose one)
# ============================
# PostgreSQL
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"

# MySQL
# DATABASE_URL="mysql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"

# SQLite
# DATABASE_URL="file:./data.db"

# ============================
# Auth
# ============================
JWT_SECRET=replace-with-a-random-string-at-least-32-chars
SESSION_SECRET=replace-with-a-random-string-at-least-32-chars

# ============================
# AI Services (use only what you need)
# ============================
OPENAI_API_KEY=sk-replace-with-your-openai-api-key
CLAUDE_API_KEY=sk-ant-replace-with-your-claude-api-key
DEEPSEEK_API_KEY=sk-replace-with-your-deepseek-api-key
# ZHIPU_API_KEY=replace-with-your-zhipu-api-key
# TAVILY_API_KEY=tvly-replace-with-your-tavily-api-key
# FIRECRAWL_API_KEY=fc-replace-with-your-firecrawl-api-key

# ============================
# Cache (optional)
# ============================
# REDIS_URL=redis://localhost:6379

# ============================
# Mail (optional)
# ============================
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=your-smtp-user
# SMTP_PASSWORD=replace-with-your-smtp-password
```

### 使用要求

- **真实项目应删除不需要的变量。** 不要让接手的人猜测哪些变量需要配置。
- **本模板只能作为示例。** 实际项目以自己的需求为准。
- **示例值不得是真实密钥。** 全部用 `replace-with-...` 或等效占位符。
- **项目 README 应说明哪些变量是必填、哪些是可选。** 降低上手成本。

---

## 23. 安全检查清单

### 23.1 开发前检查

- [ ] 是否需要新增环境变量
- [ ] 是否涉及真实密钥
- [ ] 是否涉及数据库连接
- [ ] 是否涉及 AI API Key
- [ ] 是否涉及外部服务 Token
- [ ] 是否需要修改 `.env.example`
- [ ] 是否需要用户手动配置
- [ ] 是否影响部署
- [ ] 是否需要更新 README
- [ ] 是否需要更新交付报告

### 23.2 Commit 前检查

- [ ] 没有 `.env` 出现在 staged 文件中
- [ ] 没有 `.env.local` 出现在 staged 文件中
- [ ] 没有 API Key 硬编码
- [ ] 没有 Token 硬编码
- [ ] 没有数据库密码硬编码
- [ ] 没有真实 `DATABASE_URL`
- [ ] 没有客户密钥
- [ ] `.env.example` 只有占位符，无真实值
- [ ] `.gitignore` 已覆盖所有真实密钥文件类型
- [ ] `git diff` 已逐文件检查，确认无敏感内容

### 23.3 交付前检查

- [ ] `.env.example` 已更新（包含所有项目需要的变量）
- [ ] README 已说明环境变量的用途和配置方式
- [ ] 未交付真实 `.env`（不发送、不压缩、不截图）
- [ ] 未在交付报告中暴露密钥
- [ ] 用户知道哪些变量需要通过什么方式获取（如：去 OpenAI 后台创建 API Key）
- [ ] 数据库连接说明已脱敏（示例使用占位符）
- [ ] 外部 API Key 说明已脱敏
- [ ] 生产环境变量未在交付物中泄露
- [ ] 密钥风险已说明
- [ ] 未解决风险已列出

---

## 24. 与其他标准文件的关系

| 标准文件 | 与本文件的关系 |
|----------|----------------|
| `Security_Standard.md` | 定义整体安全边界，本文件是密钥安全的专项执行标准 |
| `Git_Standard.md` | 定义 `.env` 和 secrets 不进 Git 的规则及泄露处理 |
| `Database_Standard.md` | 定义数据库连接的安全管理和回滚 |
| `Dependency_Review_Standard.md` | 定义外部依赖的密钥和凭证管理 |
| `Testing_Standard.md` | 定义测试环境变量的独立性和安全性 |
| `Delivery_Standard.md` | 定义交付时密钥处理规范 |
| `Logging_Monitoring_Standard.md` | 定义日志中不得泄露 secrets |

本文件专门定义环境变量与密钥的管理规则。整体安全策略见 `Security_Standard.md`。

---

## 25. 禁止事项

| # | 禁止事项 | 原因 |
|---|----------|------|
| 1 | 禁止提交真实 `.env` | 密钥泄露，不可逆 |
| 2 | 禁止提交 API Key | 同上 |
| 3 | 禁止提交 Token | 同上 |
| 4 | 禁止提交数据库密码 | 同上 |
| 5 | 禁止提交生产配置 | 生产环境暴露 |
| 6 | 禁止把密钥写进 README | README 可能是公开的 |
| 7 | 禁止把密钥写进 Prompt | Prompt 可能被服务商记录 |
| 8 | 禁止把密钥写进日志 | 日志可能被同步、备份、泄露 |
| 9 | 禁止把密钥写进交付报告 | 报告可能被传播 |
| 10 | 禁止让 Claude Code 默认读取真实 `.env` | Claude Code 的上下文可能被记录 |
| 11 | 禁止前端暴露后端密钥 | 浏览器端代码视为完全公开 |
| 12 | 禁止测试环境连接生产数据库 | 测试可能破坏生产数据 |
| 13 | 禁止客户密钥长期保存在本地 | 客户数据安全责任 |
| 14 | 禁止把 `.env` 压缩进交付包 | 交付包可能被多次转发 |
| 15 | 禁止密钥泄露后只删除文件不更换密钥 | 删文件不能删 Git 历史，密钥一旦怀疑泄露立即作废 |

---

## 26. 当前阶段默认结论

1. **当前阶段所有项目必须有 `.env.example`。** 没有完整变量模板的项目不能被称为正式项目。
2. **当前阶段真实 `.env` 不进入 Git。** `.gitignore` 已配置，每次提交前检查。
3. **当前阶段 Claude Code 默认不得读取真实 `.env`。** 需要了解配置结构时，读取 `.env.example`。
4. **当前阶段不把任何真实 API Key 发给 AI。** Claude Code 的上下文不包含真实密钥。
5. **当前阶段所有 AI API Key 由用户手动配置。** Claude Code 可以说明如何获取和配置，但不能代填。
6. **当前阶段不使用生产密钥做本地测试。** 开发测试用独立测试 Key。
7. **当前阶段不配置复杂 CI/CD secrets。** 先跑通本地流程。
8. **当前阶段不让 Claude Code 自动连接外部账号。** 全部人工操作或单独授权。
9. **当前阶段所有密钥相关修改必须写入交付报告。** 新增了什么变量、用途是什么、是否敏感。
10. **密钥管理标准必须先于正式产品开发完成。** 没有密钥管理规范的项目不开工。
