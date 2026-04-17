import sys
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(scripts_dir))

from search_memory import search_index, display_results

@patch("search_memory.CACHE_REVIEWS_DIR", new_callable=MagicMock)
def test_search_index_success(mock_cache_dir):
    mock_index_file = MagicMock()
    mock_cache_dir.__truediv__.return_value = mock_index_file
    mock_index_file.exists.return_value = True
    
    mock_data = [
        {"review_id": "REV-001", "task_type": "Bug Fix", "status": "active", "conclusions": ["Fixed the issue"]},
        {"review_id": "REV-002", "task_type": "Feature", "status": "active", "action_items": ["Implement feature X"]},
        {"review_id": "REV-003", "task_type": "Bug Fix Archived", "status": "archived", "conclusions": ["Archived fix"]}
    ]
    mock_index_file.read_text.return_value = json.dumps(mock_data)
    
    # Test search by task_type
    results = search_index("bug", limit=10)
    assert len(results) == 1
    assert results[0]["review_id"] == "REV-001"
    
    # Test search by action_items
    results2 = search_index("feature", limit=10)
    assert len(results2) == 1
    assert results2[0]["review_id"] == "REV-002"
    
    # Test include archived
    results3 = search_index("bug", limit=10, include_archived=True)
    assert len(results3) == 2
    assert any(r["review_id"] == "REV-003" for r in results3)

@patch("search_memory.CACHE_REVIEWS_DIR", new_callable=MagicMock)
def test_search_index_missing_file(mock_cache_dir, capsys):
    mock_index_file = MagicMock()
    mock_cache_dir.__truediv__.return_value = mock_index_file
    mock_index_file.exists.return_value = False
    
    with pytest.raises(SystemExit) as exc:
        search_index("query")
    assert exc.value.code == 1
    
    captured = capsys.readouterr()
    assert "Search index not found" in captured.err

@patch("search_memory.REVIEWS_DIR", new_callable=MagicMock)
def test_display_results_empty(mock_reviews_dir, capsys):
    display_results([])
    captured = capsys.readouterr()
    assert "No matching records found" in captured.out

@patch("search_memory.REVIEWS_DIR", new_callable=MagicMock)
def test_display_results_with_data(mock_reviews_dir, capsys):
    results = [
        {"review_id": "REV-001", "status": "active", "task_type": "Test", "timestamp": "2026-04-17T00:00:00Z", "conclusions": ["Conc 1"], "action_items": ["Action 1"]}
    ]
    display_results(results, verbose=False)
    captured = capsys.readouterr()
    assert "Found 1 matching record" in captured.out
    assert "REV-001" in captured.out
    assert "Task: Test" in captured.out
    assert "Conclusion: Conc 1" in captured.out
    assert "Action: Action 1" in captured.out
