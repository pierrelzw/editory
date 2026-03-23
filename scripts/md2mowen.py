#!/usr/bin/env python3
"""Markdown to Mowen JSON converter.

Converts Markdown text into Mowen's ProseMirror/TipTap JSON format
using markdown-it-py for parsing.

Usage:
    python3 scripts/md2mowen.py article.md          # compact JSON to stdout
    python3 scripts/md2mowen.py article.md --pretty  # formatted output
    python3 scripts/md2mowen.py -                    # read from stdin
"""

import json
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter from the beginning of text."""
    return re.sub(r"\A---\n.*?\n---\n?", "", text, count=1, flags=re.DOTALL)


def _parse_inline_tokens(tokens: list) -> list:
    """Convert inline tokens to Mowen text nodes with marks."""
    nodes = []
    marks_stack = []

    for token in tokens:
        if token.type == "text":
            node = {"type": "text", "text": token.content}
            if marks_stack:
                node["marks"] = [m.copy() for m in marks_stack]
            nodes.append(node)

        elif token.type == "code_inline":
            # code mark not supported by Mowen, keep backticks as plain text
            node = {"type": "text", "text": f"`{token.content}`"}
            if marks_stack:
                node["marks"] = [m.copy() for m in marks_stack]
            nodes.append(node)

        elif token.type == "softbreak":
            node = {"type": "text", "text": "\n"}
            if marks_stack:
                node["marks"] = [m.copy() for m in marks_stack]
            nodes.append(node)

        elif token.type == "strong_open":
            marks_stack.append({"type": "bold"})

        elif token.type == "strong_close":
            marks_stack[:] = [m for m in marks_stack if m["type"] != "bold"]

        elif token.type == "em_open":
            marks_stack.append({"type": "bold"})

        elif token.type == "em_close":
            marks_stack[:] = [m for m in marks_stack if m["type"] != "bold"]

        elif token.type == "link_open":
            href = token.attrGet("href") or ""
            marks_stack.append({"type": "link", "attrs": {"href": href}})

        elif token.type == "link_close":
            marks_stack[:] = [m for m in marks_stack if m["type"] != "link"]

        elif token.type == "image":
            # images in inline context are handled at block level
            pass

    return nodes


def _parse_inline_to_nodes(token) -> list:
    """Parse an inline token's children into Mowen text nodes."""
    if token.children:
        return _parse_inline_tokens(token.children)
    if token.content:
        return [{"type": "text", "text": token.content}]
    return []


def _collect_blockquote_content(tokens: list, start: int) -> tuple:
    """Collect all content within a blockquote, handling nesting.

    Returns (nodes_list, end_index) where nodes_list is a list of text nodes
    and end_index is the index after blockquote_close.
    """
    all_nodes = []
    depth = 1
    i = start

    while i < len(tokens) and depth > 0:
        tok = tokens[i]
        if tok.type == "blockquote_open":
            depth += 1
        elif tok.type == "blockquote_close":
            depth -= 1
            if depth == 0:
                return all_nodes, i + 1
        elif tok.type == "inline":
            if all_nodes:
                all_nodes.append({"type": "text", "text": "\n"})
            all_nodes.extend(_parse_inline_to_nodes(tok))
        i += 1

    return all_nodes, i


def convert(markdown_text: str) -> dict:
    """Convert Markdown text to Mowen doc JSON."""
    text = strip_frontmatter(markdown_text)
    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(text)

    blocks = []
    i = 0
    list_depth = 0
    ordered_counters = []  # stack of counters for ordered lists

    while i < len(tokens):
        tok = tokens[i]

        # Headings → bold paragraph
        if tok.type == "heading_open":
            # next token is inline content
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                inline_tok = tokens[i + 1]
                nodes = _parse_inline_to_nodes(inline_tok)
                # apply bold mark to all text nodes
                for node in nodes:
                    existing = node.get("marks", [])
                    if not any(m["type"] == "bold" for m in existing):
                        existing.insert(0, {"type": "bold"})
                    node["marks"] = existing
                blocks.append({"type": "paragraph", "content": nodes})
                i += 3  # skip heading_open, inline, heading_close
                continue

        # Paragraphs
        elif tok.type == "paragraph_open":
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                inline_tok = tokens[i + 1]

                # Check for images in the inline token
                if inline_tok.children:
                    has_image = any(
                        c.type == "image" for c in inline_tok.children
                    )
                    if has_image:
                        # Process mixed content: text and images
                        text_nodes = []
                        for child in inline_tok.children:
                            if child.type == "image":
                                # Flush accumulated text as paragraph
                                if text_nodes:
                                    blocks.append(
                                        {
                                            "type": "paragraph",
                                            "content": text_nodes,
                                        }
                                    )
                                    text_nodes = []
                                # Add image block
                                src = child.attrGet("src") or ""
                                alt = child.attrGet("alt") or child.content or ""
                                is_local = not src.startswith(
                                    ("http://", "https://")
                                )
                                blocks.append(
                                    {
                                        "type": "image",
                                        "attrs": {
                                            "src": src,
                                            "local": is_local,
                                            "alt": alt,
                                        },
                                    }
                                )
                            else:
                                # Accumulate non-image tokens
                                parsed = _parse_inline_tokens([child])
                                text_nodes.extend(parsed)
                        if text_nodes:
                            blocks.append(
                                {"type": "paragraph", "content": text_nodes}
                            )
                        i += 3  # skip paragraph_open, inline, paragraph_close
                        continue

                nodes = _parse_inline_to_nodes(inline_tok)
                if nodes:
                    blocks.append({"type": "paragraph", "content": nodes})
                else:
                    blocks.append({"type": "paragraph"})
                i += 3
                continue

        # Code blocks
        elif tok.type == "fence":
            lang = tok.info.strip() if tok.info else ""
            content = tok.content.rstrip("\n")
            block = {"type": "codeblock"}
            if lang:
                block["attrs"] = {"language": lang}
            if content:
                block["content"] = [{"type": "text", "text": content}]
            blocks.append(block)
            i += 1
            continue

        elif tok.type == "code_block":
            content = tok.content.rstrip("\n")
            block = {"type": "codeblock"}
            if content:
                block["content"] = [{"type": "text", "text": content}]
            blocks.append(block)
            i += 1
            continue

        # Blockquotes
        elif tok.type == "blockquote_open":
            nodes, end_i = _collect_blockquote_content(tokens, i + 1)
            block = {"type": "quote"}
            if nodes:
                block["content"] = nodes
            blocks.append(block)
            i = end_i
            continue

        # Lists
        elif tok.type == "bullet_list_open":
            list_depth += 1
            i += 1
            continue

        elif tok.type == "bullet_list_close":
            list_depth -= 1
            i += 1
            continue

        elif tok.type == "ordered_list_open":
            list_depth += 1
            ordered_counters.append(0)
            i += 1
            continue

        elif tok.type == "ordered_list_close":
            list_depth -= 1
            if ordered_counters:
                ordered_counters.pop()
            i += 1
            continue

        elif tok.type == "list_item_open":
            # Determine prefix
            indent = "  " * max(0, list_depth - 1)
            if ordered_counters:
                ordered_counters[-1] += 1
                prefix = f"{indent}{ordered_counters[-1]}. "
            else:
                prefix = f"{indent}· "

            # Collect inline content from this list item
            j = i + 1
            item_depth = 1
            item_nodes = []
            while j < len(tokens) and item_depth > 0:
                t = tokens[j]
                if t.type == "list_item_open":
                    break  # nested items handled by list_open/close
                if t.type == "list_item_close":
                    item_depth -= 1
                    if item_depth == 0:
                        break
                if t.type in (
                    "bullet_list_open",
                    "ordered_list_open",
                ):
                    break  # let the outer loop handle nested lists
                if t.type == "inline":
                    item_nodes = _parse_inline_to_nodes(t)
                j += 1

            if item_nodes:
                # Prepend the prefix to the first text node
                first = item_nodes[0]
                if first["type"] == "text":
                    item_nodes[0] = {**first, "text": prefix + first["text"]}
                    blocks.append(
                        {"type": "paragraph", "content": item_nodes}
                    )
                else:
                    prefix_node = {"type": "text", "text": prefix}
                    blocks.append(
                        {
                            "type": "paragraph",
                            "content": [prefix_node] + item_nodes,
                        }
                    )
            # Advance past all scanned tokens (j points at list_item_close
            # or a nested list/item boundary)
            i = j
            continue

        # Horizontal rule
        elif tok.type == "hr":
            blocks.append({"type": "paragraph"})
            i += 1
            continue

        # Tables
        elif tok.type == "table_open":
            # Collect table rows
            j = i + 1
            rows = []
            current_row = []
            is_header = False
            while j < len(tokens) and tokens[j].type != "table_close":
                t = tokens[j]
                if t.type == "thead_open":
                    is_header = True
                elif t.type == "thead_close":
                    is_header = False
                elif t.type == "tr_open":
                    current_row = []
                elif t.type == "tr_close":
                    rows.append((is_header, current_row))
                    current_row = []
                elif t.type == "inline":
                    current_row.append(t.content)
                j += 1

            for is_hdr, cells in rows:
                text = " | ".join(cells)
                node = {"type": "text", "text": text}
                if is_hdr:
                    node["marks"] = [{"type": "bold"}]
                blocks.append({"type": "paragraph", "content": [node]})

            i = j + 1  # skip past table_close
            continue

        i += 1

    # Insert empty paragraphs between blocks for spacing
    if blocks:
        spaced = [blocks[0]]
        for b in blocks[1:]:
            spaced.append({"type": "paragraph"})
            spaced.append(b)
        blocks = spaced

    return {"type": "doc", "content": blocks if blocks else [{"type": "paragraph"}]}


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert Markdown to Mowen JSON"
    )
    parser.add_argument(
        "file", help="Markdown file path, or - for stdin"
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output"
    )
    args = parser.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.file).read_text(encoding="utf-8")

    doc = convert(text)
    indent = 2 if args.pretty else None
    print(json.dumps(doc, ensure_ascii=False, indent=indent))


if __name__ == "__main__":
    main()
