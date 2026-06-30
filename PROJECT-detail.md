# PROJECT-detail.md — Personal Branding Scorer on LinkedIn (Skill #150)

**Slug:** `linkedin-personal-branding-scorer`
**Cluster:** `marketing-content-branding`
**Source idea:** 150
**Phase:** Built (v1) — production-grade, opensource-ready

## Executive Summary
Scores and optimizes a LinkedIn personal brand (profile + content strategy)
against distribution-algorithm and thought-leadership best practices. This skill
is a full Claude harness in the **marketing-content-branding** cluster. It runs a
research-first, framework-grounded workflow that scores the subject against named
world-renowned methodologies and returns a prioritized improvement roadmap,
while continuously updating its knowledge base via `tools/knowledge_updater.py`.

## Problem Statement
Professionals underperform on LinkedIn because their profile lacks
keyword/authority signals and their content ignores the distribution algorithm.
This skill audits the profile and content plan, scores brand strength across
five weighted dimensions, and prescribes a posting roadmap traceable to scored
findings.

## Target Users & Use Cases
Practitioners, reviewers, and decision-makers who need an expert-grade,
evidence-based assessment in this domain. Trigger examples:

1. **Profile audit** — User: "Score my LinkedIn profile" → Skill scores 5
   dimensions, names gaps, prescribes rewrites.
2. **Content plan** — User: "Plan my next month of LinkedIn posts" → Skill
   builds a pillar-based calendar aligned to the distribution algorithm.
3. **Niche pivot** — User: "Reposition me as an AI consultant" → Skill rewrites
   headline/About via Golden Circle, scores fit.
4. **Engagement slump** — User: "Why is my reach dropping?" → Skill diagnoses
   dwell-time/format issues, roadmap to recover.
5. **Degraded mode** — User: "Audit offline" → Falls back to SECOND-KNOWLEDGE-BRAIN
   heuristics, flags that algorithm data may be stale.

## Harness Architecture
```
/linkedin-personal-branding-scorer (main.md)
   ├── sub-intake .................... Intake & Context Gathering
   ├── sub-framework-selector ........ Evaluation Framework Selector
   ├── [research] WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN
   ├── sub-scoring-engine ............ Scoring Engine (5 weighted dimensions)
   ├── [challenge] devil's-advocate assumption review
   ├── sub-improvement-roadmap ....... Improvement Roadmap (effort × impact)
   └── synthesize ................... professional deliverable + Quality Gates
```

## Full Sub-Skill Catalog
### sub-intake — Intake & Context Gathering
- **Purpose:** Collect structured inputs, scope, and goals; ask clarifying
  questions when key facts are missing.
- **Inputs:** raw user request, prior-stage context.
- **Outputs:** an `IntakeContext` block (subject, scope, goals, constraints,
  available inputs, missing inputs).
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** intake is complete and internally consistent, and every
  missing input is either requested explicitly or flagged as an assumption.

### sub-framework-selector — Evaluation Framework Selector
- **Purpose:** Pick the smallest covering set of named world-renowned framework(s)
  and justify inclusion/exclusion.
- **Inputs:** IntakeContext.
- **Outputs:** a `FrameworkChoice` block (selected frameworks, rationale,
  exclusion rationale, expected coverage).
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** each selected framework is justified and covers ≥1 scoring
  dimension; no dimension is left uncovered.

### sub-scoring-engine — Scoring Engine
- **Purpose:** Apply the multi-dimensional rubric to produce 0-100 weighted
  scores with evidence citations per dimension.
- **Inputs:** IntakeContext + FrameworkChoice + research evidence.
- **Outputs:** a `Scorecard` block (per-dimension scores + evidence + weighted
  total + letter grade).
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** every dimension score cites ≥1 source or framework; weighted
  total sums to the dimensions' weights (25/25/20/20/10).

### sub-improvement-roadmap — Improvement Roadmap
- **Purpose:** Generate a prioritized, effort/impact-ranked recommendation set
  traceable to scored findings.
- **Inputs:** Scorecard + IntakeContext.
- **Outputs:** a `Roadmap` block (ranked actions with effort, impact, owner,
  traceable finding IDs).
- **Tools:** Read.
- **Quality gate:** each roadmap item links to ≥1 finding; items sorted by
  impact/effort; quick wins surfaced first.

## Evaluation Frameworks (World-Renowned, Citable)
| Framework / Standard | Role in this skill |
|---|---|
| Personal brand pillars (expertise/visibility/relationships) | Defines the brand positioning model. |
| LinkedIn Social Selling Index (SSI) | Benchmarks professional brand activity (0-100). |
| LinkedIn content distribution algorithm | Dwell-time, early engagement, format weighting. |
| Sinek's Golden Circle (Why-How-What) | Clarifies authentic positioning and message ordering. |
| Halo effect & authority bias | Credibility cues that compound reach. |

Real, citable sources for each framework are stored in `SECOND-KNOWLEDGE-BRAIN.md`.

## Evidence Hierarchy (prefer higher tier)
1. Systematic review / meta-analysis
2. Peer-reviewed primary study (RCT, cohort)
3. Primary vendor/standards source (LinkedIn, IEEE, etc.)
4. Practitioner-grade report (Sprout, Hootsuite)
5. Expert opinion / vendor blog
6. SECOND-KNOWLEDGE-BRAIN fallback (graceful degradation)

When live evidence is unavailable, the skill MAY cite tier 6 entries but MUST
state the limitation explicitly in the final deliverable.

## Scoring Model
| Dimension | Weight | What is assessed |
|---|---|---|
| Profile completeness & keyword SEO | 25% | headline, about, skills, featured optimized for search |
| Content strategy & cadence | 25% | pillar topics, format mix, posting frequency |
| Engagement & network quality | 20% | comments, dwell-time, relevant connections |
| Authority & credibility signals | 20% | proof, endorsements, thought-leadership depth |
| Voice consistency & differentiation | 10% | distinct, consistent positioning |

Each dimension is scored 0-100 with cited evidence; the weighted total yields an
overall grade: **A** 90+, **B** 75-89, **C** 60-74, **D** <60.

### Per-dimension sub-criteria (used by `sub-scoring-engine`)
- **Profile completeness & keyword SEO (25%):** headline keyword density &
  clarity (25), About length & narrative (20), experience entries with
  measurable outcomes (20), skills (10), featured/proof assets (15), banner &
  contact info (10).
- **Content strategy & cadence (25%):** defined pillar set (25), format mix
  per algorithm weighting (25), posting frequency & consistency (25),
  pillar-to-headline alignment (25).
- **Engagement & network quality (20%):** comment depth vs. vanity (30),
  early engagement velocity signals (25), connection relevance & concentration
  (25), dwell-time-friendly formats (20).
- **Authority & credibility signals (20%):** proof/featured assets (30),
  endorsements & recommendations (25), thought-leadership depth (25),
  external citations/press (20).
- **Voice consistency & differentiation (10%):** distinct positioning vs.
  peers (40), consistent tone across posts (30), Golden Circle Why-clarity (30).

## Skill File Format Specification
- Frontmatter: `name`, `description`.
- Required sections: Role & Persona, Workflow (Harness Flow), Sub-skills
  Available, Tools, Output Format, Quality Gates.
- Sub-skill files additionally expose Inputs, Process, Output, Quality Gate.

## E2E Execution Flow
1. Parse user request; if inputs are insufficient, `sub-intake` asks targeted
   questions (max one round, then proceed on flagged assumptions).
2. `sub-framework-selector` picks framework(s) and justifies the choice.
3. Research stage gathers highest-tier evidence; degrade gracefully to
   SECOND-KNOWLEDGE-BRAIN if offline and flag the limitation.
4. `sub-scoring-engine` scores each dimension 0-100 with citations and computes
   the weighted total + letter grade.
5. Challenge stage stress-tests assumptions and grades certainty.
6. `sub-improvement-roadmap` produces ranked, traceable actions.
7. Synthesize the deliverable; run Quality Gates; present.

**Error handling:** missing inputs → ask once, then proceed on assumptions;
conflicting evidence → present both, grade certainty; tool failure → fallback to
the brain + explicit limitation notice.

### Degraded-mode rules
- If `WebSearch`/`WebFetch` are unavailable, the engine cites
  SECOND-KNOWLEDGE-BRAIN entries and labels each affected score "offline-grade".
- If a dimension has zero usable evidence, it is scored with explicit "no
  evidence" certainty = low and excluded from the weighted total (weights are
  renormalized and the renormalization is stated in Limitations).

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: https://www.linkedin.com/business, https://sproutsocial.com/insights,
  https://blog.hootsuite.com, https://hbr.org
- ArXiv category: cs.SI
- Crawl queries: `linkedin algorithm ranking 2026`; `personal branding thought
  leadership research`; `social selling index benchmarks`; `b2b content
  engagement linkedin`
- Append format: dated entries with Title, Authors, Year, Venue, DOI/URL, key
  finding, relevance, and a `<!--hash:...-->` dedup token.

## Supporting Tools Spec
`tools/knowledge_updater.py`: inputs = source list + queries; outputs = appended
SECOND-KNOWLEDGE-BRAIN entries; schedule = weekly cron; dedup by URL/DOI hash;
relevance floor 0.10. See `tools/README.md` for CLI usage and `requirements.txt`
for dependencies.

## Quality Gates (must all pass before final output)
- Every score cites at least one source or the chosen framework.
- Challenge stage completed; key assumptions tested.
- Roadmap items are prioritized by effort and impact and traceable to findings.
- Limitations and evidence certainty are stated explicitly.
- Degraded mode, when active, is surfaced in the deliverable, not hidden.

## Test Scenarios
See `tests/test-scenarios.md` (5 scenarios incl. degraded mode) and the static
validator `tests/validate_skill.py`.

## Key Design Decisions
1. Framework-grounded scoring (no ad-hoc criteria).
2. Research-first with graceful degradation to the local knowledge brain.
3. Mandatory challenge stage to counter confirmation bias.
4. Standard Quality Gates enforced before delivery.
5. Self-improving knowledge base via weekly crawl with dedup + relevance floor.
6. Open-source-ready: static validator, tool README, requirements pinned.
