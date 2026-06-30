# Test Scenarios ? Personal Branding Scorer on LinkedIn (Skill #150)

These scenarios validate the harness end-to-end: stage order, framework grounding,
scoring with citations, gates, roadmap, and graceful degradation. Each scenario
lists **Inputs**, **Expected behavior**, and **Golden-path assertions** that must
all pass for the run to be accepted. The static validator
(`tests/validate_skill.py`) checks the file structure independently of these
behavioral scenarios.

### Scenario 1: Profile audit
- **Inputs:** "Score my LinkedIn profile" (plus pasted profile text).
- **Expected behavior:** Skill scores all 5 dimensions, names gaps, prescribes
  profile rewrites.
- **Golden-path assertions:**
  - [ ] Stage order = intake -> framework -> research -> score -> challenge -> roadmap -> synthesize.
  - [ ] `intent == profile_audit`.
  - [ ] At least one named framework selected and justified.
  - [ ] Every dimension score cites >=1 source or framework.
  - [ ] Roadmap contains >=1 quick win traceable to an `F#` finding.
  - [ ] Limitations + certainty stated.

### Scenario 2: Content plan
- **Inputs:** "Plan my next month of LinkedIn posts" (plus recent posts or profile).
- **Expected behavior:** Skill builds a pillar-based calendar aligned to the
  distribution algorithm.
- **Golden-path assertions:**
  - [ ] `intent == content_plan`.
  - [ ] LinkedIn distribution algorithm framework is selected (covers cadence).
  - [ ] Calendar lists pillar topics, formats (per algorithm weighting), and a
        cadence that respects the user's posting capacity.
  - [ ] Dimension scores cited; limitations stated.

### Scenario 3: Niche pivot
- **Inputs:** "Reposition me as an AI consultant" (plus existing profile).
- **Expected behavior:** Skill rewrites headline/About via Golden Circle and
  scores fit.
- **Golden-path assertions:**
  - [ ] `intent == niche_pivot`.
  - [ ] Sinek Golden Circle framework selected; rewritten headline/About lead
        with *Why*.
  - [ ] Fit score computed for the target niche with cited evidence.
  - [ ] Roadmap prioritizes repositioning actions (effort x impact).

### Scenario 4: Engagement slump
- **Inputs:** "Why is my reach dropping?" (plus recent posts + trend direction).
- **Expected behavior:** Skill diagnoses dwell-time/format issues and produces a
  recovery roadmap.
- **Golden-path assertions:**
  - [ ] `intent == engagement_slump`.
  - [ ] Diagnosis references dwell-time and format weighting explicitly.
  - [ ] Challenge stage tests the "reach drop = algorithm penalty" assumption
        and assigns certainty.
  - [ ] Recovery roadmap is traceable to findings; limitations stated.

### Scenario 5: Degraded mode (offline)
- **Inputs:** "Audit offline" (WebSearch/WebFetch unavailable).
- **Expected behavior:** Skill falls back to SECOND-KNOWLEDGE-BRAIN heuristics and
  flags that algorithm data may be stale.
- **Golden-path assertions:**
  - [ ] All affected dimension scores tagged `evidence_tier: offline`.
  - [ ] Executive Summary + Limitations explicitly state degraded mode is active.
  - [ ] SECOND-KNOWLEDGE-BRAIN citations are real, hash-tokened entries.
  - [ ] Skill exits with a deliverable, not an error (graceful degradation).

## Regression Notes
- Add real user runs here as regression cases (Inputs + observed scores).
- Verify `tools/knowledge_updater.py --dry-run --no-network` exits 0 and appends
  nothing (graceful degradation).
- Verify dedup: re-running the updater must not duplicate existing hash tokens.

## Static validation (run before release)
```bash
python tests/validate_skill.py
```
This checks frontmatter, required sections, sub-skill presence, weight sums, and
knowledge-brain hash-token integrity ? see `tests/validate_skill.py`.
