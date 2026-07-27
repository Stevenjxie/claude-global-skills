# Typed AI response contracts

Use typed blocks when the interface renders more than plain prose.

## Envelope

```ts
type AiResponse = {
  id: string
  status: 'streaming' | 'done' | 'partial' | 'error'
  context: AiContextSnapshot
  summary?: string
  blocks: AiBlock[]
  suggestions?: FollowUp[]
  provenance?: Provenance
  error?: RecoverableError
}

type AiContextSnapshot = {
  scopeType: string
  scopeId: string
  scopeLabel: string
  period?: { start: string; end: string; comparisonStart?: string; comparisonEnd?: string }
  updatedAt?: string
}
```

## Block union

```ts
type AiBlock =
  | MarkdownBlock
  | StepsBlock
  | KpiBlock
  | ChartBlock
  | TableBlock
  | EvidenceBlock
  | RecommendationBlock
  | SourceBlock
  | ProgressBlock
  | OperationPreviewBlock
  | ArtifactBlock
```

Every block needs a stable ID. Add optional status and error at block level when partial rendering is supported.

### Knowledge blocks

```ts
type MarkdownBlock = {
  id: string
  type: 'markdown'
  content: string
}

type StepsBlock = {
  id: string
  type: 'steps'
  title?: string
  items: { title: string; detail?: string; href?: string }[]
}
```

### Analytical blocks

```ts
type KpiBlock = {
  id: string
  type: 'kpi'
  items: {
    label: string
    value: number | string
    unit?: string
    comparison?: { value: number; direction: 'up' | 'down' | 'flat'; label: string }
    status?: 'good' | 'warning' | 'bad' | 'neutral'
  }[]
}

type ChartBlock = {
  id: string
  type: 'chart'
  title: string
  takeaway: string
  unit?: string
  period?: string
  spec: unknown
  accessibleTable?: { columns: string[]; rows: unknown[][] }
}

type EvidenceBlock = {
  id: string
  type: 'evidence'
  claim: string
  signals: { label: string; value: string; sourceIds: string[] }[]
  kind: 'observed' | 'inferred' | 'simulated'
}
```

### Recommendation and source blocks

```ts
type RecommendationBlock = {
  id: string
  type: 'recommendations'
  items: {
    title: string
    rationale: string
    impact?: 'high' | 'medium' | 'low'
    effort?: 'high' | 'medium' | 'low'
    owner?: string
  }[]
}

type SourceBlock = {
  id: string
  type: 'sources'
  items: {
    sourceId: string
    label: string
    href?: string
    updatedAt?: string
    excerpt?: string
  }[]
}
```

### Operation preview

```ts
type OperationPreviewBlock = {
  id: string
  type: 'operation-preview'
  operation: string
  target: { type: string; id: string; label: string }
  scopeLabel: string
  changes: { field: string; before: unknown; after: unknown }[]
  impact: string[]
  risk: 'low' | 'medium' | 'high'
  expiresAt?: string
  confirmation: {
    required: true
    buttonLabel: string
    permission: string
  }
}
```

Do not let Markdown imitate an operation preview. The client must know that confirmation is required and bind the button to an idempotent, authorized operation.

## Streaming events

Prefer typed events:

```ts
type AiStreamEvent =
  | { type: 'status'; stage: string; cancellable: boolean }
  | { type: 'block-start'; block: Pick<AiBlock, 'id' | 'type'> }
  | { type: 'block-delta'; blockId: string; delta: unknown }
  | { type: 'block-done'; blockId: string }
  | { type: 'tool-status'; toolCallId: string; label: string; state: 'running' | 'done' | 'failed' }
  | { type: 'response-done'; response: AiResponse }
  | { type: 'error'; error: RecoverableError }
```

Define one preparation and permission path for streaming and non-streaming responses so they cannot drift.

