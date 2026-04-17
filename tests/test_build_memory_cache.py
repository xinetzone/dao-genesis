from build_memory_cache import build_index
import json
import sys
from pathlib import Path

scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
sys.path.append(str(scripts_dir))


def test_build_memory_cache(tmp_path, monkeypatch, capsys):
    # Mock REVIEWS_DIR and CACHE_REVIEWS_DIR
    reviews_dir = tmp_path / ".storage" / "reviews"
    cache_dir = tmp_path / ".cache" / "reviews"

    reviews_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("build_memory_cache.REVIEWS_DIR", reviews_dir)
    monkeypatch.setattr("build_memory_cache.CACHE_REVIEWS_DIR", cache_dir)

    # Create sample review
    sample_data = {
        "review_id": "REV-20260417-001",
        "timestamp": "2026-04-17T10:00:00Z",
        "task_type": "Test",
        "status": "active",
        "decisions": ["D1"],
        "success_factors": ["S1"],
        "failure_reasons": ["F1"],
        "action_items": ["A1", "A2", "A3"]
    }

    (reviews_dir / "REV-20260417-001.json").write_text(json.dumps(sample_data), encoding="utf-8")

    # Run build_index
    build_index()

    # Verify index created
    index_file = cache_dir / "search_index.json"
    assert index_file.exists()

    index_data = json.loads(index_file.read_text(encoding="utf-8"))
    assert len(index_data) == 1

    entry = index_data[0]
    assert entry["review_id"] == "REV-20260417-001"
    assert entry["conclusions"] == ["D1", "S1", "F1"]
    assert entry["action_items"] == ["A1", "A2"]  # Sliced to 2
