from mcp.server.fastmcp import FastMCP
import sys
import json
from pathlib import Path

# Add scripts directory to path to import existing modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from config import REVIEWS_DIR
from sync_global import pull_global_memory, push_global_memory, share_local_record
from manage_memory import load_record, save_record
from search_memory import search_index
from context_injector import inject_context
from memory_lifecycle import archive_stale_memories
from knowledge_graph import generate_knowledge_graph

# Create FastMCP server
mcp = FastMCP("dao-genesis")


@mcp.tool()
def search_reviews(query: str, limit: int = 5,
                   include_archived: bool = False) -> str:
    """
    Search the review memory records.

    Args:
        query: Search keywords.
        limit: Maximum number of results to return.
        include_archived: Whether to include archived records in the search.

    Returns:
        A formatted string of matching records.
    """
    try:
        results = search_index(
            query,
            limit=limit,
            include_archived=include_archived)
        if not results:
            return "No matching records found."

        output = [f"Found {len(results)} matching record(s):\n"]
        for i, entry in enumerate(results, 1):
            review_id = entry.get("review_id", "Unknown")
            status_tag = f" [{entry.get('status')}]" if entry.get(
                "status") != "active" else ""
            output.append(
                f"{i}. {review_id}{status_tag} ({
                    entry.get(
                        'timestamp',
                        'Unknown Date')})")
            output.append(f"   Task: {entry.get('task_type', 'N/A')}")

            conclusions = entry.get("conclusions", [])
            if conclusions:
                output.append(f"   Conclusion: {conclusions[0]}")

            actions = entry.get("action_items", [])
            if actions:
                output.append(f"   Action: {actions[0]}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        return f"Error searching records: {str(e)}"


@mcp.tool()
def get_review(review_id: str) -> dict:
    """
    Get the full details of a specific review record.

    Args:
        review_id: The ID of the review record (e.g., REV-20260417-001).

    Returns:
        The full review record data.
    """
    try:
        return load_record(review_id, REVIEWS_DIR)
    except Exception as e:
        return {"error": f"Failed to load record {review_id}: {str(e)}"}


@mcp.tool()
def update_review(review_id: str, field: str, value: str,
                  append: bool = False) -> str:
    """
    Update a specific field in a review record.

    Args:
        review_id: The ID of the review record.
        field: The field to update (e.g., 'action_items', 'decisions').
        value: The new value to set or append.
        append: If true, appends to an array field instead of overwriting.

    Returns:
        Status message indicating success or failure.
    """
    array_fields = {
        "participants",
        "decisions",
        "success_factors",
        "failure_reasons",
        "best_practices",
        "action_items",
        "tags"}
    string_fields = {"task_type", "status"}

    if field not in array_fields and field not in string_fields:
        return f"Error: Field '{field}' is not allowed to be updated."

    if field in string_fields and append:
        return f"Error: Cannot append to a string field '{field}'."

    try:
        data = load_record(review_id, REVIEWS_DIR)

        if field in array_fields:
            if field not in data or not isinstance(data[field], list):
                data[field] = []
            if append:
                data[field].append(value)
                action = "新增"
            else:
                data[field] = [value]
                action = "修改"
        else:
            data[field] = value
            action = "修改"

        save_record(review_id, data, REVIEWS_DIR)
        return f"Successfully updated {review_id}: {field} [{action}] {value}"
    except Exception as e:
        return f"Failed to update {review_id}: {str(e)}"


@mcp.tool()
def archive_review(review_id: str) -> str:
    """
    Archive a memory record so it no longer appears in default searches.

    Args:
        review_id: The ID of the review record to archive.

    Returns:
        Status message indicating success or failure.
    """
    try:
        data = load_record(review_id, REVIEWS_DIR)
        if data.get("status") == "archived":
            return f"[{review_id}] is already archived."

        data["status"] = "archived"
        save_record(review_id, data, REVIEWS_DIR)
        return f"Successfully archived [{review_id}]."
    except Exception as e:
        return f"Failed to archive {review_id}: {str(e)}"


@mcp.tool()
def pull_global() -> str:
    """
    Pull the latest global memory records from the remote repository.

    Returns:
        Status message.
    """
    try:
        msg = pull_global_memory()
        return msg
    except Exception as e:
        return f"Error pulling global memory: {str(e)}"


@mcp.tool()
def push_global() -> str:
    """
    Push local changes in the global memory to the remote repository.

    Returns:
        Status message.
    """
    try:
        msg = push_global_memory()
        return msg
    except Exception as e:
        return f"Error pushing global memory: {str(e)}"


@mcp.tool()
def share_record_to_global(review_id: str) -> str:
    """
    Share a local review record to the global memory repository.

    Args:
        review_id: The ID of the local review record.

    Returns:
        Status message.
    """
    try:
        msg = share_local_record(review_id)
        return msg
    except Exception as e:
        return f"Error sharing record to global memory: {str(e)}"


@mcp.tool()
def run_context_injection() -> str:
    """
    Run context injection by analyzing active files and returning related memories.

    Returns:
        JSON string containing matching memories.
    """
    try:
        results = inject_context()
        if not results:
            return "[]"
        return json.dumps(results, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error running context injection: {str(e)}"


@mcp.tool()
def run_archive_stale_memories(days: int = 365) -> str:
    """
    Archive memories older than a specified number of days.

    Args:
        days: Number of days before a memory is considered stale.

    Returns:
        Status message indicating how many records were archived.
    """
    try:
        count = archive_stale_memories(days)
        return f"Successfully archived {count} stale memories."
    except Exception as e:
        return f"Error archiving stale memories: {str(e)}"


@mcp.tool()
def get_knowledge_graph() -> str:
    """
    Generate a Mermaid knowledge graph of tasks and action items from active memory records.

    Returns:
        Mermaid graph as a string.
    """
    try:
        return generate_knowledge_graph()
    except Exception as e:
        return f"Error generating knowledge graph: {str(e)}"


if __name__ == "__main__":
    mcp.run()
