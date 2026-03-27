#!/usr/bin/env python3
"""Publish a Markdown article to Mowen in one step.

Integrates: MD→JSON conversion + image upload + cover insertion + API publish.

Usage:
    python3 publish_to_mowen.py article.md
    python3 publish_to_mowen.py article.md --tags "AI,教程"
    python3 publish_to_mowen.py article.md --note-id xxx --cover-uuid yyy
    python3 publish_to_mowen.py article.md --cover path/to/cover.png

Environment:
    MOWEN_API_KEY  — required for image upload and API publish
                     (falls back to extracting from ~/.claude.json MCP config)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Import sibling modules
sys.path.insert(0, str(Path(__file__).parent))
from md2mowen import convert
from upload_to_mowen import upload_file


def get_api_key() -> str:
    """Get Mowen API key from env var or ~/.claude.json MCP config."""
    key = os.environ.get("MOWEN_API_KEY", "").strip()
    if key:
        return key

    # Try extracting from Claude MCP config
    claude_json = Path.home() / ".claude.json"
    if claude_json.exists():
        try:
            config = json.loads(claude_json.read_text())
            url = config.get("mcpServers", {}).get("mowen", {}).get("url", "")
            if url:
                params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                keys = params.get("key", [])
                if keys and keys[0]:
                    return keys[0]
        except (json.JSONDecodeError, KeyError):
            pass

    return ""


def get_mcp_url(api_key: str) -> str:
    """Build the MCP endpoint URL."""
    return f"https://open.mowen.cn/api/open/mcp/v1/note?key={api_key}"


def mcp_call(url: str, tool_name: str, arguments: dict) -> dict:
    """Make a JSON-RPC call to the Mowen MCP endpoint."""
    rpc = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    data = json.dumps(rpc).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if "error" in result:
        raise RuntimeError(f"MCP error: {result['error']}")

    # Extract text content from result
    content = result.get("result", {}).get("content", [])
    if content and content[0].get("type") == "text":
        return {"id": content[0]["text"]}

    return result.get("result", {})


def resolve_cover(article_path: Path, cover_arg: str | None) -> Path | None:
    """Find cover image: CLI arg > .assets/cover*."""
    if cover_arg:
        p = Path(cover_arg)
        if p.is_file():
            return p

    # Check <article>.assets/cover*
    assets_dir = article_path.parent / f"{article_path.stem}.assets"
    if assets_dir.is_dir():
        for pattern in ["cover.png", "cover.jpg", "cover.jpeg", "cover.webp"]:
            candidate = assets_dir / pattern
            if candidate.is_file():
                return candidate

    return None


def insert_cover_into_body(body: dict, cover_uuid: str) -> dict:
    """Insert cover image node after title (or after quote if present).

    Mowen uses the first image in body as the cover.
    """
    content = body.get("content", [])
    if not content:
        return body

    # Find insertion point: after title, or after quote if it follows title
    insert_at = 1
    if len(content) > 1 and content[1].get("type") == "quote":
        insert_at = 2

    cover_node = {
        "type": "image",
        "attrs": {"uuid": cover_uuid, "align": "center"},
    }
    content.insert(insert_at, cover_node)
    body["content"] = content
    return body


def process_images(body: dict, api_key: str, article_dir: Path) -> dict:
    """Upload local images and replace attrs with UUIDs."""
    content = body.get("content", [])
    for i, node in enumerate(content):
        if node.get("type") != "image":
            continue
        attrs = node.get("attrs", {})
        if not attrs.get("local", False):
            continue

        src = attrs.get("src", "")
        img_path = article_dir / src
        if not img_path.is_file():
            print(f"Warning: image not found: {img_path}", file=sys.stderr)
            continue

        try:
            result = upload_file(api_key, img_path)
            content[i] = {
                "type": "image",
                "attrs": {
                    "uuid": result["uuid"],
                    "align": "center",
                    "alt": attrs.get("alt", ""),
                },
            }
            print(f"Uploaded: {src} → {result['uuid']}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: failed to upload {src}: {e}", file=sys.stderr)

    body["content"] = content
    return body


def main():
    parser = argparse.ArgumentParser(
        description="Publish Markdown article to Mowen"
    )
    parser.add_argument("file", help="Markdown file path")
    parser.add_argument("--note-id", help="Existing note ID (for updates)")
    parser.add_argument("--cover-uuid", help="Existing cover image UUID")
    parser.add_argument("--cover", help="Cover image file path")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument(
        "--public", action="store_true", help="Set note as public after publishing"
    )
    args = parser.parse_args()

    # Validate input
    article_path = Path(args.file)
    if not article_path.is_file():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print(
            "Error: MOWEN_API_KEY not set and not found in ~/.claude.json",
            file=sys.stderr,
        )
        sys.exit(1)

    mcp_url = get_mcp_url(api_key)

    # Step 1: Convert markdown to Mowen JSON
    md_text = article_path.read_text(encoding="utf-8")
    body = convert(md_text)
    print(f"Converted: {len(body['content'])} blocks", file=sys.stderr)

    # Step 2: Upload local images
    body = process_images(body, api_key, article_path.parent)

    # Step 3: Handle cover image
    cover_uuid = args.cover_uuid
    if not cover_uuid:
        cover_path = resolve_cover(article_path, args.cover)
        if cover_path:
            try:
                result = upload_file(api_key, cover_path)
                cover_uuid = result["uuid"]
                print(f"Cover uploaded: {cover_path.name} → {cover_uuid}", file=sys.stderr)
            except Exception as e:
                print(f"Warning: cover upload failed: {e}", file=sys.stderr)

    if cover_uuid:
        body = insert_cover_into_body(body, cover_uuid)

    # Step 4: Publish or update
    body_json = json.dumps(body, ensure_ascii=False)

    if args.note_id:
        # Update existing note
        result = mcp_call(mcp_url, "EditRichNote", {
            "note_id": args.note_id,
            "body": body_json,
        })
        note_id = args.note_id
        print(f"Updated note: {note_id}", file=sys.stderr)
    else:
        # Create new note
        settings = {"auto_publish": True}
        if args.tags:
            settings["tags"] = [t.strip() for t in args.tags.split(",")]
        result = mcp_call(mcp_url, "CreateRichNote", {
            "body": body_json,
            "settings": json.dumps(settings),
        })
        note_id = result.get("id", "unknown")
        print(f"Created note: {note_id}", file=sys.stderr)

    # Step 5: Set public if requested
    if args.public:
        try:
            mcp_call(mcp_url, "ChangeNoteSettings", {
                "note_id": note_id,
                "settings": json.dumps({"section": 1}),
            })
            print("Set to public", file=sys.stderr)
        except Exception as e:
            print(f"Warning: failed to set public: {e}", file=sys.stderr)

    # Output result as JSON to stdout
    output = {"note_id": note_id}
    if cover_uuid:
        output["cover_uuid"] = cover_uuid
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
