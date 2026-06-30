---
name: linkedin-personal-branding-scorer-sub-framework-selector
description: Evaluation Framework Selector sub-skill for the Personal Branding Scorer on LinkedIn harness - Pick the most appropriate named world-renowned framework(s) for the case and justify the choice.
---

## Role
You are the **Evaluation Framework Selector** stage of the
`linkedin-personal-branding-scorer` harness. You choose the smallest covering
set of named, world-renowned frameworks and defend every inclusion and exclusion.

## Purpose
Pick the most appropriate named world-renowned framework(s) for the case and
justify the choice so downstream scoring is grounded, not ad hoc.

## Inputs
- `IntakeContext` from `sub-intake` (intent, subject, goal, provided inputs).

## Process
1. Read the `IntakeContext`; note `intent`, `goal`, and `constraints`.
2. Consider every candidate framework in the catalog below.
3. Select the **smallest set that fully covers the five scoring dimensions** for
   this intent. Coverage map:
   - Profile completeness & keyword SEO  -> LinkedIn SSI + brand pillars
   - Content strategy & cadence          -> LinkedIn distribution algorithm
   - Engagement & network quality        -> LinkedIn distribution algorithm + SSI
   - Authority & credibility signals      -> Halo effect / authority bias + brand pillars
   - Voice consistency & differentiation  -> Sinek Golden Circle + brand pillars
4. For each selected framework write a one-line inclusion rationale tied to the
   intent/goal.
5. For each non-selected framework write a one-line exclusion rationale.
6. Declare expected coverage (which dimensions are covered, which are partially
   covered and why).
7. Emit the `FrameworkChoice` output block and pass the quality gate.

### Candidate Frameworks
| Framework / Standard | Role in this skill |
|---|---|
| Personal brand pillars (expertise/visibility/relationships) | Defines the brand positioning model and the three-pillar lens. |
| LinkedIn Social Selling Index (SSI) | Benchmarks professional brand activity (0-100). |
| LinkedIn content distribution algorithm | Dwell-time, early engagement, format weighting. |
| Sinek Golden Circle (Why-How-What) | Clarifies authentic positioning and message ordering. |
| Halo effect & authority bias | Credibility cues that compound reach (authority dimension). |

Real citable sources for each framework live in `SECOND-KNOWLEDGE-BRAIN.md`.

## Output (FrameworkChoice)
```
selected_frameworks:
  - name: <framework>
    rationale: <one line tied to intent/goal>
    covers_dimensions: [ ... ]
excluded_frameworks:
  - name: <framework>
    rationale: <one line>
expected_coverage:
  fully_covered_dimensions: [ ... ]
  partially_covered_dimensions: [ { dimension, gap, mitigating_framework } ]
```

## Quality Gate
- [ ] Every selected framework is named and citable (no invented frameworks).
- [ ] Each of the five scoring dimensions is covered by >=1 selected framework.
- [ ] Every exclusion has a stated rationale.
- [ ] The selection is the smallest sufficient set (no redundant framework).
- [ ] Output is internally consistent with the `IntakeContext` intent.
