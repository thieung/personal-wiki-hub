# /wiki:browse

Navigate and discover wiki content — sections, tags, pages, search.

**Distinct from `/wiki:query`**: browse is navigation (what exists?), query is answering (what does X mean?).

## Usage

```
/wiki:browse
/wiki:browse --tag multi-agent
/wiki:browse --type entity
/wiki:browse --search "orchestration"
/wiki:browse --recent 7
```

## Arguments

- *(no args)* — Full browse: list all pages grouped by type with TLDRs
- `--tag <tag>` — List pages matching a specific tag
- `--type <type>` — List pages of a specific type (entity, concept, insight, etc.)
- `--search <keyword>` — Keyword search across page titles and TLDRs
- `--recent <days>` — Pages updated or queried within N days (default: 30)
- `--confidence <level>` — Filter by confidence level (low, medium, high)
- `--stale` — Show only stale pages needing attention

## Behavior

1. Locate vault root (look for CLAUDE.md with wiki schema)
2. Read `wiki/index.md` for page catalog
3. Apply filters based on flags
4. For each matching page, read frontmatter only (no body — token efficient)
5. Display results grouped and sorted:
   - Full browse: grouped by `type:`, sorted by `updated:` desc
   - Tag browse: flat list sorted by `updated:` desc
   - Search: ranked by title match > TLDR match
   - Recent: sorted by most recent of `updated:` or `last_queried:`

## Output Format

```
Wiki Browse — 12 pages
──────────────────────

entity (4)
  rowboat.md                    [active] [low]  updated: 2026-04-14
    Rowboat — open-source AI coworker with auto-built knowledge graphs
  karpathy-llm-wiki-pattern.md  [active] [med]  updated: 2026-04-14
    Karpathy's LLM-maintained personal knowledge base pattern

concept (3)
  multi-agent-orchestration...  [active] [low]  updated: 2026-04-14
    Common patterns for coordinating multiple AI agents
  llm-wiki-best-practices.md   [active] [med]  updated: 2026-04-14
    Seven community-validated practices for LLM wiki sustainability
```

## Notes

- Read-only operation — never modifies any files
- Reads frontmatter only for token efficiency (no full page body)
- Does NOT delegate to an agent — runs inline with Grep + Glob + Read
- For answering questions about content, use `/wiki:query` instead
