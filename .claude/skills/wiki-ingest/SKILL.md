# /wiki:ingest

Ingest external sources into the wiki knowledge base.

## Usage

```
/wiki:ingest <source>
/wiki:ingest raw/article-name.md
/wiki:ingest https://example.com/article
/wiki:ingest raw/*.md              # batch ingest
```

## Arguments

- `<source>` — File path in `raw/`, URL, or glob pattern

## Behavior

1. Locate the vault root (find nearest `CLAUDE.md` with "Personal Knowledge Base" header, or use CWD)
2. If source is a URL: fetch content, save to `raw/` first
3. Delegate to `wiki-ingestor` agent with:
   - Source path(s)
   - Vault root path
4. Agent classifies source type and extracts knowledge into `wiki/` pages
5. Updates `wiki/index.md` and `wiki/log.md`
6. Increments ingest counter in `CLAUDE.md`
7. If ingest counter >= 5: suggest running `/wiki:audit`

## Example

```
/wiki:ingest raw/rowboat-github-repo.md
→ Creates/updates: wiki/rowboat.md, wiki/multi-agent-orchestration-patterns.md
→ Updates: wiki/index.md, wiki/log.md
→ Ingest count: 3
```

## Notes

- Single source may produce multiple wiki pages — that's expected
- Source files in `raw/` are never modified (immutable)
- All wiki content in English
- Uses `wiki-ingestor` agent from `.claude/agents/wiki-ingestor.md`
