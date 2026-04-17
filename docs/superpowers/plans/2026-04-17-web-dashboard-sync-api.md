# Web Dashboard Sync API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the global memory Git sync functionality (`sync_global.py`) into the Web Dashboard interface and document the REST API endpoints.

**Architecture:** We will refactor `scripts/sync_global.py` to expose programmatic functions (`pull_global_memory()`, `push_global_memory()`, `share_local_record()`) instead of just CLI commands. Then, we will add new endpoints (`POST /api/sync/pull`, `POST /api/sync/push`, `POST /api/sync/share`) to `scripts/web_server.py`. Finally, we will update `web/index.html` and `web/app.js` to add "Sync" and "Share" buttons that call these APIs.

**Tech Stack:** Python, Vue 3, HTML/JS, Git.

---

### Task 1: Document REST API Endpoints

**Files:**
- Modify: `docs/superpowers/specs/2026-04-17-web-dashboard-design.md`

- [ ] **Step 1: Add new API endpoints to the documentation**

Append the new `/api/sync/*` endpoints to section "4. API 契约设计 (RESTful)".

```markdown
- `POST /api/sync/push`
  - 调用 `sync_global` 的 push 逻辑，将本地全局记录推送到远端 Git 仓库。
  - 返回 `{ success: true, message: "..." }`
- `POST /api/sync/pull`
  - 调用 `sync_global` 的 pull 逻辑，从远端拉取最新全局记录。
  - 返回 `{ success: true, message: "..." }`
- `POST /api/sync/share`
  - Body: `{ "review_id": "REV-xxx" }`
  - 调用 `sync_global` 的 share 逻辑，将当前项目的指定记录复制到全局目录。
  - 返回 `{ success: true }`
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-04-17-web-dashboard-design.md
git commit -m "docs: document sync REST API endpoints"
```

### Task 2: Refactor `sync_global.py` for programmatic use

**Files:**
- Modify: `scripts/sync_global.py`

- [ ] **Step 1: Extract core logic from `cmd_*` into functions**

Create `pull_global_memory()`, `push_global_memory()`, and `share_local_record(review_id)` that raise exceptions or return messages instead of calling `sys.exit()` directly.

```python
def pull_global_memory():
    global_dir = MEMORY_GLOBAL_ROOT
    if not (global_dir / ".git").exists():
        raise Exception("全局记忆库未初始化")
    subprocess.run(["git", "pull", "--rebase"], cwd=str(global_dir), check=True)
    return "成功拉取最新全局记忆"

def push_global_memory():
    global_dir = MEMORY_GLOBAL_ROOT
    if not (global_dir / ".git").exists():
        raise Exception("全局记忆库未初始化")
    status_output = run_git_cmd(["git", "status", "--porcelain"], cwd=global_dir)
    if not status_output:
        return "无需推送，已是最新"
    run_git_cmd(["git", "add", "."], cwd=global_dir)
    run_git_cmd(["git", "commit", "-m", "chore(memory): auto-sync global memory"], cwd=global_dir)
    subprocess.run(["git", "push"], cwd=str(global_dir), check=True)
    return "成功推送到全局记忆库"

def share_local_record(review_id: str):
    global_dir = MEMORY_GLOBAL_ROOT
    global_reviews_dir = global_dir / "reviews"
    if not global_reviews_dir.exists():
        raise Exception("全局 reviews 目录未初始化")
    local_file = REVIEWS_DIR / f"{review_id}.json"
    global_file = global_reviews_dir / f"{review_id}.json"
    if not local_file.exists():
        raise Exception(f"本地记录 {review_id} 不存在")
    shutil.copy2(local_file, global_file)
    return f"成功将 {review_id} 共享到全局"
```

- [ ] **Step 2: Update `cmd_*` functions to use the new core functions**

```python
def cmd_pull(args):
    try:
        print(f"[Sync] {pull_global_memory()}")
    except Exception as e:
        print(f"[Sync] 错误：{e}", file=sys.stderr)
        sys.exit(1)

def cmd_push(args):
    try:
        print(f"[Sync] {push_global_memory()}")
    except Exception as e:
        print(f"[Sync] 错误：{e}", file=sys.stderr)
        sys.exit(1)

def cmd_share(args):
    review_ids = args.review_id
    if not isinstance(review_ids, list):
        review_ids = [review_ids]
    for r_id in review_ids:
        try:
            print(f"[Share] {share_local_record(r_id)}")
        except Exception as e:
            print(f"[Share] 错误：{e}", file=sys.stderr)
```

- [ ] **Step 3: Commit**

```bash
git add scripts/sync_global.py
git commit -m "refactor: extract programmatic API from sync_global.py"
```

### Task 3: Add Sync APIs to `web_server.py`

**Files:**
- Modify: `scripts/web_server.py`

- [ ] **Step 1: Import sync functions**

```python
from sync_global import pull_global_memory, push_global_memory, share_local_record
```

- [ ] **Step 2: Add API routes in `do_POST`**

```python
        # API: /api/sync/pull
        elif parsed_path.path == '/api/sync/pull':
            try:
                msg = pull_global_memory()
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "message": msg}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        # API: /api/sync/push
        elif parsed_path.path == '/api/sync/push':
            try:
                msg = push_global_memory()
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "message": msg}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        # API: /api/sync/share
        elif parsed_path.path == '/api/sync/share':
            review_id = body.get("review_id")
            if not review_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Missing review_id"}).encode())
                return
            try:
                msg = share_local_record(review_id)
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "message": msg}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
```

- [ ] **Step 3: Commit**

```bash
git add scripts/web_server.py
git commit -m "feat(api): add sync endpoints to web server"
```

### Task 4: Integrate Sync features into Web Dashboard UI

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`

- [ ] **Step 1: Add Sync buttons to the header in `index.html`**

```html
            <div class="flex space-x-4 text-sm items-center">
                <!-- Sync Buttons -->
                <div class="flex bg-indigo-700 rounded-lg overflow-hidden mr-4">
                    <button @click="syncPull" :disabled="syncing" class="px-3 py-2 hover:bg-indigo-800 transition border-r border-indigo-600 disabled:opacity-50">
                        <i class="fa-solid fa-cloud-arrow-down" :class="{'fa-bounce': syncing === 'pull'}"></i>
                    </button>
                    <button @click="syncPush" :disabled="syncing" class="px-3 py-2 hover:bg-indigo-800 transition disabled:opacity-50">
                        <i class="fa-solid fa-cloud-arrow-up" :class="{'fa-bounce': syncing === 'push'}"></i>
                    </button>
                </div>
                
                <button @click="currentTab = 'search'" ...>
```

- [ ] **Step 2: Add "Share to Global" button in detail view header**

Next to the Archive button:
```html
                                <button v-if="selectedRecord" @click="shareRecord" class="px-3 py-1.5 bg-blue-50 text-blue-600 hover:bg-blue-100 rounded text-sm font-medium transition mr-2">
                                    <i class="fa-solid fa-share-nodes mr-1"></i> Share Global
                                </button>
                                <button v-if="selectedRecord.status !== 'archived'" @click="archiveRecord" ...>
```

- [ ] **Step 3: Implement functions in `app.js`**

Add `syncing`, `syncPull`, `syncPush`, and `shareRecord` to setup and return.

```javascript
        const syncing = ref(false);

        const syncPull = async () => {
            syncing.value = 'pull';
            try {
                const res = await fetch(`${API_BASE}/sync/pull`, { method: 'POST' });
                const data = await res.json();
                if (res.ok) alert(data.message);
                else alert("Error: " + data.error);
            } catch(e) {
                alert("Network error");
            } finally {
                syncing.value = false;
            }
        };

        const syncPush = async () => {
            syncing.value = 'push';
            try {
                const res = await fetch(`${API_BASE}/sync/push`, { method: 'POST' });
                const data = await res.json();
                if (res.ok) alert(data.message);
                else alert("Error: " + data.error);
            } catch(e) {
                alert("Network error");
            } finally {
                syncing.value = false;
            }
        };

        const shareRecord = async () => {
            if (!selectedRecord.value) return;
            try {
                const res = await fetch(`${API_BASE}/sync/share`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ review_id: selectedRecord.value.review_id })
                });
                const data = await res.json();
                if (res.ok) alert(data.message);
                else alert("Error: " + data.error);
            } catch(e) {
                alert("Network error");
            }
        };
```

Add these to the `return { ... }` block at the end of setup.

- [ ] **Step 4: Commit**

```bash
git add web/index.html web/app.js
git commit -m "feat(ui): add global sync and share buttons to dashboard"
```
