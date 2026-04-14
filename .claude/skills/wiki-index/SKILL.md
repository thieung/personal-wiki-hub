# /wiki:index

Rebuild `wiki/index.md` from actual wiki files.

## Usage

```
/wiki:index
/wiki:index --full
```

## Arguments

- `--full` — Include page TLDRs in index (heavier but more useful for search)

## Behavior

1. Glob all `wiki/*.md` files (excluding index.md, log.md)
2. Read frontmatter from each file (title, type, tags, updated)
3. If `--full`: also extract TLDR line
4. Group by type (entity, concept, summary, comparison, insight, query-result)
5. Sort alphabetically within groups
6. Rebuild `wiki/index.md` with:
   - Grouped entries with `[[wikilinks]]`
   - Tag cloud at bottom
   - Last rebuilt timestamp
7. Append to `wiki/log.md`: `## [YYYY-MM-DD] index | rebuild`

## Index Format

```markdown
# Wiki Index

*Last rebuilt: YYYY-MM-DD*

## Entities
- [[rowboat]] — AI coworker platform (YC S24)
- [[karpathy-llm-wiki-pattern]] — LLM-maintained persistent knowledge base

## Concepts
- [[llm-wiki-best-practices]] — Community-validated wiki practices
- [[multi-agent-orchestration-patterns]] — Agent typing and control flow

## Comparisons
(none yet)

## Insights
(none yet)

## Tags
agent-orchestration (2), knowledge-management (3), llm-tools (1)
```

## Notes

- Non-destructive: fully replaces index.md content
- Does not modify any wiki pages
- Fast operation — no web access needed
