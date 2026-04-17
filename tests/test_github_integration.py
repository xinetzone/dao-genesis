import os
import json
import urllib.error
from unittest.mock import patch, MagicMock, mock_open
import pytest

from scripts.github_integration import main

@patch("os.environ.get")
@patch("urllib.request.urlopen")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("sys.exit")
def test_github_integration_success(mock_exit, mock_makedirs, mock_open_file, mock_urlopen, mock_env):
    # Mock environment variables
    def env_get(key, default=None):
        envs = {
            "GITHUB_TOKEN": "fake_token",
            "GITHUB_REPOSITORY": "fake/repo",
            "PR_NUMBER": "123"
        }
        return envs.get(key, default)
    mock_env.side_effect = env_get

    # Mock urllib.request.urlopen responses
    # First call: PR JSON
    mock_response_pr = MagicMock()
    mock_response_pr.read.return_value = json.dumps({"user": {"login": "test_user"}}).encode("utf-8")
    
    # Second call: PR Diff
    mock_response_diff = MagicMock()
    mock_response_diff.read.return_value = b"diff --git a/file.py b/file.py\n+ print('hello')"
    
    # Third call: Comments JSON
    mock_response_comments = MagicMock()
    mock_response_comments.read.return_value = json.dumps([]).encode("utf-8")
    
    # Fourth call: Post Comment
    mock_response_post = MagicMock()
    mock_response_post.status = 201
    
    mock_urlopen.side_effect = [
        MagicMock(__enter__=lambda _: mock_response_pr, __exit__=lambda *args: None),
        MagicMock(__enter__=lambda _: mock_response_diff, __exit__=lambda *args: None),
        MagicMock(__enter__=lambda _: mock_response_comments, __exit__=lambda *args: None),
        MagicMock(__enter__=lambda _: mock_response_post, __exit__=lambda *args: None)
    ]

    # Run the main function
    main()

    # Verify that os.makedirs was called to create the reviews directory
    mock_makedirs.assert_called_with(os.path.join(".storage", "reviews"), exist_ok=True)
    
    # Verify that a file was opened to write the review
    mock_open_file.assert_called_once()
    
    # Verify that sys.exit was not called
    mock_exit.assert_not_called()

@patch("os.environ.get")
@patch("sys.exit")
def test_github_integration_missing_env(mock_exit, mock_env):
    # Mock missing environment variables
    mock_env.return_value = None
    mock_exit.side_effect = SystemExit(1)

    with pytest.raises(SystemExit):
        main()

    # Verify that sys.exit was called with 1
    mock_exit.assert_called_once_with(1)
