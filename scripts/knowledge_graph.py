import json
import sys
import re
from pathlib import Path

# Ensure we can import from the same directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import REVIEWS_DIR

def sanitize_id(text):
    """Sanitize text to be used as a Mermaid node ID"""
    if not text:
        return "Unknown"
    # Replace non-alphanumeric characters with underscore
    sanitized = re.sub(r'[^a-zA-Z0-9]', '_', text)
    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = "N_" + sanitized
    return sanitized

def sanitize_label(text):
    """Sanitize text to be used as a Mermaid node label"""
    if not text:
        return ""
    # Escape double quotes
    return text.replace('"', "'")

def generate_knowledge_graph():
    """
    Parse all active JSON records and create a Mermaid graph 
    linking task_type to action_items.
    """
    if not REVIEWS_DIR.exists():
        return "graph TD\n    Empty[\"No records found\"]"

    lines = ["graph TD"]
    
    # Track created nodes to avoid duplicates
    task_nodes = set()
    action_nodes = set()
    
    # We will use a counter for action nodes to guarantee unique IDs
    # since action items can be very long and have special characters
    action_counter = 0

    for file_path in REVIEWS_DIR.glob("*.json"):
        try:
            content = file_path.read_text(encoding="utf-8")
            record = json.loads(content)
            
            if record.get("status") != "active":
                continue
                
            task_type = record.get("task_type", "Unknown Task")
            action_items = record.get("action_items", [])
            
            if not action_items:
                continue
                
            task_id = f"T_{sanitize_id(task_type)}"
            
            if task_id not in task_nodes:
                lines.append(f'    {task_id}["{sanitize_label(task_type)}"]')
                task_nodes.add(task_id)
                
            for action in action_items:
                action_counter += 1
                action_id = f"A_{action_counter}"
                
                lines.append(f'    {action_id}["{sanitize_label(action)}"]')
                lines.append(f'    {task_id} --> {action_id}')
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)

    if len(lines) == 1:
        return "graph TD\n    Empty[\"No active records found\"]"

    return "\n".join(lines)

if __name__ == "__main__":
    graph = generate_knowledge_graph()
    print(graph)
