Generate a daily insights report and optionally send via IM.

Parse the user's arguments: $ARGUMENTS

Format: [--send] [--date YYYY-MM-DD]
- `--send` — after generating, send report via Telegram (telegram MCP `send_message`)
- `--date` — target date (default: yesterday)

## Execute the following workflow:

### Step 1: Work Summary
1. Run `git log --since="<date> 00:00" --until="<date> 23:59" --all --oneline` across all repos in `~/codes/` (use `find ~/codes -maxdepth 2 -name .git -type d` to discover repos)
2. Use cccmemory MCP `list_recent_sessions` to get session summaries for the date
3. Compile: number of commits, key files modified, session count, tasks completed
4. Keep commit summaries concise — group by repo, max 5 most notable per repo

### Step 2: Config Health Check
1. Check `.claude/settings.json` — valid JSON, no empty/broken entries
2. Check MCP servers — use mowen MCP `Echo` tool as connectivity test
3. Count: skills in `.claude/commands/`, agents available, hooks configured
4. Flag any obvious issues (empty config, missing CLAUDE.md, etc.)

### Step 3: Content Pipeline Status
1. List files in `my_works/` — show draft status (check git status for uncommitted changes)
2. Check for recent `/iterate-style` runs (git log for `[style-update]` commits)
3. List pending platform publishes (drafts not yet published)

### Step 4: Memory & Learning
1. Use cccmemory MCP `get_health_report` for memory health
2. Use cccmemory MCP `get_memory_stats` for stats overview
3. Summarize: total memories, recent additions, any warnings

### Step 5: Compile Report
Format as concise Markdown suitable for mobile reading:

```
📊 Daily Insights — <date>

**Work:** X commits across Y repos, Z sessions
- [top commit summaries grouped by repo]

**Config:** ✅ healthy / ⚠️ issues found
- [details if issues]

**Content:** X drafts, Y pending publish
- [draft list with status]

**Memory:** X total, Y recent
- [health status]
```

Keep total report under 2000 characters for mobile readability.

### Step 6: Deliver
If `--send` flag is present:
1. Use telegram MCP `send_message` to send the compiled report (use Markdown formatting)
2. Report delivery status to user

If `--send` not present:
1. Display report in terminal only
