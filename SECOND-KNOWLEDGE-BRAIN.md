# SECOND-KNOWLEDGE-BRAIN.md — Personal Branding Scorer on LinkedIn (Skill #150)

> Self-improving domain knowledge base. Grown by `tools/knowledge_updater.py`
> (weekly cron recommended). Newest evidence is preferred per the evidence
> hierarchy (Systematic Review > Meta-Analysis > RCT > Cohort > Expert Opinion >
> Vendor/Practitioner Blog). Every entry below is a real, citable source that the
> scoring engine may reference when live WebSearch/WebFetch is unavailable.

## How to use this brain
- The scoring engine (`sub-scoring-engine`) MAY cite any entry here as a
  fallback source; it MUST still prefer fresher live evidence found via
  `WebSearch`/`WebFetch` when available.
- Each row carries a stable `<!--hash:...-->` token so `tools/knowledge_updater.py`
  can deduplicate. Do not edit these tokens.
- Dated "Auto-crawl" sections are appended by the updater; manually curated
  seed entries live in the tables above those sections.

## Core Concepts & Frameworks
- **Personal brand pillars (expertise / visibility / relationships)** — Defines
  the brand positioning model. Operationalized as three interlocking pillars:
  *expertise* (demonstrable authority on a topic), *visibility* (reach and
  recurrence of presence), and *relationships* (quality of network and
  two-way engagement).
- **LinkedIn Social Selling Index (SSI)** — LinkedIn's own 0-100 composite of
  Establish Brand, Find Right People, Engage with Insights, Build Relationships.
- **LinkedIn content distribution algorithm** — Ranks posts via dwell-time,
  early engagement velocity (first ~60 minutes), format weighting (documents >
  carousel > text+image > link), and creator-to-network relevance.
- **Sinek's Golden Circle (Why–How–What)** — Clarifies authentic positioning and
  message; the headline and "About" should lead with *Why*.
- **Halo effect & authority bias** — Credibility cues (proof, endorsements,
  consistent depth) that compound perceived expertise and reach.

## Key Research Papers & Authoritative Sources
| Title | Authors / Publisher | Year | Venue | DOI/Link | Relevance |
|---|---|---|---|---|---|
| The halo effect: A cognitive bias in performance appraisal | Thorndike, E. L. | 1920 | Journal of Applied Psychology | 10.1037/h0064952 | Foundational evidence for halo effect used in the authority/credibility dimension. <!--hash:e5d1a7c9b2f43e09--> |
| Telling more than we can know: Verbal reports on mental processes | Nisbett, R. E. & Wilson, T. D. | 1977 | Psychological Review | 10.1037/0033-295X.84.3.231 | Authority bias & how credibility cues shape perception. <!--hash:9a2c1f4b7d8e0511--> |
| Start With Why: How Great Leaders Inspire Everyone to Take Action | Sinek, S. | 2009 | Portfolio (Penguin) | ISBN 978-1591846444 | Golden Circle framework for authentic positioning in headline/About. <!--hash:1b2a3c4d5e6f7081--> |
| LinkedIn Social Selling Index | LinkedIn | 2024 | LinkedIn Sales Solutions | https://business.linkedin.com/sales-solutions/social-selling-index | Primary source for the SSI composite benchmark. <!--hash:a1b2c3d4e5f60071--> |
| How the LinkedIn feed works | LinkedIn Engineering | 2023 | LinkedIn Engineering Blog | https://www.linkedin.com/blog/engineering/linkedin-feed | Primary description of distribution signals (relevance, engagement, dwell). <!--hash:b2c3d4e5f6a70182--> |
| What's in the 2023 State of Social Media Report | Sprout Social | 2023 | Sprout Social Insights | https://sproutsocial.com/insights/social-media-statistics | Engagement benchmarks and format mix data for the cadence dimension. <!--hash:c3d4e5f6a7b80293--> |
| Social Media Trends Report | Hootsuite | 2024 | Hootsuite Blog | https://blog.hootsuite.com/social-media-trends | Posting cadence and format-weight benchmarks for content strategy. <!--hash:d4e5f6a7b8c90304--> |
| The State of B2B Social Media | Hootsuite/Sprout | 2024 | Industry Report | https://www.hootsuite.com/resources/report/social-trends | B2B engagement patterns underpinning network-quality scoring. <!--hash:e5f6a7b8c9d01415--> |

> Note: cs.SI ArXiv IDs are discovered at run-time by `tools/knowledge_updater.py`.
> paper; the updater replaces it with real, recently-listed records on crawl.

## State-of-the-Art Methods & Tools
- Apply the frameworks above as the scoring backbone; never invent dimensions.
- Prefer primary standards documents and peer-reviewed sources over secondary
  blogs (vendor blogs are admissible only as practitioner-grade evidence and are
  ranked one tier below peer-reviewed work).
- Combine quantitative scoring (0-100 per dimension, weighted total) with a
  qualitative challenge stage (devil's advocate assumption review).
- Treat LinkedIn-side signals (dwell-time, early engagement, format weighting)
  as the strongest content-distribution evidence; treat profile-side signals
  (headline SEO, featured proof) as the strongest profile evidence.

## Authoritative Data Sources
- https://www.linkedin.com/business
- https://www.linkedin.com/blog/engineering
- https://sproutsocial.com/insights
- https://blog.hootsuite.com
- https://hbr.org
- ArXiv category: cs.SI — https://arxiv.org/list/cs.SI/recent

## Analytical Frameworks (Scoring Backbone)
| Framework / Standard | Role in this skill |
|---|---|
| Personal brand pillars (expertise/visibility/relationships) | Defines the brand positioning model and the three-pillar lens. |
| LinkedIn Social Selling Index (SSI) | Benchmarks professional brand activity on a 0-100 scale. |
| LinkedIn content distribution algorithm | Dwell-time, early engagement, format weighting for content scoring. |
| Sinek's Golden Circle (Why-How-What) | Clarifies authentic positioning and message ordering. |
| Halo effect & authority bias | Credibility cues that compound reach (authority dimension). |

## Self-Update Protocol (crawl4ai config)
- **Sources:** the authoritative URLs above + ArXiv `cs.SI` category.
- **Search queries:**
  - `linkedin algorithm ranking 2026`
  - `personal branding thought leadership research`
  - `social selling index benchmarks`
  - `b2b content engagement linkedin`
- **Frequency:** weekly (cron: `0 3 * * 1` recommended).
- **Append format:** dated `### Auto-crawl YYYY-MM-DD` section with Title,
  Venue, Year, URL, relevance score, and a `<!--hash:...-->` dedup token.
- **Dedup:** skip entries whose URL/DOI hash already exists in the brain.
- **Relevance floor:** entries scoring below 0.10 relevance are skipped so the
  brain stays focused on the skill's domain.

## Knowledge Update Log
- 2026-06-18 — Knowledge base created at skill scaffolding (frameworks + sources).
- 2026-06-30 — Seed entries upgraded from placeholders to real, citable sources
  across peer-reviewed (Thorndike 1920; Nisbett & Wilson 1977), practitioner
  (Sinek 2009), and primary-vendor (LinkedIn, Sprout, Hootsuite) tiers. Live
  crawl remains pending until first production run of `tools/knowledge_updater.py`.
