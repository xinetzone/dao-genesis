# dao-genesis Web Dashboard 设计说明书

## 1. 背景与目标
在 CLI 工具链完善后，我们希望提供一个对人类友好的交互界面，让团队成员或个人能通过 Web 浏览器更直观地检索、查看、分析和管理 `dao-genesis` 存储的结构化记忆。
目标是实现一个轻量级、零依赖（前端纯静态 + 后端轻量 Python 原生库）的“记忆看板”。

## 2. 架构设计

由于需要支持从 Web 端对本地 JSON 数据进行更新与归档（Web 端管理功能），前端无法仅通过浏览器 `file://` 协议跨域读写本地文件。因此，架构采用 **“轻量后端 API + 纯静态前端 SPA”**：

- **后端 (`scripts/web_server.py`)**：
  基于 Python 内置的 `http.server` 构建，不依赖 Django/Flask/FastAPI 等第三方包。提供 RESTful API，直接封装我们已有的 `config.py` 和 `manage_memory.py` 逻辑。
- **前端 (`web/index.html`)**：
  采用原生 HTML5 + CSS3 + Vanilla JavaScript。为了实现组件化和美观，可以引入轻量级的 CDN 库（如 Tailwind CSS 通过 CDN、Vue.js 3 通过 CDN 用于数据绑定，或 ECharts 用于可视化，均不需要 Node.js 构建工具）。

## 3. 功能模块划分

### 3.1 搜索与过滤 (Search & Filter)
- **界面**：顶部/左侧有一个显眼的搜索框，支持输入关键词。旁边有状态下拉框（全部/Active/Archived）和任务类型筛选。
- **逻辑**：输入时实时向后端发送查询请求，或者直接前端读取 `search_index.json` 进行本地模糊过滤。结果以卡片列表（Card List）形式展示摘要（Review ID, 核心结论, Action Items）。

### 3.2 详细记录查看 (Detail View)
- **界面**：点击左侧的某条记录卡片，右侧主展示区渲染该记录的完整 JSON。
- **逻辑**：将数组字段（`action_items`, `decisions` 等）以清晰的 Markdown/无序列表形式渲染；将字符串字段（`task_type`, `timestamp`）作为元数据 Badge 显示。

### 3.3 数据可视化统计 (Dashboard Analytics)
- **界面**：一个单独的 Tab 或顶部统计区域。
- **图表**：
  1. **任务类型分布图 (Pie Chart)**：各 `task_type` 的占比。
  2. **时间趋势图 (Line/Bar Chart)**：过去 X 天/月，复盘记录新增的数量趋势。
- **技术**：引入 ECharts CDN。

### 3.4 Web 端管理与编辑 (Management)
- **归档**：详情页提供一个醒目的 [Archive] 按钮，点击调用后端 `PUT /api/reviews/{id}/archive` 接口，将状态置为 `archived`。
- **快速追加**：在 `action_items` 或 `decisions` 下方提供一个 Input 框，输入文字后点击 [Add]，调用后端 `PUT /api/reviews/{id}` 接口完成 `--append` 操作，并实时刷新页面数据。

## 4. API 契约设计 (RESTful)

后端需提供以下接口，所有请求/响应均为 JSON：

- `GET /api/index`
  - 返回 `.cache/reviews/search_index.json` 中的数据（带重建逻辑如果文件不存在）。
- `GET /api/reviews/{review_id}`
  - 读取 `.storage/reviews/{review_id}.json` 返回完整详情。
- `POST /api/reviews/{review_id}/archive`
  - 调用 `manage_memory` 归档逻辑，返回 `{ success: true }`。
- `POST /api/reviews/{review_id}/update`
  - Body: `{ "field": "action_items", "value": "新内容", "append": true }`
  - 调用 `manage_memory` 更新逻辑，返回 `{ success: true }`。

- `POST /api/sync/pull`
  - 调用 `sync_global` 的 pull 逻辑，从远端拉取最新全局记录。
  - 返回 `{ success: true, message: "..." }`
- `POST /api/sync/push`
  - 调用 `sync_global` 的 push 逻辑，将本地全局记录推送到远端 Git 仓库。
  - 返回 `{ success: true, message: "..." }`
- `POST /api/sync/share`
  - Body: `{ "review_id": "REV-xxx" }`
  - 调用 `sync_global` 的 share 逻辑，将当前项目的指定记录复制到全局目录。
  - 返回 `{ success: true, message: "..." }`

## 5. 实施步骤
1. 编写 `scripts/web_server.py`，实现基础 HTTP 路由与跨域（CORS）支持。
2. 创建 `web/` 目录结构（`index.html`, `app.js`, `style.css`）。
3. 集成 Vue 3 (CDN) 实现双向绑定与页面渲染。
4. 集成 ECharts (CDN) 完成数据统计视图。
5. 联调前后端接口，确保在本地 `python scripts/web_server.py` 启动后，打开 `http://localhost:8000` 即可使用所有功能。
6. 更新 `README.md` 与 `spec.md` 说明。