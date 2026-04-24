# /wiki:autoresearch

Iterative web research loop with fact-check guardrail. Produces research synthesis in `outputs/research/`, promotes validated entities/concepts to `wiki/`.

## Usage

```
/wiki:autoresearch <topic>
/wiki:autoresearch "llm wiki patterns"
/wiki:autoresearch "agent orchestration" --rounds 5
/wiki:autoresearch "react server components" --no-factcheck
```

## Arguments

- `<topic>` — Research topic (required)
- `--rounds N` — Number of research rounds (default 3, max 5)
- `--no-factcheck` — Skip cross-model fact-check (emergency only)

## Workflow

### Round 1: Broad Search

1. Decompose topic into 3-5 search angles
2. Per angle: 2-3 WebSearch queries
3. Top 2-3 results per angle: WebFetch (max 10 fetches)
4. Extract: key claims, entities, concepts, open questions

### Round 2: Gap Fill

1. Identify contradictions/missing pieces from Round 1
2. Max 5 targeted WebSearch queries
3. WebFetch top results (max 6 fetches)

### Round 3: Synthesis Check (optional)

1. Only if major gaps remain after Round 2
2. 1-2 targeted passes (max 4 fetches)

**Total WebFetch limit: 20 per run**

## Filing

### Primary Output

Save to `outputs/research/{topic-slug}-YYMMDD.md`:

```yaml
---
title: "Research: {Topic}"
type: research
status: draft
confidence: low
created: YYYY-MM-DD
sources: [url1, url2, ...]
source_hashes: { url1: "sha256-8", ... }
---
```

Body structure: See `references/output-schema.md`

### Fact-check Gate (MANDATORY unless `--no-factcheck`)

Delegate to `codex:rescue`:

```
Task: Independent read of synthesis at {path} against cited sources.
Flag unsupported claims, recommend confidence adjustments.
```

Apply findings:
- Unsupported claims → add `[uncertainty: reason]`
- Contradictions → create `type: decision` record
- Well-corroborated → bump `confidence` if appropriate

### Promotion to wiki/ (separate step)

**Do NOT auto-promote.** After research completes:

1. Entities/concepts with ≥3 mentions → create `wiki/{name}.md` (kebab-case)
2. <3 mentions → append to `wiki/backlog.md`
3. Update `wiki/index.md` ONLY if pages created in wiki/
4. Prepend to `wiki/log.md`: `## [YYYY-MM-DD] autoresearch | {topic}`

User can also promote via `/wiki:ingest` on the research output.

## Integration

- Respect 7-layer ownership: synthesis → `outputs/research/`, entities → `wiki/`
- Use `source_hashes:` (sha256 first-8 of fetched content)
- Use typed `relations:` between extracted entities
- On contradictions: create `type: decision` record
- Counter-arguments section mandatory

## Constraints

- MUST run codex:rescue fact-check unless `--no-factcheck`
- MUST NOT auto-promote to wiki/ — user decides
- MUST NOT create stub pages — use `wiki/backlog.md`
- Max 20 WebFetch calls per run
- English-only output

## Example

```
/wiki:autoresearch "llm wiki patterns"
→ Round 1: 5 angles, 12 searches, 8 fetches
→ Round 2: 3 gap-fill queries, 4 fetches
→ Synthesis: outputs/research/llm-wiki-patterns-260424.md
→ Fact-check: codex: 2 claims softened, 1 confidence bump
→ Promotion candidates: 4 entities (3 created, 1 to backlog)
→ wiki/ pages: karpathy-wiki-pattern.md, obsidian-bases.md, qmd-search.md
→ Backlog: "mempalace" (2 mentions)
```

## References

- `references/program.md` — Research configuration
- `references/output-schema.md` — Synthesis page template
