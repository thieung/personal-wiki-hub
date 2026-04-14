# Project Structure

Detailed breakdown of the thieunv-vault architecture — a 7-layer LLM-maintained knowledge base.

## Directory Tree

```
thieunv-vault/
├── raw/                    # Layer 1: External Sources
│   ├── assets/             # Images, PDFs attached to sources
│   └── archive/            # Auto-archived after 30 days unprocessed
│
├── wiki/                   # Layer 2: LLM-Maintained Knowledge
│   ├── assets/             # Diagrams (Excalidraw, Mermaid→SVG)
│   ├── index.md            # Content catalog (auto-rebuilt)
│   ├── log.md              # Operation history (append-only)
│   └── backlog.md          # Concepts pending promotion (<3 mentions)
│
├── notes/                  # Layer 3: User-Owned Thinking
│   ├── daily/              # Daily journal entries (YYYY-MM-DD.md)
│   ├── fleeting/           # Quick captures, inbox notes
│   ├── reviews/            # Weekly review notes
│   └── assets/             # Personal diagrams, sketches
│
├── outputs/                # Layer 4: LLM-Generated Artifacts
│   ├── answers/            # Q&A results worth keeping
│   ├── reports/            # Analysis reports
│   └── research/           # Research synthesis
│
├── projects/               # Layer 5: Code-Driven Knowledge
│   └── <project-name>/     # Per-project knowledge
│       ├── _overview.md    # Project summary
│       ├── knowledge/      # Domain knowledge files
│       ├── decisions/      # ADRs, technical decisions
│       └── ops/            # Runbooks, deployment notes
│
├── content/                # Layer 6: Blog/Publication Drafts
│   └── *.md                # Flat structure, frontmatter status:
│
├── sessions/               # Layer 7: Session Logs
│   └── *.txt               # Auto-exported Claude Code sessions
│
├── templates/              # Frontmatter Templates
│   ├── daily-note.md       # Daily journal template
│   ├── weekly-review.md    # Weekly review checklist
│   ├── fleeting-note.md    # Quick capture template
│   └── wiki-page.md        # Wiki page template
│
├── .claude/agents/         # Wiki Subagents (5)
│   ├── wiki-ingestor.md
│   ├── wiki-librarian.md
│   ├── wiki-synthesizer.md
│   ├── wiki-auditor.md
│   └── wiki-crystallizer.md
│
├── plans/                  # ClaudeKit Plans (gitignored)
├── docs/                   # ClaudeKit Docs (gitignored)
│
├── CLAUDE.md               # Schema Governance
├── README.md               # Full Reference
├── QUICK_START.md          # A-Z Setup Guide
└── PROJECT_STRUCTURE.md    # This File
```

---

## Layer Details

### Layer 1: `raw/` — External Sources

**Purpose:** Immutable storage for original source material.

| Aspect | Rule |
|--------|------|
| Writer | User only |
| Reader | LLM |
| Mutability | Immutable after drop |
| Naming | `{source-title-slug}.md` or original filename |

**Subfolders:**
- `assets/` — Images, PDFs referenced by sources
- `archive/` — Unprocessed items >30 days (auto-moved by audit)

**Workflow:**
```
User drops file → LLM ingests → wiki/ pages created → raw/ untouched
```

---

### Layer 2: `wiki/` — LLM-Maintained Knowledge

**Purpose:** Refined, queryable knowledge derived from raw sources.

| Aspect | Rule |
|--------|------|
| Writer | LLM only |
| Reader | Both |
| Source | Always cites `raw/` or other wiki pages |

**System Files:**
- `index.md` — Auto-rebuilt catalog grouped by type
- `log.md` — Append-only operation history
- `backlog.md` — Concepts with <3 mentions awaiting promotion

**Page Types:**
| Type | Description |
|------|-------------|
| `summary` | Overview of a source or topic |
| `entity` | Tool, project, person, organization |
| `concept` | Pattern, principle, technique |
| `comparison` | Structured X vs Y analysis |
| `query-result` | Promoted answer from outputs/ |
| `insight` | Distilled lesson from sessions |
| `decision` | Conflicting positions + resolution |

---

### Layer 3: `notes/` — User-Owned Thinking

**Purpose:** Personal thinking space. LLM reads but never writes.

| Aspect | Rule |
|--------|------|
| Writer | User only |
| Reader | Both |
| LLM action | Audit (report-only), never modify |

**Subfolders:**

| Folder | Purpose | Template |
|--------|---------|----------|
| `daily/` | Daily journal entries | `daily-note.md` |
| `fleeting/` | Quick captures, inbox | `fleeting-note.md` |
| `reviews/` | Weekly reviews | `weekly-review.md` |
| `assets/` | Personal diagrams |  |

**Note Lifecycle (Zettelkasten-inspired):**
```
fleeting/ (quick capture) → daily/ (processed) → wiki/ (if worth keeping)
```

---

### Layer 4: `outputs/` — LLM-Generated Artifacts

**Purpose:** Temporary LLM outputs that may be promoted to wiki/.

| Aspect | Rule |
|--------|------|
| Writer | LLM |
| Reader | Both |
| Promotion | Good answers → wiki/ as `query-result` |

**Subfolders:**
- `answers/` — Q&A results worth keeping
- `reports/` — Analysis, audit reports
- `research/` — Research synthesis

---

### Layer 5: `projects/` — Code-Driven Knowledge

**Purpose:** Knowledge compiled from codebases and sessions.

| Aspect | Rule |
|--------|------|
| Writer | LLM compiles, user reviews |
| Source | Git repos + session logs |
| Trigger | Weekly via `"compile [project]"` |

**Per-Project Structure:**
```
projects/<name>/
├── _overview.md      # Project summary, tech stack
├── knowledge/        # Domain knowledge (1 file per bounded context)
├── decisions/        # ADRs, technical decisions
└── ops/              # Runbooks, deployment notes
```

---

### Layer 6: `content/` — Blog/Publication Drafts

**Purpose:** Blog posts, articles, social content in progress.

| Aspect | Rule |
|--------|------|
| Writer | User drafts, LLM assists |
| Structure | Flat, frontmatter `status:` |
| Statuses | `draft` → `review` → `published` |

---

### Layer 7: `sessions/` — Session Logs

**Purpose:** Auto-exported Claude Code session transcripts.

| Aspect | Rule |
|--------|------|
| Writer | Auto-export hook |
| Reader | LLM (for crystallize operation) |
| Processing | `"crystallize [session]"` → wiki/ insights |

---

## Templates

| Template | Location | Used For |
|----------|----------|----------|
| `daily-note.md` | Daily journal | Periodic Notes plugin |
| `weekly-review.md` | Weekly checklist | Periodic Notes plugin |
| `fleeting-note.md` | Quick captures | Manual or hotkey |
| `wiki-page.md` | Wiki pages | LLM reference |

---

## Ownership Matrix

| Directory | Writer | Reader | Notes |
|-----------|--------|--------|-------|
| `raw/` | User | LLM | Immutable after drop |
| `wiki/` | **LLM** | Both | Derived from raw/ + notes/ |
| `notes/` | **User** | Both | LLM audits, never modifies |
| `outputs/` | LLM | Both | May promote to wiki/ |
| `projects/` | LLM compiles | Both | From codebases + sessions |
| `content/` | User drafts | Both | LLM assists |
| `sessions/` | Auto-export | LLM | Read-only for LLM |

---

## Naming Conventions

| Context | Convention | Example |
|---------|------------|---------|
| Wiki pages | kebab-case | `multi-agent-patterns.md` |
| Daily notes | ISO date | `2026-04-14.md` |
| Weekly reviews | ISO week | `2026-W16.md` |
| Sessions | Timestamp + slug | `260414-1707-topic.txt` |
| Projects | Lowercase | `ejar3/`, `goclaw/` |
| Tags | English kebab-case | `agent-orchestration` |

---

## Obsidian Integration

### Required Plugins

| Plugin | Purpose | Config |
|--------|---------|--------|
| Periodic Notes | Auto-create daily/weekly | Templates folder: `templates/` |
| Templater | Template variables | Enable folder templates |

### Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| Smart Connections | Semantic search (>100 pages) |
| Dataview | Query frontmatter |
| Obsidian Git | Auto-commit |
| Calendar | Daily/weekly navigation |

### Periodic Notes Config

| Setting | Value |
|---------|-------|
| Daily Note Template | `templates/daily-note.md` |
| Daily Note Folder | `notes/daily/` |
| Weekly Note Template | `templates/weekly-review.md` |
| Weekly Note Folder | `notes/reviews/` |

---

## Git Configuration

### .gitignore

```
sessions/
plans/
docs/
.DS_Store
.obsidian/workspace*.json
```

### Tracked

```
raw/
wiki/
notes/
outputs/
projects/
content/
templates/
.claude/agents/
CLAUDE.md
README.md
QUICK_START.md
PROJECT_STRUCTURE.md
```

---

## Search Tiers

| Scale | Backend | When to Upgrade |
|-------|---------|-----------------|
| <100 pages | Grep + index.md | Default |
| 100-500 | QMD CLI | Index scan feels slow |
| 500+ | QMD MCP server | CLI response >2s |

---

## Trigger Phrases

| Phrase | Operation |
|--------|-----------|
| `"ingest [file]"` | raw/ → wiki/ |
| `"compile this week"` | Process recent raw/ |
| `"compile [project]"` | Update project knowledge |
| `"crystallize [session]"` | Extract session insights |
| `"query [question]"` | Search + answer |
| `"audit vault"` | Health check |
| `"analyze graph health"` | Obsidian graph analysis |
| `"refresh [page]"` | Update wiki page |
| `"review backlog"` | Process pending concepts |
