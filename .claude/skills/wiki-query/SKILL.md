# /wiki:query

Search the wiki and answer questions with citations.

## Usage

```
/wiki:query <question>
/wiki:query "What orchestration patterns does Rowboat use?"
/wiki:query "Compare DDD vs clean architecture" --save
```

## Arguments

- `<question>` — Natural language question
- `--save` — Force save answer to `outputs/answers/`
- `--scope <dir>` — Limit search to specific directory (e.g., `projects/ejar3`)
- `--deep` — Force L3 progressive disclosure (read linked raw sources for fact-checking)
- `--file-back` — Save answer as synthesis page in `wiki/` (type: query-result)

## Behavior

1. Locate vault root
2. Delegate to `wiki-librarian` agent with question, scope, and depth flags
3. Agent uses **progressive disclosure** (L0→L3) for token efficiency:
   - L0: index TLDRs only → L1: headings → L2: full pages → L3: linked raw sources
4. Follows `relations:` typed links (supports/contradicts) for connected knowledge
5. Synthesizes answer with `[[wikilinks]]` citations
6. If answer is reusable (comparison, analysis, novel synthesis): save to `outputs/`
7. If `--save` flag: always save to `outputs/answers/`
8. If `--file-back` flag: save as `wiki/` page (type: query-result)

## Example

```
/wiki:query "What are the tradeoffs of MCP vs direct API integration?"
→ Searches: wiki/rowboat.md, wiki/multi-agent-orchestration-patterns.md
→ Answer with citations inline
→ Saved to: outputs/answers/mcp-vs-direct-api-tradeoffs.md (if reusable)
```

## Notes

- Read-only operation on wiki/ — never modifies knowledge pages
- Can read notes/ for additional context
- Uses `wiki-librarian` agent from `.claude/agents/wiki-librarian.md`
- If question can't be answered from wiki, says so explicitly
