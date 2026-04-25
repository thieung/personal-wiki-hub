# Available Commands

Complete reference of slash commands and CLI tools in this vault.

---

## Wiki Skills (12)

Core knowledge base management commands.

| Command | Description |
|---------|-------------|
| `/wiki:capture` | Capture external sources (URL, PDF, clipboard) into `raw/` |
| `/wiki:ingest` | Process `raw/` sources into wiki pages |
| `/wiki:autoresearch` | Iterative web research with fact-checking |
| `/wiki:query` | Search and answer questions from wiki |
| `/wiki:browse` | Navigate wiki by type, tag, keyword, or recency |
| `/wiki:synthesize` | Cross-page analysis, find patterns and connections |
| `/wiki:audit` | Structural health check, auto-fix safe issues |
| `/wiki:refresh` | Update stale wiki pages |
| `/wiki:index` | Rebuild `wiki/index.md` catalog |
| `/wiki:link` | Add missing cross-references between pages |
| `/wiki:setup` | Initialize or verify vault structure |
| `/wiki:status` | Display health metrics dashboard |

---

## Additional Skills

### /tasknotes — Obsidian Task Management

Manage tasks via TaskNotes plugin HTTP API.

```bash
/tasknotes                      # List all tasks
/tasknotes list                 # List all tasks (explicit)
/tasknotes list in-progress     # Filter by status
/tasknotes list --project "X"   # Filter by project
/tasknotes create "Task title"  # Create new task
/tasknotes create "Task" --project "Project" --priority high
/tasknotes done "Tasks/x.md"    # Mark task done
/tasknotes update "Tasks/x.md" --status cancelled
/tasknotes delete "Tasks/x.md"  # Delete task
/tasknotes options              # Show available statuses/priorities
/tasknotes stats                # Task statistics
```

**Requirements:** TaskNotes plugin with HTTP API enabled (port 8080)

### /session-sync — Export Claude Code Sessions

Export session logs for crystallization and search.

```bash
/session-sync                   # Export current session
/session-sync --all             # Export all recent sessions
```

---

## Trigger Phrases

Natural language triggers that activate operations.

| Phrase | Operation |
|--------|-----------|
| "ingest [filename]" | Process single raw/ file |
| "compile this week" | Process raw/ files from last 7 days |
| "compile [project]" | Update project knowledge |
| "crystallize [session]" | Extract insights from session log |
| "query [question]" | Search + synthesize answer |
| "audit vault" | Full structural audit |
| "analyze graph health" | Obsidian graph analysis |
| "refresh [page]" | Update single wiki page |
| "review backlog" | Process `wiki/backlog.md` |
| "show my tasks" | List Obsidian tasks |
| "create task for X" | Create new task |
| "mark X as done" | Complete task |

---

## CLI Scripts

### bin/setup-vault.sh

Bootstrap Obsidian vault structure.

```bash
./bin/setup-vault.sh            # Create all directories and templates
```

### .claude/skills/tasknotes/scripts/tasks.py

Direct CLI for TaskNotes (bypasses slash command).

```bash
uv run .claude/skills/tasknotes/scripts/tasks.py list --table
uv run .claude/skills/tasknotes/scripts/tasks.py create "Title" --project "Project"
uv run .claude/skills/tasknotes/scripts/tasks.py update "Tasks/x.md" --status done
uv run .claude/skills/tasknotes/scripts/tasks.py delete "Tasks/x.md"
uv run .claude/skills/tasknotes/scripts/tasks.py options --table
uv run .claude/skills/tasknotes/scripts/tasks.py stats --table
```

---

## Agents (5)

Background agents spawned by skills.

| Agent | Role |
|-------|------|
| `wiki-ingestor` | raw/ → wiki/ extraction with provenance tracking |
| `wiki-librarian` | Search + answer with progressive disclosure |
| `wiki-synthesizer` | Cross-page analysis, min 3 sources |
| `wiki-auditor` | Health check, hash drift detection |
| `wiki-crystallizer` | sessions/ → wiki insights extraction |

---

## Quick Reference

```bash
# Daily workflow
/wiki:status                    # Check health
/tasknotes list in-progress     # What am I working on?
/wiki:query "question"          # Ask wiki

# Add knowledge
/wiki:capture https://url --ingest

# Weekly maintenance
/wiki:audit --fix
/wiki:link
/wiki:index --full
```
