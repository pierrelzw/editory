"""Tests for md2mowen.py — Markdown to Mowen JSON converter."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from md2mowen import convert, strip_frontmatter


# --- Frontmatter ---


class TestFrontmatter:
    def test_strip_frontmatter(self):
        text = "---\ntitle: Hello\ntags: [a, b]\n---\nContent here"
        assert strip_frontmatter(text) == "Content here"

    def test_no_frontmatter(self):
        text = "Just content"
        assert strip_frontmatter(text) == "Just content"

    def test_frontmatter_in_convert(self):
        md = "---\ntitle: Test\n---\nHello world"
        doc = convert(md)
        content = doc["content"]
        text_blocks = [b for b in content if b.get("content")]
        assert any(
            n["text"] == "Hello world"
            for b in text_blocks
            for n in b.get("content", [])
            if n.get("text")
        )


# --- Headings ---


class TestHeadings:
    def test_h1(self):
        doc = convert("# Title")
        block = doc["content"][0]
        assert block["type"] == "paragraph"
        assert block["content"][0]["text"] == "Title"
        assert {"type": "bold"} in block["content"][0]["marks"]

    def test_h2(self):
        doc = convert("## Subtitle")
        block = doc["content"][0]
        assert block["content"][0]["text"] == "Subtitle"
        assert {"type": "bold"} in block["content"][0]["marks"]

    def test_h3(self):
        doc = convert("### Section")
        block = doc["content"][0]
        assert {"type": "bold"} in block["content"][0]["marks"]

    def test_h4(self):
        doc = convert("#### Subsection")
        block = doc["content"][0]
        assert {"type": "bold"} in block["content"][0]["marks"]


# --- Paragraphs and inline ---


class TestParagraphs:
    def test_plain_text(self):
        doc = convert("Hello world")
        block = doc["content"][0]
        assert block["type"] == "paragraph"
        assert block["content"][0]["text"] == "Hello world"
        assert "marks" not in block["content"][0]

    def test_bold(self):
        doc = convert("This is **bold** text")
        block = doc["content"][0]
        nodes = block["content"]
        bold_nodes = [n for n in nodes if "marks" in n and any(m["type"] == "bold" for m in n["marks"])]
        assert len(bold_nodes) == 1
        assert bold_nodes[0]["text"] == "bold"

    def test_inline_code_as_backticks(self):
        doc = convert("Use `foo()` here")
        block = doc["content"][0]
        texts = "".join(n["text"] for n in block["content"])
        assert "`foo()`" in texts

    def test_link(self):
        doc = convert("Click [here](https://example.com) now")
        block = doc["content"][0]
        link_nodes = [
            n for n in block["content"]
            if "marks" in n and any(m["type"] == "link" for m in n["marks"])
        ]
        assert len(link_nodes) == 1
        assert link_nodes[0]["text"] == "here"
        link_mark = next(m for m in link_nodes[0]["marks"] if m["type"] == "link")
        assert link_mark["attrs"]["href"] == "https://example.com"

    def test_mixed_formatting(self):
        doc = convert("Normal **bold** and [link](http://x.com) and `code`")
        block = doc["content"][0]
        texts = "".join(n["text"] for n in block["content"])
        assert "bold" in texts
        assert "link" in texts
        assert "`code`" in texts


# --- Blockquotes ---


class TestBlockquotes:
    def test_single_paragraph(self):
        doc = convert("> This is a quote")
        # find quote block
        quotes = [b for b in doc["content"] if b["type"] == "quote"]
        assert len(quotes) == 1
        assert quotes[0]["content"][0]["text"] == "This is a quote"

    def test_multi_paragraph(self):
        doc = convert("> First line\n>\n> Second line")
        quotes = [b for b in doc["content"] if b["type"] == "quote"]
        assert len(quotes) == 1
        texts = [n["text"] for n in quotes[0]["content"]]
        combined = "".join(texts)
        assert "First line" in combined
        assert "Second line" in combined

    def test_with_inline_formatting(self):
        doc = convert("> This is **bold** in quote")
        quotes = [b for b in doc["content"] if b["type"] == "quote"]
        assert len(quotes) == 1
        bold_nodes = [
            n for n in quotes[0]["content"]
            if "marks" in n and any(m["type"] == "bold" for m in n["marks"])
        ]
        assert len(bold_nodes) >= 1


# --- Code blocks ---


class TestCodeBlocks:
    def test_with_language(self):
        doc = convert("```python\nprint('hello')\n```")
        codes = [b for b in doc["content"] if b["type"] == "codeblock"]
        assert len(codes) == 1
        assert codes[0]["attrs"]["language"] == "python"
        assert codes[0]["content"][0]["text"] == "print('hello')"

    def test_without_language(self):
        doc = convert("```\nsome code\n```")
        codes = [b for b in doc["content"] if b["type"] == "codeblock"]
        assert len(codes) == 1
        assert "attrs" not in codes[0] or "language" not in codes[0].get("attrs", {})


# --- Images ---


class TestImages:
    def test_local_image(self):
        doc = convert("![alt text](images/photo.png)")
        images = [b for b in doc["content"] if b["type"] == "image"]
        assert len(images) == 1
        assert images[0]["attrs"]["src"] == "images/photo.png"
        assert images[0]["attrs"]["local"] is True
        assert images[0]["attrs"]["alt"] == "alt text"

    def test_url_image(self):
        doc = convert("![desc](https://example.com/img.jpg)")
        images = [b for b in doc["content"] if b["type"] == "image"]
        assert len(images) == 1
        assert images[0]["attrs"]["src"] == "https://example.com/img.jpg"
        assert images[0]["attrs"]["local"] is False


# --- Lists ---


class TestLists:
    def test_unordered_flat(self):
        doc = convert("- Item A\n- Item B\n- Item C")
        paragraphs = [b for b in doc["content"] if b["type"] == "paragraph" and b.get("content")]
        texts = [b["content"][0]["text"] for b in paragraphs]
        assert any("· Item A" in t for t in texts)
        assert any("· Item B" in t for t in texts)
        assert any("· Item C" in t for t in texts)

    def test_ordered_flat(self):
        doc = convert("1. First\n2. Second\n3. Third")
        paragraphs = [b for b in doc["content"] if b["type"] == "paragraph" and b.get("content")]
        texts = [b["content"][0]["text"] for b in paragraphs]
        assert any("1. First" in t for t in texts)
        assert any("2. Second" in t for t in texts)
        assert any("3. Third" in t for t in texts)

    def test_nested_unordered(self):
        md = "- Parent\n  - Child\n  - Child 2"
        doc = convert(md)
        paragraphs = [b for b in doc["content"] if b["type"] == "paragraph" and b.get("content")]
        texts = [b["content"][0]["text"] for b in paragraphs]
        # child items should have indentation
        assert any("  · " in t for t in texts)


# --- Tables ---


class TestTables:
    def test_basic_table(self):
        md = "| Name | Age |\n|---|---|\n| Alice | 30 |\n| Bob | 25 |"
        doc = convert(md)
        paragraphs = [b for b in doc["content"] if b["type"] == "paragraph" and b.get("content")]
        # header row should be bold
        header = paragraphs[0]
        assert any(m["type"] == "bold" for m in header["content"][0].get("marks", []))
        assert "Name" in header["content"][0]["text"]


# --- Spacing ---


class TestSpacing:
    def test_empty_paragraphs_between_blocks(self):
        doc = convert("First paragraph\n\nSecond paragraph")
        # should have: para, empty, para
        assert len(doc["content"]) == 3
        assert doc["content"][1] == {"type": "paragraph"}


# --- Horizontal rule ---


class TestHorizontalRule:
    def test_hr_becomes_empty_paragraph(self):
        doc = convert("Above\n\n---\n\nBelow")
        # should contain empty paragraphs (at least one from hr)
        empty = [b for b in doc["content"] if b == {"type": "paragraph"}]
        assert len(empty) >= 1


# --- End-to-end ---


class TestEndToEnd:
    def test_full_article(self):
        md = """---
title: Test Article
tags: [test]
---

# Introduction

This is a **test** article with [a link](https://example.com).

> Important quote here

```python
def hello():
    print("world")
```

## List Section

- Item one
- Item two
- Item three

![cover](cover.png)

---

Final paragraph.
"""
        doc = convert(md)
        assert doc["type"] == "doc"
        assert len(doc["content"]) > 0

        types = [b["type"] for b in doc["content"]]
        assert "paragraph" in types
        assert "codeblock" in types
        assert "quote" in types
        assert "image" in types


# --- CLI ---


class TestCLI:
    def test_stdin(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "md2mowen.py"), "-"],
            input="Hello **world**",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        doc = json.loads(result.stdout)
        assert doc["type"] == "doc"

    def test_pretty_flag(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("# Title\n\nContent")
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "md2mowen.py"), str(md_file), "--pretty"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "\n" in result.stdout  # pretty-printed has newlines
        doc = json.loads(result.stdout)
        assert doc["type"] == "doc"
