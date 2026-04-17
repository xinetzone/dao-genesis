from sync_global import (
    cmd_init, pull_global_memory, push_global_memory, share_local_record
)
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(scripts_dir))


class MockArgs:
    def __init__(self, repo_url=None, review_id=None):
        self.repo_url = repo_url
        self.review_id = review_id


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
@patch("sync_global.subprocess.run")
def test_cmd_init_success(mock_run, mock_global_root):
    # Mock global directory state
    mock_global_root.exists.return_value = False
    mock_global_root.__truediv__.return_value.exists.return_value = False

    args = MockArgs(repo_url="git@github.com:test/repo.git")
    cmd_init(args)

    mock_run.assert_called_once()
    assert "clone" in mock_run.call_args[0][0]
    assert "git@github.com:test/repo.git" in mock_run.call_args[0][0]


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
@patch("sync_global.subprocess.run")
def test_pull_global_memory_success(mock_run, mock_global_root):
    # Mock .git exists
    mock_global_root.__truediv__.return_value.exists.return_value = True

    result = pull_global_memory()

    mock_run.assert_called_once()
    assert "pull" in mock_run.call_args[0][0]
    assert result == "成功拉取最新全局记忆"


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
def test_pull_global_memory_not_init(mock_global_root):
    # Mock .git does not exist
    mock_global_root.__truediv__.return_value.exists.return_value = False

    with pytest.raises(Exception, match="未找到全局记忆库"):
        pull_global_memory()


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
@patch("sync_global.run_git_cmd")
@patch("sync_global.subprocess.run")
def test_push_global_memory_with_changes(
        mock_run, mock_git_cmd, mock_global_root):
    # Mock .git exists
    mock_global_root.__truediv__.return_value.exists.return_value = True
    # Mock git status returning something (has changes)
    mock_git_cmd.side_effect = ["M some_file.json", "", ""]

    result = push_global_memory()

    assert mock_git_cmd.call_count == 3
    mock_run.assert_called_once()
    assert "push" in mock_run.call_args[0][0]
    assert "成功" in result


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
@patch("sync_global.run_git_cmd")
def test_push_global_memory_no_changes(mock_git_cmd, mock_global_root):
    # Mock .git exists
    mock_global_root.__truediv__.return_value.exists.return_value = True
    # Mock git status returning empty (no changes)
    mock_git_cmd.return_value = ""

    result = push_global_memory()

    assert mock_git_cmd.call_count == 1
    assert "无需推送" in result


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
@patch("sync_global.REVIEWS_DIR", new_callable=MagicMock)
@patch("sync_global.shutil.copy2")
def test_share_local_record_success(
        mock_copy, mock_reviews_dir, mock_global_root):
    # Mock global reviews dir exists
    mock_global_root.__truediv__.return_value.exists.return_value = True
    # Mock local record exists
    mock_reviews_dir.__truediv__.return_value.exists.return_value = True

    result = share_local_record("REV-001")

    mock_copy.assert_called_once()
    assert "成功将 REV-001 共享到全局记忆目录" in result


@patch("sync_global.MEMORY_GLOBAL_ROOT", new_callable=MagicMock)
@patch("sync_global.REVIEWS_DIR", new_callable=MagicMock)
def test_share_local_record_not_found(mock_reviews_dir, mock_global_root):
    # Mock global reviews dir exists
    mock_global_root.__truediv__.return_value.exists.return_value = True
    # Mock local record DOES NOT exist
    mock_reviews_dir.__truediv__.return_value.exists.return_value = False

    with pytest.raises(Exception, match="本地记录 REV-001 不存在"):
        share_local_record("REV-001")
