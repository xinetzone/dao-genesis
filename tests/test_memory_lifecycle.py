import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

import pytest

from scripts.memory_lifecycle import archive_stale_memories

@pytest.fixture
def mock_reviews_dir(tmp_path):
    # Create a temporary reviews directory with some JSON files
    reviews_dir = tmp_path / "reviews"
    reviews_dir.mkdir()
    
    now = datetime.now(timezone.utc)
    
    # 1. Old record (should be archived)
    old_date = now - timedelta(days=400)
    old_record = {
        "status": "active",
        "timestamp": old_date.isoformat()
    }
    (reviews_dir / "old.json").write_text(json.dumps(old_record))
    
    # 2. Recent record (should not be archived)
    recent_date = now - timedelta(days=100)
    recent_record = {
        "status": "active",
        "timestamp": recent_date.isoformat()
    }
    (reviews_dir / "recent.json").write_text(json.dumps(recent_record))
    
    # 3. Already archived record
    archived_date = now - timedelta(days=400)
    archived_record = {
        "status": "archived",
        "timestamp": archived_date.isoformat()
    }
    (reviews_dir / "archived.json").write_text(json.dumps(archived_record))
    
    # 4. Invalid record (no timestamp)
    invalid_record = {
        "status": "active"
    }
    (reviews_dir / "invalid.json").write_text(json.dumps(invalid_record))
    
    return reviews_dir

@patch("scripts.memory_lifecycle.REVIEWS_DIR")
def test_archive_stale_memories(mock_reviews_dir_patch, mock_reviews_dir):
    # Point REVIEWS_DIR to our temporary directory
    mock_reviews_dir_patch.exists.return_value = True
    mock_reviews_dir_patch.glob.side_effect = mock_reviews_dir.glob
    
    count = archive_stale_memories(days=365)
    
    assert count == 1
    
    # Verify the old record was archived
    old_content = json.loads((mock_reviews_dir / "old.json").read_text())
    assert old_content["status"] == "archived"
    
    # Verify the recent record is still active
    recent_content = json.loads((mock_reviews_dir / "recent.json").read_text())
    assert recent_content["status"] == "active"
    
@patch("scripts.memory_lifecycle.REVIEWS_DIR")
def test_archive_stale_memories_no_dir(mock_reviews_dir_patch):
    mock_reviews_dir_patch.exists.return_value = False
    
    count = archive_stale_memories()
    assert count == 0