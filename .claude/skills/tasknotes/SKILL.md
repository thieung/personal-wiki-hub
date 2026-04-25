---
name: tasknotes
description: Manage tasks in Obsidian via TaskNotes plugin API. Use when user wants to create tasks, list tasks, query by status or project, update task status, delete tasks, or check what they need to do.
---

# TaskNotes Skill

Manage Obsidian tasks via the TaskNotes plugin HTTP API.

## Slash Command Usage

```
/tasknotes                     # List all tasks
/tasknotes list                # List all tasks  
/tasknotes list in-progress    # List by status
/tasknotes create "Task title" # Create new task
/tasknotes done "Tasks/x.md"   # Mark task done
/tasknotes options             # Show available statuses/priorities
```

## Instructions

When this skill is invoked, parse the args and run the appropriate command:

| Args Pattern | Action |
|--------------|--------|
| (empty) or `list` | `uv run .claude/skills/tasknotes/scripts/tasks.py list --table` |
| `list <status>` | `uv run .claude/skills/tasknotes/scripts/tasks.py list --status "<status>" --table` |
| `create "<title>"` | `uv run .claude/skills/tasknotes/scripts/tasks.py create "<title>" --table` |
| `create "<title>" --project <p>` | `uv run .claude/skills/tasknotes/scripts/tasks.py create "<title>" --project "<p>" --table` |
| `done "<task-id>"` | `uv run .claude/skills/tasknotes/scripts/tasks.py update "<task-id>" --status done --table` |
| `update "<task-id>" --status <s>` | `uv run .claude/skills/tasknotes/scripts/tasks.py update "<task-id>" --status "<s>" --table` |
| `delete "<task-id>"` | `uv run .claude/skills/tasknotes/scripts/tasks.py delete "<task-id>" --table` |
| `options` | `uv run .claude/skills/tasknotes/scripts/tasks.py options --table` |
| `stats` | `uv run .claude/skills/tasknotes/scripts/tasks.py stats --table` |

## Requirements

1. **TaskNotes plugin** installed in Obsidian
2. **Enable HTTP API** in TaskNotes settings (port 8080)

## Trigger Phrases

- "show my tasks", "list tasks" → `/tasknotes list`
- "create task for X" → `/tasknotes create "X"`
- "mark X as done" → `/tasknotes done "X"`
- "what should I work on" → `/tasknotes list in-progress`
