---
name: ai-interface-design
description: Design, review, or implement AI product features and interfaces across web, mobile, desktop, and embedded panels. Use for AI assistants, chat panels, copilots, agents, knowledge/RAG experiences, data-analysis AI, generative workspaces, AI onboarding, prompt/input design, response modules, streaming/tool states, explainability, confirmation flows, AI design systems, AI UI/UX audits, wireframes, prototypes, and production UI implementation. Trigger for requests involving AI 功能设计, AI 面板, AI 助手, AI 对话, AI UI/UX, AI 样式, AI 工作台, copilot, agent interface, RAG UI, AI analytics, or improving an existing AI experience.
---

# AI Interface Design

Design the AI's product behavior and interface as one system. Do not decorate a generic chat box before defining what the AI is responsible for.

## Core workflow

1. Inspect the target product, platform, users, current design system, AI/data capabilities, permissions, and write risks.
2. Classify the primary AI surface:
   - **Knowledge guide**: explanation, RAG, SOP, support, onboarding.
   - **Data analyst**: metrics, comparisons, evidence, diagnosis, recommendations.
   - **Workflow copilot**: task completion, tool calls, previews, approvals, audit.
   - **Generative workspace**: create, refine, compare, version, export.
   - **Embedded assistant**: contextual help inside a focused business screen.
3. Define the functional contract before styling:
   - user job and success condition;
   - scope and explicit non-capabilities;
   - context inputs and retention;
   - output block types;
   - read/write permissions and confirmation;
   - loading, streaming, tool, success, partial, empty, refusal, and error states;
   - evidence, freshness, confidence, and recovery.
4. Design the end-to-end flow: entry → prompt/context → progress → answer/action → verification → follow-up.
5. Select modules and a visual direction that fit the AI surface and host product.
6. Produce the requested artifact: feature spec, flow, wireframe, visual system, prototype, code, or audit.
7. Validate responsive behavior, keyboard access, long content, state coverage, trust cues, and risk boundaries.

Make reasonable assumptions when context is missing and label them. Ask only when a missing decision would materially change scope or safety.

## Required output

For a new AI feature or substantial redesign, include:

1. **AI Product Contract** — user job, AI role, boundaries, inputs, outputs, and success measures.
2. **Interaction Flow** — happy path plus partial, error, refusal, and retry paths.
3. **Module Architecture** — ordered screen/panel modules and conditional visibility.
4. **State Model** — at minimum `idle`, `composing`, `thinking`, `streaming`, `tool-running`, `done`, `partial`, `error`, `cancelled`.
5. **Trust and Control** — context, source/freshness, confidence, preview/confirmation, and undo or recovery.
6. **Visual System** — hierarchy, color roles, typography, spacing, shape, motion, and responsive rules.
7. **Acceptance Checklist** — concrete UX and functional checks.

If the user requests implementation, create a runnable result and verify it at representative desktop and mobile sizes. If the request is review-only, do not modify product files.

## Routing references

Read only the references needed for the chosen surface:

- Read [references/product-function.md](references/product-function.md) for feature architecture, context, tools, permissions, state machines, metrics, and AI safety.
- Read [references/ui-patterns.md](references/ui-patterns.md) for module stacks, visual directions, responsive behavior, and AI-specific component patterns.
- Read [references/response-contracts.md](references/response-contracts.md) when designing APIs, typed response blocks, frontend renderers, operation previews, or generative outputs.
- Read [references/quality-gates.md](references/quality-gates.md) before finalizing a spec, prototype, implementation, or audit.

Use [assets/ai-panel-starter.html](assets/ai-panel-starter.html) as a no-dependency starting point only when a generic web prototype helps. Adapt its structure and tokens to the host product; do not treat its green/gold palette as mandatory.

## Non-negotiable design rules

- Show meaningful progress; never use a typing animation as the only status for a long tool run.
- Preserve the user's input during errors and provide a specific recovery action.
- Keep scope, entity, tenant, file, store, date, or other consequential context visible near the input or answer.
- Put the direct answer first. Move methodology, raw traces, SQL, and debug detail behind progressive disclosure.
- Distinguish facts, inference, recommendation, simulation, and unavailable data visually and semantically.
- Never fabricate sources, confidence, live status, completion, tool execution, or data freshness.
- Render structured content as typed modules; do not force KPI, charts, diffs, citations, and approvals into one Markdown blob.
- Separate read answers from write actions. A write requires a dedicated preview with target, impact, before/after values, permission, confirmation, execution result, and recovery.
- Make cancellation real. If work cannot be cancelled, say so before it starts.
- Do not expose chain-of-thought. Show concise rationale, evidence, assumptions, tool progress, and decision-relevant traces.
- Avoid placeholder-heavy dashboards, excessive card grids, neon gradients, generic robot imagery, and ornamental "AI sparkles" without meaning.
- Respect the host design system unless the user explicitly asks for a standalone visual language.

## Surface-specific answer order

- **Knowledge guide**: direct answer → steps/explanation → where to act → sources → related questions.
- **Data analyst**: conclusion → KPI/evidence → drivers → recommendations → method/source → follow-up.
- **Workflow copilot**: understood intent → plan → tool progress → preview/diff → confirmation → result/audit.
- **Generative workspace**: brief/context → generation progress → primary output → variants → refine/version → export.
- **Embedded assistant**: current context → concise answer/action → affected field/record → return to task.

## Visual direction selection

Choose one direction deliberately:

- **Calm editorial** for knowledge and support: warm paper, restrained accent, readable prose, source-led answers.
- **Analytical editorial** for business/data: dense but calm hierarchy, tabular numerals, evidence cards, limited semantic color.
- **Operational command** for tool-using copilots: explicit stages, strong state feedback, diffs, approvals, audit trail.
- **Creative canvas** for generation: large artifact area, compact prompt controls, version rail, comparison and export.
- **Host-native embedded** for contextual help: inherit product tokens and minimize chrome.

State why the direction matches the user's job. Avoid mixing all directions in one surface.

## Implementation discipline

- Inspect existing components and tokens before introducing new primitives.
- Keep state, content contracts, and rendering components separate.
- Use semantic HTML and keyboard-operable controls.
- Use token variables instead of scattered literal values.
- Prefer CSS/SVG for simple decorative visuals; use real charts for analytical data.
- Test short/long prompts, long answers, zero data, partial data, source loss, disconnect, retry, cancellation, and permission denial.
- For streaming, append safely, maintain scroll control, allow selection/copy, and do not steal focus.
- For mobile, keep context legible, composer reachable, and tables/charts convertible to stacked or scrollable forms.

