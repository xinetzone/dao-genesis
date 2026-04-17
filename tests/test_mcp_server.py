import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src and scripts to sys.path to import mcp_server and scripts
src_dir = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_dir))

from mcp_server import (
    search_reviews,
    get_review,
    update_review,
    archive_review,
    pull_global,
    push_global,
    share_record_to_global
)

@patch("mcp_server.search_index")
def test_search_reviews_found(mock_search):
    mock_search.return_value = [
        {
            "review_id": "REV-001",
            "status": "active",
            "timestamp": "2026-04-17T10:00:00Z",
            "task_type": "Test Task",
            "conclusions": ["Test conclusion"],
            "action_items": ["Test action"]
        }
    ]
    result = search_reviews("test query", limit=1)
    assert "Found 1 matching record" in result
    assert "REV-001" in result
    assert "Test Task" in result
    assert "Test conclusion" in result
    assert "Test action" in result

@patch("mcp_server.search_index")
def test_search_reviews_not_found(mock_search):
    mock_search.return_value = []
    result = search_reviews("empty query")
    assert result == "No matching records found."

@patch("mcp_server.load_record")
def test_get_review(mock_load):
    mock_load.return_value = {"review_id": "REV-001", "task_type": "Test Task"}
    result = get_review("REV-001")
    assert result["review_id"] == "REV-001"
    assert result["task_type"] == "Test Task"

@patch("mcp_server.load_record")
@patch("mcp_server.save_record")
def test_update_review_array_append(mock_save, mock_load):
    mock_load.return_value = {"review_id": "REV-001", "action_items": ["Old Action"]}
    result = update_review("REV-001", "action_items", "New Action", append=True)
    assert "Successfully updated" in result
    assert "[新增]" in result
    mock_save.assert_called_once()
    saved_data = mock_save.call_args[0][1]
    assert "New Action" in saved_data["action_items"]

@patch("mcp_server.load_record")
@patch("mcp_server.save_record")
def test_update_review_string_field(mock_save, mock_load):
    mock_load.return_value = {"review_id": "REV-001", "task_type": "Old Task"}
    result = update_review("REV-001", "task_type", "New Task", append=False)
    assert "Successfully updated" in result
    assert "[修改]" in result
    mock_save.assert_called_once()
    saved_data = mock_save.call_args[0][1]
    assert saved_data["task_type"] == "New Task"

def test_update_review_invalid_field():
    result = update_review("REV-001", "invalid_field", "value")
    assert "Error: Field 'invalid_field' is not allowed" in result

def test_update_review_string_append_error():
    result = update_review("REV-001", "task_type", "value", append=True)
    assert "Error: Cannot append to a string field" in result

@patch("mcp_server.load_record")
@patch("mcp_server.save_record")
def test_archive_review_success(mock_save, mock_load):
    mock_load.return_value = {"review_id": "REV-001", "status": "active"}
    result = archive_review("REV-001")
    assert "Successfully archived" in result
    mock_save.assert_called_once()
    saved_data = mock_save.call_args[0][1]
    assert saved_data["status"] == "archived"

@patch("mcp_server.load_record")
def test_archive_review_already_archived(mock_load):
    mock_load.return_value = {"review_id": "REV-001", "status": "archived"}
    result = archive_review("REV-001")
    assert "already archived" in result

@patch("mcp_server.pull_global_memory")
def test_pull_global(mock_pull):
    mock_pull.return_value = "Successfully pulled"
    result = pull_global()
    assert result == "Successfully pulled"

@patch("mcp_server.push_global_memory")
def test_push_global(mock_push):
    mock_push.return_value = "Successfully pushed"
    result = push_global()
    assert result == "Successfully pushed"

@patch("mcp_server.share_local_record")
def test_share_record_to_global(mock_share):
    mock_share.return_value = "Successfully shared"
    result = share_record_to_global("REV-001")
    assert result == "Successfully shared"
