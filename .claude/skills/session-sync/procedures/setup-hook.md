# Setup Stop Hook — Auto-sync Sessions

## Add to settings

Add to `~/.claude/settings.json` (global) or `.claude/settings.local.json` (project):

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/scripts/session-sync.py sync"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/` with the actual skill path:
- Global: `~/.claude/skills/session-sync/scripts/session-sync.py`
- Project-local: `.claude/skills/session-sync/scripts/session-sync.py`

## How it works

1. Claude Code fires `Stop` hook after each assistant turn
2. Hook receives JSON on stdin: `{"session_id": "...", "transcript_path": "..."}`
3. Script exports/updates the session markdown in `sessions/`
4. Preserved fields (status, tags, rating, My Notes) survive re-sync

## Verify

After a session, check:
```bash
tail -5 .claude/skills/session-sync/sync.log
ls -la sessions/*.md | tail -5
```

## Notes

- Stop hook only (no UserPromptSubmit) to minimize overhead
- Silent no-op on first prompt (no session data yet)
- Idempotent: safe to re-run
