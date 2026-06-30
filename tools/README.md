# tools/knowledge_updater.py

Self-improving crawl pipeline for Skill #150 ? *Personal Branding Scorer on
LinkedIn* (cluster: `marketing-content-branding`).

## What it does
1. Fetches the latest ArXiv `cs.SI` records and authoritative domain pages
   (LinkedIn, Sprout, Hootsuite, HBR) using `crawl4ai`.
2. Parses each page into a structured record (title, venue, year, URL, abstract).
3. Scores relevance against the skill's domain keywords.
4. Appends new, deduplicated, date-stamped entries to
   `SECOND-KNOWLEDGE-BRAIN.md`.
5. Writes an optional JSONL event log for observability.

## Why it never fails the skill
If `crawl4ai` or the network is unavailable, the updater logs and exits 0 so
the skill keeps working off the existing knowledge brain (graceful degradation).

## Install
```bash
pip install -r requirements.txt   # crawl4ai is the only optional dependency
```

## Usage
```bash
# Normal weekly run (writes to ../SECOND-KNOWLEDGE-BRAIN.md)
python tools/knowledge_updater.py

# Dry-run: compute and print what would be appended, but write nothing
python tools/knowledge_updater.py --dry-run

# Skip all network I/O (still useful for schema/log testing)
python tools/knowledge_updater.py --no-network

# Verbose + custom brain + event log
python tools/knowledge_updater.py -v --brain path/to/brain.md --event-log events.jsonl

# Override defaults via JSON config
python tools/knowledge_updater.py --config config.json
```

## Config (optional `config.json`)
```json
{
  "arxiv_categories": ["cs.SI"],
  "web_sources": ["https://www.linkedin.com/business", "https://sproutsocial.com/insights"],
  "search_queries": ["linkedin algorithm ranking 2026", "personal branding thought leadership research"],
  "relevance_floor": 0.10,
  "limit": 50
}
```

## CLI flags
| Flag | Default | Purpose |
|---|---|---|
| `--brain` | `../SECOND-KNOWLEDGE-BRAIN.md` | Path to the knowledge brain |
| `--limit` | 50 | Max candidate entries to keep |
| `--relevance-floor` | 0.10 | Minimum relevance to append |
| `--dry-run` | off | Compute but do not write |
| `--no-network` | off | Skip all live fetches |
| `-v/--verbose` | off | Debug logging |
| `--event-log` | none | JSONL event log path |
| `--config` | none | JSON config file overriding defaults |

## Scheduling (recommended)
Weekly cron:
```
0 3 * * 1 cd /path/to/skill && python tools/knowledge_updater.py --event-log logs/knowledge_events.jsonl
```

## Dedup model
Each appended line carries a stable `<!--hash:16hex-->` token computed as
`sha256(normalize_url(url))[:16]`. Existing hashes are scanned from the brain on
every run so appends are idempotent.

## Testing without network
```bash
python tools/knowledge_updater.py --no-network --dry-run
```
Exits 0 with "no new entries this run" ? confirms graceful degradation.
