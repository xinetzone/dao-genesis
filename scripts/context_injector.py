import subprocess
import sys
import re
from pathlib import Path

# Ensure we can import from the same directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_memory import search_index

def get_active_files():
    try:
        # Use git diff to find modified files relative to HEAD
        # Also include untracked files
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--modified', '--exclude-standard'],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]
    except Exception as e:
        print(f"Error getting active files: {e}", file=sys.stderr)
        return []

def extract_keywords(files):
    keywords = set()
    for file in files:
        path = Path(file)
        name = path.stem
        # Split by non-alphanumeric characters
        words = re.split(r'[^a-zA-Z0-9]+', name)
        for word in words:
            if len(word) > 2:  # Ignore very short words
                keywords.add(word)
    return list(keywords)

def inject_context():
    """
    Find active files, extract keywords, and return related memories.
    """
    files = get_active_files()
    if not files:
        return []
    
    keywords = extract_keywords(files)
    if not keywords:
        return []
    
    query = " ".join(keywords)
    results = search_index(query, limit=5)
    return results

if __name__ == "__main__":
    import json
    results = inject_context()
    print(json.dumps(results, indent=2, ensure_ascii=False))
