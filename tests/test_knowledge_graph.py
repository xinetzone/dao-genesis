import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.knowledge_graph import sanitize_id, sanitize_label, generate_knowledge_graph

def test_sanitize_id():
    assert sanitize_id("Task Type") == "Task_Type"
    assert sanitize_id("Task-123") == "Task_123"
    assert sanitize_id("123_Task") == "N_123_Task"
    assert sanitize_id("") == "Unknown"

def test_sanitize_label():
    assert sanitize_label('Task "123"') == "Task '123'"
    assert sanitize_label("") == ""

@pytest.fixture
def mock_reviews_dir(tmp_path):
    reviews_dir = tmp_path / "reviews"
    reviews_dir.mkdir()
    
    # 1. Valid record
    record1 = {
        "status": "active",
        "task_type": "Bug Fix",
        "action_items": ["Fix error", 'Add "test"']
    }
    (reviews_dir / "1.json").write_text(json.dumps(record1))
    
    # 2. Inactive record (should be ignored)
    record2 = {
        "status": "archived",
        "task_type": "Feature",
        "action_items": ["Do something"]
    }
    (reviews_dir / "2.json").write_text(json.dumps(record2))
    
    # 3. Valid record with no action items (should be ignored)
    record3 = {
        "status": "active",
        "task_type": "Refactor",
        "action_items": []
    }
    (reviews_dir / "3.json").write_text(json.dumps(record3))
    
    # 4. Another valid record with the same task type
    record4 = {
        "status": "active",
        "task_type": "Bug Fix",
        "action_items": ["Deploy fix"]
    }
    (reviews_dir / "4.json").write_text(json.dumps(record4))
    
    return reviews_dir

@patch("scripts.knowledge_graph.REVIEWS_DIR")
def test_generate_knowledge_graph(mock_reviews_dir_patch, mock_reviews_dir):
    mock_reviews_dir_patch.exists.return_value = True
    # mock_reviews_dir_patch.glob.return_value = list(mock_reviews_dir.glob("*.json"))
    # The glob needs to return an iterator
    def mock_glob(pattern):
        return mock_reviews_dir.glob(pattern)
    mock_reviews_dir_patch.glob.side_effect = mock_glob
    
    graph = generate_knowledge_graph()
    
    assert "graph TD" in graph
    # Check that Bug Fix node is created once
    assert 'T_Bug_Fix["Bug Fix"]' in graph
    assert graph.count('T_Bug_Fix["Bug Fix"]') == 1
    
    # Check that action items are correctly sanitized and linked
    assert '["Fix error"]' in graph
    assert "['test']" in graph.replace("Add 'test'", "'test'") or "Add 'test'" in graph
    assert '["Deploy fix"]' in graph
    
    # Ensure there are 3 action links (2 from first record, 1 from fourth)
    assert graph.count("T_Bug_Fix --> A_") == 3

@patch("scripts.knowledge_graph.REVIEWS_DIR")
def test_generate_knowledge_graph_empty(mock_reviews_dir_patch):
    mock_reviews_dir_patch.exists.return_value = False
    graph = generate_knowledge_graph()
    assert "No records found" in graph

@patch("scripts.knowledge_graph.REVIEWS_DIR")
def test_generate_knowledge_graph_no_active(mock_reviews_dir_patch, tmp_path):
    mock_reviews_dir_patch.exists.return_value = True
    
    reviews_dir = tmp_path / "reviews"
    reviews_dir.mkdir()
    
    record = {
        "status": "archived",
        "task_type": "Feature",
        "action_items": ["Do something"]
    }
    (reviews_dir / "1.json").write_text(json.dumps(record))
    
    def mock_glob(pattern):
        return reviews_dir.glob(pattern)
    mock_reviews_dir_patch.glob.side_effect = mock_glob
    
    graph = generate_knowledge_graph()
    assert "No active records found" in graph
