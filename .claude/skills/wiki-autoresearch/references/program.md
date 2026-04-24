# Autoresearch Program Configuration

Configurable parameters for `/wiki:autoresearch`.

## Preferred Sources

Prioritize these source types (in order):
1. Official documentation
2. Academic papers (arXiv, ACL, IEEE)
3. Reputable tech blogs (official company blogs, well-known authors)
4. GitHub repositories (for code-related topics)
5. News from established outlets

Deprioritize:
- SEO-optimized aggregator sites
- Forums without clear expertise signals
- Paywalled content (note limitation in synthesis)

## Confidence Scoring

| Level | Criteria |
|-------|----------|
| `high` | 3+ independent corroborating sources |
| `medium` | 2 sources OR 1 highly authoritative source |
| `low` | Single source OR conflicting sources |

Downgrade confidence when:
- Source is >6 months old for fast-moving topics
- Source has clear commercial bias
- Claims are extraordinary without strong evidence

## Round Limits

| Parameter | Default | Max |
|-----------|---------|-----|
| Rounds | 3 | 5 |
| WebFetch per run | 20 | 20 |
| Search angles (Round 1) | 3-5 | 7 |
| Queries per angle | 2-3 | 4 |
| Results per query | 2-3 | 5 |

## Domain-Specific Constraints

User can add domain rules here:

```yaml
# Example:
ai_safety:
  required_sources: ["arxiv.org", "alignmentforum.org"]
  avoid: ["buzzfeed", "medium.com/@random"]

web_frameworks:
  prefer: ["official docs", "github.com"]
  check_version: true  # flag outdated version info
```

## Extraction Rules

### Entities (type: entity)
- Named tools, projects, people, organizations
- Must have concrete defining characteristics
- Threshold: ≥3 mentions across sources for wiki/ promotion

### Concepts (type: concept)
- Patterns, principles, techniques
- Must be generalizable beyond single context
- Threshold: ≥3 mentions for wiki/ promotion

### Claims
- Extract with source attribution
- Mark uncertain claims with `[uncertainty: reason]`
- Track contradictions for decision records

## Output Sections

Every synthesis must include:
1. Overview — topic summary
2. Key Findings — numbered list
3. Entities — extracted with brief description
4. Concepts — patterns/techniques discovered
5. Contradictions — where sources disagree
6. Open Questions — gaps in research
7. Counter-arguments — strongest critiques
8. Sources — numbered list with URLs
