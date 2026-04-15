---
name: session-sync
description: Export Claude Code sessions to searchable markdown with lifecycle management. Use when user says "sync sessions", "export sessions", "search sessions", "session history", "list sessions", "resume session", or wants to backup/search/annotate past conversations. Don't use for live note-taking, meeting transcripts, or non-Claude-Code content.
---

# Session Sync v2

Export Claude Code sessions to searchable markdown with lifecycle management, skills detection, and re-sync preservation.

## Quick Start

```bash
SCRIPT=".claude/skills/session-sync/scripts/session-sync.py"

# Check status
python3 $SCRIPT status

# Export last 7 days
python3 $SCRIPT export --days 7

# List active sessions
python3 $SCRIPT list --active

# Search
python3 $SCRIPT search "authentication"
```

## Commands

### Core

| Command | Description |
|---------|-------------|
| `sync` | Sync current session (Stop hook or manual) |
| `export` | Export sessions. Filters: `--all`, `--days N`, `--project NAME`, `--since DATE` |
| `status` | Show config, QMD status, session count |
| `config` | Set `--target-folder`, `--vault-mode`, `--auto-sync`, `--output-subdir`, `--collection-name` |
| `list-projects` | List available Claude Code projects |
| `setup` | Show setup instructions |

### Lifecycle

| Command | Description |
|---------|-------------|
| `list` | Browse sessions. `--active` (default), `--all`, `--json` |
| `resume` | Resume session in Claude Code. `--pick` (fzf/numbered), `--active` (most recent), `--fork`, or pass file path |
| `note TEXT` | Append timestamped note to session. `--session-id` optional |
| `close [TEXT]` | Mark session done with optional closing note |
| `log [TEXT]` | Multi-field update: `--status S`, `--tags T`, `--rating N` |

### Search (requires QMD)

| Command | Description |
|---------|-------------|
| `index` | Re-index sessions in QMD |
| `search QUERY` | BM25 keyword search (`-n` for result count) |
| `vsearch QUERY` | Semantic vector search (`-n` for result count) |

## Procedures

### Export Sessions

```bash
SCRIPT=".claude/skills/session-sync/scripts/session-sync.py"

# All sessions
python3 $SCRIPT export --all

# Last N days
python3 $SCRIPT export --days 7

# Specific project
python3 $SCRIPT export --project ejar

# Since date
python3 $SCRIPT export --since 2026-04-01
```

### Annotate Sessions

```bash
# Add note to current/most-recent session
python3 $SCRIPT note "Fixed the N+1 query issue"

# Close session with note
python3 $SCRIPT close "Delivered to QC team"

# Multi-field update
python3 $SCRIPT log --status done --rating 8 --tags "implementation,quick"

# Target specific session
python3 $SCRIPT log --session-id abc12345 --status blocked "Waiting for API access"
```

### Resume Sessions

```bash
# Interactive picker (fzf if available, else numbered list)
python3 $SCRIPT resume --pick

# Most recent active session
python3 $SCRIPT resume --active

# Fork instead of resume
python3 $SCRIPT resume --pick --fork

# Resume specific file
python3 $SCRIPT resume sessions/2026-04-14-0249-bebe21cb.md
```

### Search Sessions

```bash
# Keyword search
python3 $SCRIPT search "authentication" -n 10

# Semantic search
python3 $SCRIPT vsearch "how to optimize database queries" -n 5

# Re-index after exports
python3 $SCRIPT index
```

## Output Format

Sessions exported to `sessions/` (vault mode, flat):

```yaml
---
type: claude-session
project: ejar
date: 2026-04-14
session_id: bebe21cb-...
title: "Check implement details trong MR !9792"
messages: 15
created: 2026-04-14T02:49:47.523Z
last_activity: 2026-04-14T03:13:29.273Z
cwd: /Users/thieunv/projects/ejar
git_branch: main
status: active
tags: []
rating: null
skills:
  - gitlab-self-hosted
comments: ""
---
```

### Re-sync Preservation

On re-export, these fields survive: `title`, `status`, `tags`, `rating`, `comments`, `## My Notes` section. Fresh extraction updates: messages, last_activity, conversation, skills, artifacts.

## Configuration

Config: `.claude/skills/session-sync/config.json`

| Key | Default | Description |
|-----|---------|-------------|
| `target_folder` | Vault root | Parent folder |
| `output_subdir` | `sessions` | Subfolder for exports |
| `vault_mode` | `true` | Flat output (no per-project subdirs) |
| `auto_sync` | `false` | Whether Stop hook is configured |
| `collection_name` | `claude-sessions` | QMD collection name |
| `qmd_path` | `""` | Custom QMD binary path |

## References

- `references/schema.md` — Full frontmatter schema
- `schema/tags.yaml` — Valid session tags
- `procedures/setup.md` — First-time setup
- `procedures/setup-hook.md` — Stop hook configuration
