# Setup — Session Sync v2

## Prerequisites

- Python 3.10+
- Claude Code CLI
- (Optional) fzf for interactive session picker
- (Optional) QMD for search: `npm i -g @tobilu/qmd`

## Quick Start

### 1. Verify config

```bash
python3 ~/.claude/skills/session-sync/scripts/session-sync.py status
```

For project-local override (vault):
```bash
python3 .claude/skills/session-sync/scripts/session-sync.py status
```

### 2. Configure (if needed)

```bash
# Set target folder
python3 scripts/session-sync.py config --target-folder /path/to/vault

# Enable vault mode (flat output)
python3 scripts/session-sync.py config --vault-mode true
```

### 3. Export existing sessions

```bash
# Export last 7 days
python3 scripts/session-sync.py export --days 7

# Export all
python3 scripts/session-sync.py export --all
```

### 4. Set up auto-sync hook

See `procedures/setup-hook.md`.

### 5. (Optional) Index for search

```bash
python3 scripts/session-sync.py index
python3 scripts/session-sync.py search "authentication"
python3 scripts/session-sync.py vsearch "how to fix N+1 queries"
```
