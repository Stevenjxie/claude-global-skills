# AI UI patterns

## Contents

1. Shared anatomy
2. Knowledge guide
3. Data analyst
4. Workflow copilot
5. Generative workspace
6. Embedded assistant
7. Responsive and visual rules

## 1. Shared anatomy

Use only the modules the job needs:

1. identity and status;
2. scope/context;
3. starter prompts or recent work;
4. conversation or artifact viewport;
5. structured answer blocks;
6. sources/trust footer;
7. follow-up/actions;
8. persistent composer.

The first screen should answer:

- What can this AI do?
- What context is it using?
- What is a good first request?
- Will it change anything?

Starter prompts must be real capabilities, not marketing slogans.

## 2. Knowledge guide

Recommended stack:

```text
Header: identity + status + new conversation
Hero: job-focused greeting + capability boundary
Scope panel: knowledge domain + freshness
Starter prompts: 3–6 representative questions
Answer: direct explanation + steps + location/link
Trust footer: source references + updated date
Composer: text + optional attachment/voice
```

Visual traits:

- low density and generous reading width;
- warm neutral surface;
- editorial headline, clear body type;
- one restrained accent;
- source chips and inline navigation;
- prose, steps, callouts, and tables rather than KPI cards.

## 3. Data analyst

Recommended stack:

```text
Header: entity/store/project + period/comparison
Health: freshness + completeness
Priority questions
KPI strip
User question
Executive conclusion
Evidence/chart/table blocks
Driver analysis
Action suggestions
Method/source disclosure
Follow-up chips
Composer
```

Visual traits:

- tabular numerals for KPI and comparison;
- semantic colors only for status or direction;
- charts paired with a textual conclusion;
- dense information grouped into a few strong regions;
- clear distinction between observed data, inferred driver, and recommendation.

Never present a chart without title, unit, period, and plain-language takeaway.

## 4. Workflow copilot

Recommended stack:

```text
Current object and permission
Intent summary
Plan with editable steps
Tool timeline
Result blocks
Operation preview / diff
Impact warning
Confirmation
Execution receipt and audit
```

Visual traits:

- strong stage/status language;
- timeline or stepper;
- monospace only for IDs/code, not whole answers;
- diff colors with icons/text, never color alone;
- primary action labeled with scope and count.

Keep normal chat visually separate from action execution.

## 5. Generative workspace

Recommended stack:

```text
Brief/context controls
Prompt composer
Primary canvas/output
Generation status
Variant rail
Selection-level refinement
Version history
Compare
Export/share
```

Visual traits:

- artifact dominates the viewport;
- prompt controls compact after generation;
- versions and variants stay visible without covering output;
- provide editable intermediate states;
- show generation parameters only when they help refinement.

Do not make chat the main surface when the artifact is the user's real work.

## 6. Embedded assistant

Recommended stack:

```text
Current field/record context
One concise recommendation
Apply/draft/explain
Evidence or rule
Dismiss/return
```

Visual traits:

- inherit host tokens and density;
- minimal header and no duplicate navigation;
- anchor the response to the affected field or record;
- preserve the user's place and unsaved changes.

## 7. Responsive and visual rules

### Layout

- Reading width: usually 640–860 px.
- Analytical width: usually 900–1200 px.
- Keep the composer fixed or sticky without covering the last response.
- On mobile, collapse sidebars into drawers or top context controls.
- Convert KPI rows to 2-column or horizontal scroll.
- Convert wide tables into prioritized columns, cards, or explicit horizontal scroll.

### Type

- Use one display family and one body family at most.
- Use tabular numerals for financial/metric values.
- Keep answer body at comfortable reading size and line height.
- Do not shrink important metadata below legibility to fit card grids.

### Color

- Assign roles: canvas, surface, primary text, secondary text, border, accent, success, warning, danger, info.
- Use the accent for selected/current/primary—not every icon.
- Reserve warning/danger for real risk or failure.
- Test contrast in disabled, hover, focus, chart, and dark-mode states.

### Shape and depth

- Use a small radius scale, for example 8/12/16.
- Prefer border and background changes over stacked shadows.
- Use one elevation for floating composer/panel.
- Keep chat bubble geometry subtle; avoid novelty speech bubbles.

### Motion

- Use motion to explain state changes, streaming, panel transitions, or generated artifacts.
- Respect reduced motion.
- Avoid endless pulsing, decorative sparkles, and fake progress.

