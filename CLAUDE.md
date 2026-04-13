# Personal Knowledge Base — Schema

This vault is a persistent, LLM-maintained knowledge base following the [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted for multi-project software engineering workflow with code-driven + research-driven knowledge.

## Architecture (7 layers)

```
thieunv-vault/
├── raw/               # External sources — immutable, user drops files
│   ├── assets/        # Images attached to sources
│   └── archive/       # Unprocessed items >30 days
├── wiki/              # LLM-maintained research knowledge
│   ├── assets/        # LLM-generated diagrams (Excalidraw, Mermaid→SVG)
│   ├── index.md       # Content catalog
│   └── log.md         # Operation log (append-only)
├── notes/             # USER-owned — personal thinking, LLM reads only
│   └── assets/        # User's diagrams, sketches
├── outputs/           # LLM-generated artifacts (answers, reports, research)
│   ├── answers/       # Q&A results worth keeping
│   ├── reports/       # Analysis reports
│   └── research/      # Research synthesis
├── projects/          # Code-driven project knowledge
│   ├── ejar3/         # Per-project: _overview, knowledge/, decisions/, ops/
│   ├── goclaw/
│   └── vividkit/
├── content/           # Blog drafts (flat, frontmatter status:)
├── sessions/          # Auto-exported Claude Code session logs
├── templates/         # Frontmatter templates
├── .claude/agents/    # wiki-* subagents
├── plans/ + docs/     # ClaudeKit workflow (gitignored)
└── CLAUDE.md          # This file
```

## Ownership Matrix

| Directory | Writer | Reader | Notes |
|-----------|--------|--------|-------|
| `raw/` | User only | LLM | Immutable post-drop |
| `wiki/` | **LLM only** | Both | Derived from raw/ + notes/ ingest |
| `notes/` | **User only** | Both | LLM can audit (report-only), never modify |
| `outputs/` | LLM | Both | Q&A artifacts, may be promoted to wiki/ |
| `projects/` | LLM compiles, user reviews | Both | Compiled from codebase + sessions |
| `content/` | User drafts, LLM assists | Both | Blog/social content |
| `sessions/` | Auto-export hook | LLM | Historical context |
| `templates/` | User | Both | Frontmatter skeletons |

## Sync Flows

```
raw/      ──ingest────→ wiki/         (always, external sources)
notes/    ──select────→ wiki/         (selective, user decides)
code      ──compile──→ projects/      (weekly, git-diff triggered)
sessions/ ──extract──→ projects/      (weekly, mine for insights)
sessions/ ──crystallize──→ wiki/ + projects/  (on-demand, extract insights)
query     ──answer──→ outputs/        (when answer is reusable)
outputs/  ──promote──→ wiki/          (when answer becomes canonical)
```

## Source Classification (before ingest)

| Type | Extraction approach |
|------|-------------------|
| report / whitepaper | Section-by-section, exec summary first |
| paper | Method + findings |
| transcript | Speaker attribution, decisions, action items |
| article / blog | Key claims + evidence |
| thread / tweet | Core insight + context |
| code repo | Architecture + patterns + dependencies |

## Wiki Page Conventions

### Frontmatter (required)

```yaml
---
title: Page Title
type: summary | entity | concept | comparison | query-result | insight | decision
status: draft | active | stale | superseded
sources: [source-filename.md, ...]
source_hashes: { source-filename.md: "sha256-first-8-chars" }
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low | medium | high   # low=1 source, medium=2+, high=3+ corroborating
last_queried: YYYY-MM-DD          # bumped when page used to answer a query (optional)
supersedes: "[[old-page-name]]"   # this page replaces the target (optional)
superseded_by: "[[new-page-name]]" # this page was replaced by target (optional)
tags: [always-english-kebab-case]
relations:                         # typed semantic links (optional)
  - { type: supports, target: "[[page-name]]" }
  - { type: contradicts, target: "[[page-name]]" }
  # types: supports | contradicts | is-a | part-of | evolved-into | evolved-from | depends-on
---
```

### Type descriptions

- `summary` — overview of a source or topic
- `entity` — a specific tool, project, person, or organization
- `concept` — a pattern, principle, or technique
- `comparison` — structured comparison of alternatives
- `query-result` — reusable answer promoted from outputs/
- `insight` — distilled lesson from sessions, debugging, or cross-project observation
- `decision` — records conflicting positions and the chosen resolution

### Status lifecycle

`draft` → `active` → `stale` (auto, >60 days no update AND no query) → `superseded` (manual, set `superseded_by:`)

Stale detection considers `last_queried:` — a page queried recently stays `active` even if `updated:` is old. When superseding, set `superseded_by:` on old page and `supersedes:` on new page (bidirectional).

### Body structure

1. **Title** (`# Title`)
2. **TLDR** — 1-2 sentences immediately after title. Used for index scanning, saves tokens on irrelevant pages.
3. **Body** — organized by topic
4. **Counter-arguments and data gaps** (mandatory). If all sources agree, find the strongest critique. Never let wiki become one-sided.
5. **Related pages** — wikilinks to connected pages

### Language

All vault content is **English only**. Vietnamese support is an Obsidian UI concern (i18n plugin), not a vault content concern. No `lang:` or bilingual aliases.

### Uncertainty notation

Use `[uncertainty: reason]` inline when a claim is inferred, speculative, or partially supported. Never present uncertain info as fact.

Example: "Rowboat's entity extraction quality is poor at scale [uncertainty: only HN anecdotes, no published benchmarks]."

### Cross-references

Use `[[page-name]]` Obsidian-style wikilinks for internal links. Never use relative markdown paths.

### Filenames

Kebab-case. Self-documenting. `rowboat.md`, `multi-agent-orchestration-patterns.md`, `ejar3-billing-domain.md`.

## Operations

### Ingest (external sources)

1. Read source from `raw/`
2. Classify source type
3. Write summary/entity/concept page(s) in `wiki/`
4. Update relevant existing pages
5. Update `wiki/index.md`
6. Compute SHA-256 hash (first 8 chars) of source file, store in `source_hashes` frontmatter
7. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Source Title` with `Deferred:` and `Next:` fields
8. A single source may touch 10-15 pages
9. On contradicting sources: create decision record (type: decision) instead of silently overwriting

### Query

1. Read `wiki/index.md` (or QMD search when installed)
2. Read relevant pages, synthesize answer with citations
3. If answer is reusable (comparison, analysis, novel synthesis), save to `outputs/answers/` or `outputs/research/`
4. If answer becomes canonical knowledge, promote to `wiki/` as query-result page
5. Append to `wiki/log.md`: `## [YYYY-MM-DD] query | question` with `Deferred:` and `Next:` fields

### Compile (code-driven)

1. Run `git log --since="1 week ago" --name-only` in each project repo
2. Identify changed domains/modules
3. Re-compile affected knowledge files in `projects/*/knowledge/`
4. One file per bounded context (domain). Per-layer or per-feature compilation is wrong granularity.
5. Mark `source: ai-compiled`, `confidence: medium`
6. On contradiction with existing docs: add `## [YYYY-MM-DD] contradiction` section with both versions, mark `confidence: low`, let user resolve

### Crystallize (session → wiki)

Extract reusable knowledge from Claude Code session logs.

1. Read session log from `sessions/`
2. Identify: key decisions, failed approaches, reusable patterns, tool discoveries
3. For each extractable insight:
   - Check if existing wiki/project page covers it → update
   - Otherwise create new page (type: insight) in `wiki/` or `projects/*/knowledge/`
4. Update `wiki/index.md`
5. Append to `wiki/log.md`: `## [YYYY-MM-DD] crystallize | Session Title`
6. Single session typically yields 1-3 insight pages
7. Reprocessing guard: check `wiki/log.md` for existing crystallize entry before processing a session

### Audit (wiki + notes, structural)

Scope: `wiki/` and `notes/`.

Checks:
- Stale files (`updated:` >60 days, auto-mark `status: stale`)
- Missing frontmatter fields (including new: status, confidence, source_hashes)
- Source hash drift (raw file changed after wiki page compiled)
- Broken `[[wikilinks]]`
- Orphan pages (no inbound links)
- Duplicate titles or overlapping concepts
- `confidence: low` backlog
- Contradictions between pages
- Counter-arguments section missing (wiki only)
- Supersession integrity: pages with `status: superseded` must have `superseded_by:`, and target must have `supersedes:` (bidirectional)
- Archival candidates: pages with `last_queried:` >90 days and `confidence: low`
- Reinforcement: pages with `last_queried:` within 30 days are immune to stale marking

Scope rule:
- `wiki/` issues → can auto-fix or suggest fix
- `notes/` issues → report only, user decides

Trigger: every 5-10 ingests, or on-demand via `/wiki:audit`.

### Refresh (single page content update)

Target: a specific existing wiki page.

1. Read target page, parse frontmatter
2. Audit claims against other wiki pages (consistency)
3. Validate source URLs still accessible
4. Optional: fresh web research (`--research` flag)
5. Propose diff — don't auto-apply
6. On approval: update content, bump `updated:`, append to `wiki/log.md`
7. Preserve history via git

## Search Tier (scale-based)

| Scale | Backend | Setup |
|-------|---------|-------|
| <100 pages | Grep + `wiki/index.md` | Default (current) |
| 100-500 | QMD CLI | `brew install tobi/tap/qmd` |
| 500+ | QMD MCP server | QMD + MCP config |

Always read this section before searching. Degrade gracefully: MCP → CLI → Grep.

## Ingest Counter

Track ingests since last lint. When count ≥5, trigger audit automatically.

**Current count since last lint:** 2

## Non-Negotiable Principles

1. `raw/` is immutable — never modify files after drop
2. `notes/` is user-owned — LLM reads, never writes
3. Every derived wiki page must cite sources from `raw/` or other wiki pages
4. Uncertainty must be explicit — use `[uncertainty: reason]`
5. Write-back discipline — valuable answers go to `outputs/` or `wiki/`, not ephemeral chat
6. Markdown-first, wikilinks over relative paths
7. No placeholder pages — only create pages with real content
8. English-only vault content
