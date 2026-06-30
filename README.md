# Personal Branding Scorer on LinkedIn

**A Claude Skill that scores and optimizes a LinkedIn personal brand ? profile
plus content strategy ? against distribution-algorithm and thought-leadership
best practices.**

- **Skill ID:** #150
- **Cluster:** `marketing-content-branding`
- **Phase:** Built (v1) ? production-grade, open-source-ready
- **Language:** Markdown skill (Claude harness) + Python tooling

---

## Table of Contents
1. [Overview](#overview)
2. [Why this skill exists](#why-this-skill-exists)
3. [Key features](#key-features)
4. [How it works (harness)](#how-it-works-harness)
5. [Scoring model](#scoring-model)
6. [Evaluation frameworks](#evaluation-frameworks)
7. [Repository layout](#repository-layout)
8. [Quick start](#quick-start)
9. [Validate (offline)](#validate-offline)
10. [Knowledge updater (CLI)](#knowledge-updater-cli)
11. [Configuration](#configuration)
12. [Scheduling](#scheduling)
13. [Composability](#composability)
14. [Testing](#testing)
15. [Documentation](#documentation)
16. [Design decisions](#design-decisions)
17. [License](#license)

---

## Overview

`linkedin-personal-branding-scorer` is a research-first, framework-grounded
Claude harness. It audits a LinkedIn profile and its content plan, scores brand
strength across five weighted dimensions (0?100 each), runs a devil's-advocate
challenge on its own conclusions, and returns a prioritized, traceable
improvement roadmap. While it runs, a self-improving knowledge brain grows
weekly via a `crawl4ai` pipeline so the skill keeps getting smarter.

The skill is built to be **defensible, not opinionated**: every score cites a
real source or a named world-renowned framework, limitations are stated
explicitly, and it degrades gracefully to offline heuristics when live evidence
is unavailable.

## Why this skill exists

Professionals underperform on LinkedIn for two compounding reasons:

1. **Profile weakness** ? headlines, About sections, and skills lack the keyword
   and authority signals that make the profile discoverable and credible.
2. **Content weakness** ? content ignores the distribution algorithm
   (dwell-time, early engagement velocity, format weighting), so even good posts
   get buried.

This skill audits both, scores both, and prescribes a posting roadmap that is
traceable to the scored findings ? so the user knows *why* each action matters.

## Key features

- **Framework-grounded scoring.** Five dimensions mapped to named, citable
  frameworks; no ad-hoc criteria.
- **Evidence-cited by default.** Every dimension score carries at least one
  citation and an evidence tier (`primary`, `practitioner`, or `offline`).
- **Mandatory challenge stage.** A devil's-advocate pass tests the top
  assumptions and grades certainty (high / medium / low).
- **Traceable roadmap.** Every recommendation links back to a finding ID (`F#`)
  and is ranked by impact-per-effort, with quick wins surfaced first.
- **Graceful degradation.** Without network access it falls back to the
  `SECOND-KNOWLEDGE-BRAIN.md` knowledge base and labels affected scores
  `evidence_tier: offline` instead of failing.
- **Self-improving knowledge brain.** `tools/knowledge_updater.py` crawls ArXiv
  (`cs.SI`) and authoritative domain sources weekly, dedups by URL hash, and
  appends date-stamped entries.
- **Offline static validator.** `tests/validate_skill.py` checks repo layout,
  frontmatter, required sections, scoring weight sums, and knowledge-brain
  hash-token integrity ? no network, no model.
- **Open-source ready.** README, requirements, example config, `.gitignore`,
  tool README, and a typed stage-contract model for cross-skill composition.

## How it works (harness)

The main skill (`skills/main.md`) orchestrates a strict stage order. Each stage
emits a typed block that the next stage consumes. Quality gates block progress
on failure.

```
                        ???????????????????????????????????????????????
   user request ???????? ? sub-intake            -> IntakeContext     ?
                        ???????????????????????????????????????????????
                        ? sub-framework-selector-> FrameworkChoice    ?
                        ???????????????????????????????????????????????
                        ? research (WebSearch/WebFetch + Brain)       ?
                        ?                      -> EvidencePack        ?
                        ???????????????????????????????????????????????
                        ? sub-scoring-engine    -> Scorecard          ?
                        ???????????????????????????????????????????????
                        ? challenge (devil's advocate)                ?
                        ?                      -> ChallengeReport     ?
                        ???????????????????????????????????????????????
                        ? sub-improvement-roadmap-> Roadmap          ?
                        ???????????????????????????????????????????????
                        ? synthesize + Quality Gates -> deliverable   ?
                        ???????????????????????????????????????????????
```

**Stage contracts** (what each stage produces and consumes):

| Stage | Produces | Consumes |
|---|---|---|
| `sub-intake` | `IntakeContext` | raw request |
| `sub-framework-selector` | `FrameworkChoice` | `IntakeContext` |
| research | `EvidencePack` | `IntakeContext` + `FrameworkChoice` |
| `sub-scoring-engine` | `Scorecard` | `IntakeContext` + `FrameworkChoice` + `EvidencePack` |
| challenge | `ChallengeReport` | `Scorecard` |
| `sub-improvement-roadmap` | `Roadmap` | `IntakeContext` + `Scorecard` + `ChallengeReport` |
| synthesize | professional deliverable | all of the above + Quality Gates |

## Scoring model

Five dimensions, weights summing to 100%. Each dimension is scored 0?100 with at
least one citation per dimension; the weighted total maps to a letter grade.

| Dimension | Weight | What is assessed |
|---|---:|---|
| Profile completeness & keyword SEO | 25% | headline, about, skills, featured ? optimized for search |
| Content strategy & cadence | 25% | pillar topics, format mix, posting frequency |
| Engagement & network quality | 20% | comments, dwell-time, relevant connections |
| Authority & credibility signals | 20% | proof, endorsements, thought-leadership depth |
| Voice consistency & differentiation | 10% | distinct, consistent positioning |
| **Total** | **100%** | weighted across all five dimensions |

**Grade bands:** A (90+), B (75?89), C (60?74), D (<60).

If a dimension has zero usable evidence, it is excluded from the total, the
remaining weights are renormalized, and the renormalization is stated explicitly
in the deliverable's Limitations section.

### Per-dimension sub-criteria

Each dimension is scored against its own sub-criteria (intra-dimension weights
sum to 100). Full detail lives in `skills/sub-scoring-engine.md`.

## Evaluation frameworks

All frameworks are named, world-renowned, and citable. Real sources for each are
stored in `SECOND-KNOWLEDGE-BRAIN.md` with stable dedup hash tokens.

| Framework / Standard | Role in this skill |
|---|---|
| Personal brand pillars (expertise / visibility / relationships) | Defines the brand positioning model. |
| LinkedIn Social Selling Index (SSI) | Benchmarks professional brand activity (0?100). |
| LinkedIn content distribution algorithm | Dwell-time, early engagement, format weighting. |
| Sinek's Golden Circle (Why?How?What) | Clarifies authentic positioning and message ordering. |
| Halo effect & authority bias | Credibility cues that compound reach. |

**Evidence hierarchy** (prefer higher tier):
Systematic review / meta-analysis ? peer-reviewed primary study ? primary
vendor/standards source ? practitioner-grade report ? expert opinion / vendor
blog ? `SECOND-KNOWLEDGE-BRAIN.md` fallback (offline).

## Repository layout

```
linkedin-personal-branding-scorer/
??? skills/
?   ??? main.md                       Harness orchestration + quality gates
?   ??? sub-intake.md                 Intake & Context Gathering
?   ??? sub-framework-selector.md     Evaluation Framework Selector
?   ??? sub-scoring-engine.md         Scoring Engine (rubric + sub-criteria)
?   ??? sub-improvement-roadmap.md    Improvement Roadmap (effort x impact)
??? tools/
?   ??? knowledge_updater.py          crawl4ai pipeline + CLI (self-improving brain)
?   ??? README.md                     Tool usage & scheduling
??? tests/
?   ??? test-scenarios.md             5 behavioral scenarios (incl. degraded mode)
?   ??? validate_skill.py             Offline static validator
??? SECOND-KNOWLEDGE-BRAIN.md         Self-improving knowledge base
??? PROJECT-detail.md                 Full technical spec
??? PROJECT-DEVELOPMENT-PHASE-TRACKING.md
??? CLAUDE.md                         Skill + cross-skill wiring notes
??? README.md                         This file
??? requirements.txt
??? config.example.json
??? .gitignore
```

## Quick start

### As a Claude Skill
1. Open this directory in Claude (it reads `CLAUDE.md` and `skills/main.md`).
2. Trigger with a request, for example: *"Score my LinkedIn profile"* and paste
   your profile text.
3. The harness runs end-to-end and returns a professional deliverable: executive
   summary, dimension scores with citations, findings & risks, challenge notes,
   a prioritized roadmap, limitations, and sources.

### Standalone knowledge updater
```bash
pip install -r requirements.txt                 # crawl4ai is the only optional dep
python tools/knowledge_updater.py --dry-run     # see what would be appended
python tools/knowledge_updater.py               # write to SECOND-KNOWLEDGE-BRAIN.md
```

The updater degrades gracefully: if `crawl4ai` or the network is unavailable it
logs and exits 0 so the skill keeps working off the existing knowledge brain.

## Validate (offline)

No network and no model are required.

```bash
python tests/validate_skill.py
```

This checks:
- Required files and directories exist.
- Every skill markdown file has `name` and `description` frontmatter.
- `main.md` has all required sections.
- Each `sub-*.md` exposes Role, Purpose, Inputs, Process, Output, Quality Gate.
- The scoring dimensions table sums to 100% with the five canonical dimensions.
- Every `<!--hash:...-->` token in the knowledge brain is unique and well-formed.

Expected output: `PASS - all static checks succeeded.` (exit code 0).

## Knowledge updater (CLI)

`tools/knowledge_updater.py` is the self-improving crawl pipeline. It fetches the
latest ArXiv `cs.SI` records and authoritative domain pages, parses them, scores
relevance, deduplicates by a stable URL hash, and appends date-stamped entries to
`SECOND-KNOWLEDGE-BRAIN.md`.

```text
usage: knowledge_updater.py [-h] [--brain BRAIN] [--limit LIMIT]
                            [--relevance-floor RELEVANCE_FLOOR] [--dry-run]
                            [--no-network] [--verbose] [--event-log EVENT_LOG]
                            [--config CONFIG]
```

| Flag | Default | Purpose |
|---|---|---|
| `--brain` | `../SECOND-KNOWLEDGE-BRAIN.md` | Path to the knowledge brain |
| `--limit` | 50 | Max candidate entries to keep |
| `--relevance-floor` | 0.10 | Minimum relevance score to append an entry |
| `--dry-run` | off | Compute but do not write to the brain |
| `--no-network` | off | Skip all live fetches |
| `-v` / `--verbose` | off | Debug logging |
| `--event-log` | none | JSONL event log path for observability |
| `--config` | none | JSON config file overriding defaults |

**Dedup model.** Each appended line carries a stable
`<!--hash:16hex-->` token computed as
`sha256(normalize_url(url))[:16]`. Existing hashes are scanned from the brain on
every run, so appends are idempotent.

**Graceful degradation.** If `crawl4ai` is not installed, the updater logs and
exits 0. The skill keeps working off the existing brain.

## Configuration

Defaults are baked into the tool. To override, copy and edit the example config:

```bash
cp config.example.json config.json
python tools/knowledge_updater.py --config config.json
```

```json
{
  "arxiv_categories": ["cs.SI"],
  "web_sources": [
    "https://www.linkedin.com/business",
    "https://www.linkedin.com/blog/engineering",
    "https://sproutsocial.com/insights",
    "https://blog.hootsuite.com",
    "https://hbr.org"
  ],
  "search_queries": [
    "linkedin algorithm ranking 2026",
    "personal branding thought leadership research",
    "social selling index benchmarks",
    "b2b content engagement linkedin"
  ],
  "relevance_floor": 0.10,
  "limit": 50
}
```

## Scheduling

A weekly cron refreshes the knowledge brain. Example:

```text
0 3 * * 1 cd /path/to/linkedin-personal-branding-scorer && \
    python tools/knowledge_updater.py --event-log logs/knowledge_events.jsonl
```

## Composability

This skill is part of the `marketing-content-branding` cluster and exposes typed
stage outputs so sibling skills can compose around it.

| Surface | Provided by | Consumable by sibling skill |
|---|---|---|
| `IntakeContext` | `sub-intake` | Any content/branding skill needing structured profile+goal intake. |
| `FrameworkChoice` | `sub-framework-selector` | Branding/positioning skills sharing the brand-pillars & Golden Circle frameworks. |
| `Scorecard` (5 dimensions, `F#` findings) | `sub-scoring-engine` | Content-calendar or ad-creative skills needing a brand baseline. |
| `Roadmap` (quick wins + themes) | `sub-improvement-roadmap` | Execution/automation skills acting on prioritized actions. |
| `SECOND-KNOWLEDGE-BRAIN.md` | `tools/knowledge_updater.py` | Any cluster skill may Read it as an offline evidence fallback. |

**Ownership rule:** writes to the knowledge brain are owned exclusively by
`tools/knowledge_updater.py` to preserve hash-token dedup integrity; sibling
skills should only read it.

## Testing

Two complementary layers, both offline:

1. **Static validation** ? `tests/validate_skill.py` verifies file structure,
   frontmatter, sections, weight sums, and brain hash-token integrity.
2. **Behavioral scenarios** ? `tests/test-scenarios.md` defines five scenarios
   (profile audit, content plan, niche pivot, engagement slump, and offline
   degraded mode), each with golden-path assertions the harness must satisfy.

```bash
python tests/validate_skill.py
python tools/knowledge_updater.py --no-network --dry-run
```

## Documentation

- `PROJECT-detail.md` ? full technical spec (scoring model, evidence hierarchy,
  degraded-mode rules, E2E flow).
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` ? phase roadmap and status.
- `SECOND-KNOWLEDGE-BRAIN.md` ? self-improving knowledge base.
- `CLAUDE.md` ? skill summary plus cross-skill wiring notes.
- `tools/README.md` ? updater CLI reference.

## Design decisions

1. **Framework-grounded scoring.** No ad-hoc criteria; every dimension maps to a
   named, citable framework.
2. **Research-first with graceful degradation.** Live evidence is preferred;
   when offline, the brain is used and the limitation is stated plainly.
3. **Mandatory challenge stage.** A devil's-advocate pass counters confirmation
   bias and grades certainty.
4. **Standard quality gates enforced before delivery.** No deliverable ships
   unless every gate passes.
5. **Self-improving knowledge base.** Weekly crawl with URL-hash dedup and a
   relevance floor keeps the brain focused and fresh.
6. **Open-source ready.** Pinned requirements, example config, offline
   validator, `.gitignore`, and a README.

## License

MIT. Built as an open-source-ready Claude Skill.

---
