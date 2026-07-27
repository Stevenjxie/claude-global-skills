# AI interface quality gates

Run the relevant gates before handoff.

## Product and function

- [ ] The primary user and job are explicit.
- [ ] The AI role and non-capabilities are visible.
- [ ] Consequential context is visible and correctable.
- [ ] The surface is not overloaded with unrelated AI jobs.
- [ ] Output modules map to real backend/data capabilities.
- [ ] Empty, partial, refusal, permission, error, retry, cancel, and success paths exist.
- [ ] Success measures reflect task outcomes, not message volume.

## Trust and safety

- [ ] Facts, inferences, recommendations, and simulations are distinguishable.
- [ ] Sources, period, scope, freshness, and missing data appear where relevant.
- [ ] Confidence has a defined meaning or is omitted.
- [ ] No fake data, source, progress, completion, or tool execution is shown.
- [ ] Read and write behavior are separate.
- [ ] Writes show exact target, impact, before/after, confirmation, result, and recovery.
- [ ] Destructive or external actions cannot be triggered by an ambiguous button.
- [ ] Hidden chain-of-thought is not exposed.

## Interaction

- [ ] Starter prompts are representative and actually supported.
- [ ] The direct answer appears before methodology.
- [ ] Long-running work shows meaningful stages and supports cancellation when possible.
- [ ] User input and context survive failure.
- [ ] Follow-ups preserve only valid context and allow correction.
- [ ] Streaming does not steal focus or prevent copy/selection.
- [ ] The composer never covers the last response.

## Visual and content

- [ ] Hierarchy works without relying on color alone.
- [ ] Semantic colors are reserved for status/direction.
- [ ] Typography, spacing, radius, and elevation use tokens.
- [ ] Cards group meaning; they are not used for every sentence.
- [ ] Long prose, tables, charts, code, citations, and operation previews are readable.
- [ ] Loading skeletons resemble the eventual content.
- [ ] AI decoration does not overpower task content.

## Accessibility

- [ ] Keyboard navigation and visible focus work.
- [ ] Controls have names, not icon-only ambiguity.
- [ ] Live updates use appropriate announcements without excessive interruption.
- [ ] Charts have a takeaway and accessible data fallback.
- [ ] Contrast meets the target standard.
- [ ] Reduced motion is respected.
- [ ] Zoom and text enlargement do not hide context or actions.

## Responsive

Verify at minimum:

- [ ] 360–390 px mobile;
- [ ] 768 px tablet or narrow desktop;
- [ ] 1280–1440 px desktop;
- [ ] long localized labels and Chinese/English mixed text;
- [ ] software keyboard and safe-area behavior where relevant.

## Evidence

For implementation, report separately:

- static/type/lint status;
- interaction/component tests;
- visual screenshots at tested sizes;
- API/tool-state evidence;
- write counts or side effects;
- known gaps and untested states.

