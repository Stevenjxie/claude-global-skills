# AI product and functional design

## Contents

1. Product contract
2. Context model
3. State machine
4. Tool and write flows
5. Trust and explainability
6. Success measures

## 1. Product contract

Define these before screen layout:

| Field | Required decision |
|---|---|
| User | Primary role, expertise, frequency, pressure |
| Job | Concrete task the user is trying to finish |
| AI role | Guide, analyst, copilot, creator, reviewer, router |
| Inputs | Text, voice, files, selection, current record, history |
| Outputs | Answer, chart, table, plan, artifact, proposal, action |
| Boundary | What the AI cannot know or must not do |
| Authority | Read, draft, preview, execute, approve |
| Success | Time saved, completion, accuracy, adoption, correction rate |

Write one sentence:

> For [user], the AI helps [job] by [capability], while never [boundary].

If this sentence contains several unrelated jobs, split the surface or introduce explicit modes.

## 2. Context model

Context must be:

- **visible** when it changes meaning;
- **editable** when the user can correct it;
- **scoped** to the current tenant/project/store/file/entity;
- **freshness-aware** for changing data;
- **bounded** for history and token use;
- **removable** for privacy.

Use compact context chips or a context bar for consequential scope. Examples:

- project, workspace, file, selection;
- factory, store, department, customer;
- date range and comparison range;
- currency, timezone, unit;
- data source and last refresh;
- model or generation mode only when user choice matters.

Do not hide high-impact context in placeholder text.

## 3. State machine

Use an explicit state model:

```text
idle → composing → submitted
submitted → thinking → streaming → done
thinking → tool-running → streaming/done
thinking/streaming/tool-running → cancelled
thinking/streaming/tool-running → partial/error
partial/error → retrying → thinking
done → follow-up or action-preview
action-preview → confirmed → executing → succeeded/failed
```

Required behavior:

- `thinking`: acknowledge the task and show cancellable progress if it may exceed two seconds.
- `streaming`: keep stable layout; do not repeatedly scroll away from user selection.
- `tool-running`: name the meaningful stage, not internal implementation jargon.
- `partial`: preserve usable results and name what is missing.
- `error`: preserve prompt/context, explain impact, and offer retry/edit/fallback.
- `cancelled`: clarify whether any side effect occurred.

For multi-step work, show 3–7 meaningful stages. Avoid fake exact percentages unless the backend supplies real progress.

## 4. Tool and write flows

Classify every tool:

- read-only query;
- reversible draft/change;
- irreversible or externally visible action;
- privileged/security-sensitive action.

For a write or external action, show:

1. understood intent;
2. exact target and scope;
3. proposed changes;
4. before/after values or generated payload;
5. impact and dependencies;
6. permission/approval status;
7. explicit confirmation;
8. execution progress;
9. result IDs/counts and post-action state;
10. undo, rollback, or recovery where possible.

Never use a vague `Confirm` button for a high-impact action. Label the actual action, such as `Send 24 emails` or `Update this store only`.

## 5. Trust and explainability

Show decision-relevant evidence:

- sources or datasets;
- entity and time range;
- calculation definition;
- data freshness and completeness;
- important assumptions;
- fact versus inference;
- limitations and missing inputs.

Avoid false precision. Confidence must have a defined meaning. If there is no calibrated confidence value, use qualitative status such as `data complete`, `partial evidence`, or `needs verification`.

Do not reveal hidden reasoning. Provide a short rationale:

> Conclusion + 2–4 strongest signals + assumptions + what would change the conclusion.

## 6. Success measures

Choose measures by surface:

- Knowledge guide: answer resolution, source opens, escalation, correction, time-to-answer.
- Data analyst: decision time, verified insight rate, follow-up depth, export/use, numerical correctness.
- Workflow copilot: successful completion, correction before execution, approval time, rollback rate, prevented unsafe actions.
- Generative workspace: usable first draft, edit distance, variant comparison, export, regeneration rate.
- Embedded assistant: task completion, field correction, abandoned flow, context mismatch.

Do not use message count or token consumption as primary UX success metrics.

