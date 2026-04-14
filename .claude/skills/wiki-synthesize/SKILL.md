# /wiki:synthesize

Cross-page analysis to find connections, patterns, and insights across wiki pages.

## Usage

```
/wiki:synthesize [focus]
/wiki:synthesize "orchestration patterns"
/wiki:synthesize --pages wiki/rowboat.md wiki/karpathy-llm-wiki-pattern.md
```

## Arguments

- `[focus]` — Topic or question to synthesize around (optional, defaults to full wiki scan)
- `--pages <paths>` — Specific pages to synthesize from

## Behavior

1. Locate vault root
2. Delegate to `wiki-synthesizer` agent with focus and page list
3. Agent reads index, identifies related clusters, deep-reads pages
4. Produces synthesis artifact:
   - Comparison/insight → new `wiki/` page (type: comparison | insight)
   - Research report → `outputs/research/`
5. Updates cross-references in source pages
6. Updates `wiki/index.md` and `wiki/log.md`

## Example

```
/wiki:synthesize "How do different tools approach LLM knowledge persistence?"
→ Reads: wiki/karpathy-llm-wiki-pattern.md, wiki/rowboat.md, wiki/llm-wiki-best-practices.md
→ Creates: wiki/llm-knowledge-persistence-comparison.md
→ Updates: index.md, log.md, cross-links in source pages
```

## Notes

- Minimum 3 source pages required (otherwise it's a summary, not synthesis)
- Uses concrete noun test: artifact must have a clear, referenceable name
- Surfaces contradictions between pages as primary value
- Uses `wiki-synthesizer` agent from `.claude/agents/wiki-synthesizer.md`
