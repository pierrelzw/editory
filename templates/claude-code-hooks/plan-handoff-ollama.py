#!/usr/bin/env python3
"""
Claude Code hook: on a trigger prompt (e.g. `/go`) during plan->execute,
read the session transcript, extract the latest assistant "plan" text,
translate it to English via local Ollama, then inject as additionalContext.

This does NOT replace the user prompt text. It appends English context so
Claude can treat the English handoff as authoritative during execution.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional


def _read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def _safe_get(d: dict[str, Any], key: str, default=None):
    v = d.get(key, default)
    return v if v is not None else default


def _is_probably_zh(text: str) -> bool:
    # Fast heuristic: any CJK Unified Ideographs.
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def _strip_command_prefix(prompt: str) -> str:
    # Allow: "/go" or "/go ..." where "... " contains extra instructions.
    if prompt.startswith("/go"):
        rest = prompt[3:].lstrip()
        return rest
    return prompt


def _iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _extract_assistant_text(message_obj: dict[str, Any]) -> str:
    """
    Transcript message format in Claude Code jsonl usually looks like:
      {"type":"assistant", "message": {"role":"assistant","content":[{"type":"text","text":"..."}]}}
    We take only "text" segments (ignore "thinking", "tool_use", etc).
    """
    msg = message_obj.get("message") or {}
    if msg.get("role") != "assistant":
        return ""
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "text" and isinstance(item.get("text"), str):
            parts.append(item["text"])
    return "\n".join([p for p in parts if p.strip()]).strip()


def _latest_assistant_text(transcript_path: Path, max_scan: int = 5000) -> str:
    # Scan from the end is ideal but jsonl is line-based; keep it simple:
    # read all lines but cap by last N parsed messages.
    msgs: list[str] = []
    for obj in _iter_jsonl(transcript_path):
        if obj.get("type") != "assistant":
            continue
        text = _extract_assistant_text(obj)
        if text:
            msgs.append(text)
            if len(msgs) > max_scan:
                msgs = msgs[-max_scan:]
    return msgs[-1] if msgs else ""


def _ollama_translate(zh_text: str, model: str) -> str:
    instruction = (
        "Translate the following Chinese text into English.\n"
        "Rules:\n"
        "- Preserve code identifiers, file paths, API names, URLs, and shell commands exactly.\n"
        "- Keep Markdown structure (headings/lists/code blocks) intact.\n"
        "- Output ONLY the English translation, no preface.\n"
        "\n"
        "Chinese text:\n"
        f"{zh_text}\n"
    )
    env = os.environ.copy()
    # Keep output readable for injection.
    cmd = ["ollama", "run", model, instruction]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = (p.stdout or "").strip()
    if p.returncode != 0 or not out:
        err = (p.stderr or "").strip()
        raise RuntimeError(f"ollama failed (code={p.returncode}): {err}")
    return out


def _should_skip_for_writing(prompt: str) -> bool:
    # Let users explicitly mark writing tasks.
    if prompt.lstrip().startswith("@write"):
        return True
    # Heuristic fallback keywords.
    return bool(re.search(r"(润色|改写|写作|文章|文案|小红书|公众号|标题党|排版)", prompt))


def main() -> int:
    hook_input = _read_stdin_json()

    prompt = str(_safe_get(hook_input, "prompt", "")).strip()
    permission_mode = str(_safe_get(hook_input, "permission_mode", "")).strip()
    transcript_path_raw = _safe_get(hook_input, "transcript_path", "")

    # Only trigger on an explicit command to avoid latency on every prompt.
    if not prompt.startswith("/go"):
        return 0

    # If the user is doing a writing task, skip translation injection.
    if _should_skip_for_writing(prompt):
        return 0

    transcript_path = Path(str(transcript_path_raw)) if transcript_path_raw else None
    if not transcript_path or not transcript_path.exists():
        # Fail open: do not block the run.
        print(json.dumps({"decision": "approve"}))
        return 0

    latest = _latest_assistant_text(transcript_path)
    if not latest or not _is_probably_zh(latest):
        # Nothing to translate (or already English).
        return 0

    # Optional: allow extra instructions after /go to be included (still English).
    go_extra = _strip_command_prefix(prompt)

    model = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b-instruct").strip() or "qwen2.5:14b-instruct"
    try:
        en = _ollama_translate(latest, model=model)
    except Exception as e:
        # Fail open: approve, but annotate the failure for visibility.
        print(
            json.dumps(
                {
                    "decision": "approve",
                    "additionalContext": f"[handoff] Ollama translation failed: {e}",
                }
            )
        )
        return 0

    injected = (
        "[handoff] English Execution Brief (translated from the latest plan)\n\n"
        f"{en}\n"
    )
    injected += (
        "\n[handoff] Instruction: Use the English brief above as the authoritative plan for execution. "
        "If it conflicts with earlier Chinese text, ask the user for clarification.\n"
    )
    if go_extra:
        injected += "\n[handoff] Extra execution notes from the user:\n\n" + go_extra + "\n"

    # In practice, permission_mode can be "plan" / "default" / etc. We don't hard-require it,
    # because users may type /go at the boundary and the mode may already have flipped.
    _ = permission_mode  # reserved for future routing if needed

    print(json.dumps({"decision": "approve", "additionalContext": injected}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
