#!/usr/bin/env bash
# translate-prompt.sh — UserPromptSubmit hook for Claude Code
# Detects Chinese in user prompts and auto-translates to English via local Ollama.
# Translation is injected as additionalContext so Claude sees both versions.
#
# Usage: Configure in .claude/settings.json under hooks.UserPromptSubmit
# Requires: jq, curl, Ollama running on localhost:11434

set -euo pipefail

# --- Ensure tools are on PATH (hook env may be minimal) ---
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# --- Debug logging (set TRANSLATE_DEBUG=1 to enable) ---
DEBUG="${TRANSLATE_DEBUG:-0}"
debug_log() {
  if [[ "$DEBUG" == "1" ]]; then
    echo "[$(date '+%H:%M:%S')] $*" >> /tmp/translate-prompt.log
  fi
}

debug_log "=== Hook started ==="
debug_log "PATH=$PATH"
debug_log "jq=$(which jq 2>/dev/null || echo 'NOT FOUND')"
debug_log "curl=$(which curl 2>/dev/null || echo 'NOT FOUND')"
debug_log "perl=$(which perl 2>/dev/null || echo 'NOT FOUND')"

# --- Config ---
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
OLLAMA_MODEL="${TRANSLATE_MODEL:-qwen2.5:7b-instruct}"
OLLAMA_TIMEOUT="${OLLAMA_TIMEOUT:-30}"

# Skip translation for projects matching these patterns (comma-separated)
# Example: TRANSLATE_SKIP_PROJECTS="editory,my-blog,writing"
SKIP_PROJECTS="${TRANSLATE_SKIP_PROJECTS:-}"

# --- Read stdin ---
INPUT=$(cat)
debug_log "stdin bytes: ${#INPUT}"
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
debug_log "prompt: $PROMPT"
debug_log "cwd: $CWD"

# No prompt → pass through
if [[ -z "$PROMPT" ]]; then
  debug_log "empty prompt, exiting"
  exit 0
fi

# --- Skip list check ---
if [[ -n "$SKIP_PROJECTS" ]]; then
  IFS=',' read -ra SKIP_LIST <<< "$SKIP_PROJECTS"
  for pattern in "${SKIP_LIST[@]}"; do
    pattern=$(echo "$pattern" | xargs)  # trim whitespace
    if [[ "$CWD" == *"$pattern"* ]]; then
      exit 0
    fi
  done
fi

# --- Chinese detection ---
# Check if prompt contains any CJK Unified Ideographs (U+4E00–U+9FFF)
# Use perl for Unicode support (macOS grep lacks -P flag)
# Must enable UTF-8 decoding via binmode, otherwise perl matches bytes not codepoints
if ! echo "$PROMPT" | perl -e 'binmode STDIN,":utf8"; local $/; $t=<STDIN>; exit($t=~/[\x{4e00}-\x{9fff}]/?0:1)'; then
  # No Chinese characters → skip
  debug_log "no Chinese detected, skipping"
  exit 0
fi
debug_log "Chinese detected, translating..."

# --- Clear proxy env vars (Ollama is local) ---
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY 2>/dev/null || true

# --- Call Ollama ---
SYSTEM_PROMPT="You are a translator. Translate the following Chinese text to English. The text is a programming instruction for an AI coding assistant. Preserve all code identifiers, file paths, command names, and technical terms exactly as-is. Output ONLY the English translation, nothing else."

PAYLOAD=$(jq -n \
  --arg model "$OLLAMA_MODEL" \
  --arg prompt "$PROMPT" \
  --arg system "$SYSTEM_PROMPT" \
  '{model: $model, prompt: $prompt, system: $system, stream: false}')

RESPONSE=$(curl -s --max-time "$OLLAMA_TIMEOUT" \
  "${OLLAMA_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" 2>/dev/null) || {
  # Ollama unreachable → graceful degradation, no output
  debug_log "curl failed (Ollama unreachable?)"
  exit 0
}
debug_log "Ollama response length: ${#RESPONSE}"
debug_log "Ollama raw response: $RESPONSE"

# Extract translation from response
TRANSLATION=$(echo "$RESPONSE" | jq -r '.response // empty' 2>/dev/null)

if [[ -z "$TRANSLATION" ]]; then
  # Failed to parse → graceful degradation
  debug_log "empty translation, exiting"
  exit 0
fi

debug_log "translation OK (${#TRANSLATION} chars): $TRANSLATION"
# --- Output additionalContext ---
jq -n --arg translation "$TRANSLATION" '{
  "additionalContext": ("[TRANSLATED INSTRUCTION — Follow this English version]\n" + $translation + "\n\n[End of translated instruction. The original message is in Chinese. Execute based on the English translation above. Respond in Chinese.]")
}'
