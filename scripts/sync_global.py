import argparse
import sys
import subprocess
import shutil
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import MEMORY_GLOBAL_ROOT, REVIEWS_DIR

def run_git_cmd(cmd: list, cwd: Path, check=True) -> str:
    """Run a git command in a specific directory and return its stdout."""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing '{' '.join(cmd)}' in {cwd}:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        if check:
            sys.exit(1)
        return ""

def cmd_init(args):
    repo_url = args.repo_url
    global_dir = MEMORY_GLOBAL_ROOT
    
    if (global_dir / ".git").exists():
        print(f"[Sync] 全局记忆库已在 {global_dir} 初始化过。")
        return
        
    if global_dir.exists() and any(global_dir.iterdir()):
        print(f"[Sync] 警告：目录 {global_dir} 已存在且非空，无法直接 clone。")
        print("建议先清理该目录，或手动在此目录执行 git init / git remote add。")
        sys.exit(1)
        
    print(f"[Sync] 正在将全局记忆库克隆到 {global_dir} ...")
    global_dir.parent.mkdir(parents=True, exist_ok=True)
    
    # Use subprocess.run directly instead of run_git_cmd to capture interactive cloning prompts if needed
    subprocess.run(["git", "clone", repo_url, str(global_dir)], check=True)
    
    # Ensure reviews directory exists in global
    (global_dir / "reviews").mkdir(parents=True, exist_ok=True)
    
    print(f"[Sync] 成功初始化全局记忆库：{global_dir}")

def cmd_pull(args):
    global_dir = MEMORY_GLOBAL_ROOT
    if not (global_dir / ".git").exists():
        print(f"[Sync] 错误：未找到全局记忆库。请先使用 `python scripts/sync_global.py init <repo_url>` 初始化。")
        sys.exit(1)
        
    print("[Sync] 正在拉取全局记忆...")
    subprocess.run(["git", "pull", "--rebase"], cwd=str(global_dir), check=True)
    print("[Sync] 成功拉取最新全局记忆。")

def cmd_push(args):
    global_dir = MEMORY_GLOBAL_ROOT
    if not (global_dir / ".git").exists():
        print(f"[Sync] 错误：未找到全局记忆库。请先使用 `python scripts/sync_global.py init <repo_url>` 初始化。")
        sys.exit(1)
        
    status_output = run_git_cmd(["git", "status", "--porcelain"], cwd=global_dir)
    if not status_output:
        print("[Sync] 无需推送，全局记忆库已是最新（无未提交更改）。")
        return
        
    print("[Sync] 发现本地更改，正在推送...")
    run_git_cmd(["git", "add", "."], cwd=global_dir)
    run_git_cmd(["git", "commit", "-m", "chore(memory): auto-sync global memory"], cwd=global_dir)
    subprocess.run(["git", "push"], cwd=str(global_dir), check=True)
    
    print("[Sync] 成功将本地更改推送到全局记忆库。")

def cmd_share(args):
    """Copy a local review to the global memory directory."""
    review_ids = args.review_id
    if not isinstance(review_ids, list):
        review_ids = [review_ids]
        
    global_dir = MEMORY_GLOBAL_ROOT
    global_reviews_dir = global_dir / "reviews"
    
    if not global_reviews_dir.exists():
        print(f"[Sync] 错误：未找到全局 reviews 目录，请先确保全局目录已初始化。")
        sys.exit(1)
        
    for review_id in review_ids:
        local_file = REVIEWS_DIR / f"{review_id}.json"
        global_file = global_reviews_dir / f"{review_id}.json"
        
        if not local_file.exists():
            print(f"[Share] 错误：本地记录 {review_id} 不存在。")
            continue
            
        # Copy to global directory
        try:
            shutil.copy2(local_file, global_file)
            print(f"[Share] 成功将 {review_id} 共享到全局记忆目录。")
        except Exception as e:
            print(f"[Share] 复制 {review_id} 失败：{e}", file=sys.stderr)
            
    print("\n[Share] 提示：执行 `python scripts/sync_global.py push` 将共享的记录推送到云端。")

def main():
    parser = argparse.ArgumentParser(description="Sync global memory records across projects via Git.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # init
    parser_init = subparsers.add_parser("init", help="Initialize global memory by cloning a git repository.")
    parser_init.add_argument("repo_url", type=str, help="Git repository URL (e.g., git@github.com:user/global-memory.git)")
    
    # pull
    parser_pull = subparsers.add_parser("pull", help="Pull latest global memory from remote.")
    
    # push
    parser_push = subparsers.add_parser("push", help="Push local global memory changes to remote.")
    
    # share
    parser_share = subparsers.add_parser("share", help="Share a local project review to the global memory directory.")
    parser_share.add_argument("review_id", type=str, nargs="+", help="The ID(s) of the local review record(s)")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "share":
        cmd_share(args)

if __name__ == "__main__":
    main()
