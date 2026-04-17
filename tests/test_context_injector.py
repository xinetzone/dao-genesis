import sys
from unittest.mock import patch, MagicMock
import pytest

from scripts.context_injector import get_active_files, extract_keywords, inject_context

@patch("subprocess.run")
def test_get_active_files(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "file1.py\ndir/file2.txt\n"
    mock_run.return_value = mock_result
    
    files = get_active_files()
    assert files == ["file1.py", "dir/file2.txt"]
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_get_active_files_error(mock_run):
    mock_run.side_effect = Exception("git error")
    
    files = get_active_files()
    assert files == []

def test_extract_keywords():
    files = ["src/main_app.py", "tests/test_utils.js"]
    keywords = extract_keywords(files)
    
    # "main", "app", "test", "utils" should be extracted
    assert "main" in keywords
    assert "app" in keywords
    assert "test" in keywords
    assert "utils" in keywords
    # "src" or "py" or "js" might not be in it because we extract from path.stem
    # wait, path.stem of src/main_app.py is main_app
    # test_utils.js -> test_utils
    # so we expect main, app, test, utils

@patch("scripts.context_injector.get_active_files")
@patch("scripts.context_injector.extract_keywords")
@patch("scripts.context_injector.search_index")
def test_inject_context(mock_search_index, mock_extract_keywords, mock_get_active_files):
    mock_get_active_files.return_value = ["file1.py"]
    mock_extract_keywords.return_value = ["keyword1", "keyword2"]
    mock_search_index.return_value = [{"id": "1", "content": "mock memory"}]
    
    results = inject_context()
    
    assert results == [{"id": "1", "content": "mock memory"}]
    mock_search_index.assert_called_once_with("keyword1 keyword2", limit=5)

@patch("scripts.context_injector.get_active_files")
def test_inject_context_no_files(mock_get_active_files):
    mock_get_active_files.return_value = []
    
    results = inject_context()
    assert results == []

@patch("scripts.context_injector.get_active_files")
@patch("scripts.context_injector.extract_keywords")
def test_inject_context_no_keywords(mock_extract_keywords, mock_get_active_files):
    mock_get_active_files.return_value = ["file1.py"]
    mock_extract_keywords.return_value = []
    
    results = inject_context()
    assert results == []
