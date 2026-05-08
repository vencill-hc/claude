---
name: parallel-implement
description: >-
  Orchestrate parallel implementation across non-overlapping file groups using
  concurrent agents. Use when an implementation plan touches 4+ files that can be
  split into independent groups, when CLAUDE.md says to parallelize, or when the
  user says "implement in parallel", "parallel agents", or "split this across agents".
---

# Parallel Implement

Orchestrate concurrent implementation of a multi-file plan by partitioning files into non-overlapping groups, launching parallel implementer agents, and auditing cross-file consistency.

## Instructions

Follow these 7 steps in order. Do not skip steps.

### Step 1: Receive Plan

Accept an implementation plan from one of these sources:
- A plan produced in plan mode (read from the plan file)
- A user message describing what to implement
- An argument passed to `/parallel-implement`

The plan MUST specify:
- **Files to create** (with target paths)
- **Files to modify** (with target paths and description of changes)

If no plan is provided or the plan lacks file paths, ask the user:
> "I need an implementation plan that lists specific files to create and modify. Can you provide one, or should I enter plan mode first?"

Do NOT proceed until you have a concrete file list.

### Step 2: Explore Context

Launch 1-2 Explore agents (using `Task` with `subagent_type=Explore`) to gather the full contents of:
- Every file listed in the plan (existing files that will be modified)
- Key dependency files (imports, shared types, config files referenced by planned changes)
- Nearby `__init__.py`, `index.ts`, or barrel files that may need re-exports

Store the complete file contents mentally — each implementer agent will receive relevant contents pasted directly into its prompt. This avoids agents reading overlapping files and causing git state conflicts.

If the plan references 8+ dependency files, launch 2 Explore agents in parallel with non-overlapping file lists.

### Step 3: Partition into Groups

Split the files-to-create and files-to-modify into **N groups** (2-4, never more than 4) following these rules:

1. **No file appears in more than one group.** This is the hard constraint.
2. **Related changes stay together.** A new module and its re-export in `__init__.py` go in the same group. A component and its stylesheet go together.
3. **Each group is self-contained.** An agent can implement its group without seeing real-time output from other agents.
4. **Balance group sizes.** Avoid one group with 8 files and another with 1.

Print the partition table for the user before proceeding:

```
Partition Plan (N groups):

Group 1 — [short label, e.g., "Backend models"]
  CREATE  src/metroline/models/new_model.py
  MODIFY  src/metroline/models/__init__.py

Group 2 — [short label, e.g., "Frontend components"]
  CREATE  web/src/components/NewComponent.tsx
  MODIFY  web/src/App.tsx

Group 3 — [short label]
  ...
```

Wait for the user to confirm or adjust the partition. If the user says nothing (auto-approve), proceed after printing.

### Step 4: Launch Parallel Agents

Launch **all N implementer agents in a single message** (concurrent `Task` tool calls with `subagent_type=implementer`). This is critical — they must be launched in one message to run concurrently.

Each agent's prompt MUST include:

1. **Its subset of the plan.** Only the files and changes assigned to its group.
2. **Complete contents of files it will modify.** Pasted inline so it doesn't need to read them.
3. **Complete contents of files OTHER agents will create/modify** that this agent depends on, prefixed with:
   > "NOTE: The following file will be created/modified by another agent running in parallel. Use these contents as reference but do NOT write or edit this file."
4. **Explicit instructions:**
   - Use `Read` before `Edit` for any file being modified (even though contents are provided, this satisfies the tool requirement).
   - Use `Write` for new files.
   - Use `Edit` for modifications to existing files.
   - Do not modify files outside your assigned group.
   - If you discover a needed change to a file outside your group, note it in your final output but do not make the change.

Example prompt structure for one agent:

```
## Your Task
Implement Group 2 of the parallel implementation plan.

## Files You Own (create or modify these)
- CREATE web/src/components/NewWidget.tsx
- MODIFY web/src/pages/Dashboard.tsx

## Plan Details
[relevant subset of the plan for these files]

## File Contents — Your Files
### web/src/pages/Dashboard.tsx (MODIFY — read before editing)
```tsx
[full file contents]
```

## File Contents — Other Agents' Files (reference only, do NOT edit)
### src/metroline/api/routes/widget.py (being created by Group 1)
```python
[planned contents or skeleton]
```

## Instructions
- Read each file before editing it.
- Use Write for new files, Edit for modifications.
- Do NOT touch files outside your group.
- If you find a needed cross-group change, note it in your output.
```

### Step 5: Collect Results

Wait for all agents to complete. For each agent, record:
- **Status:** succeeded or failed
- **Files touched:** list of files created/modified
- **Cross-group notes:** any issues the agent flagged about files outside its group

If any agent failed, report the failure and ask the user whether to retry that group or proceed with the audit.

### Step 6: Audit Cross-File Consistency

Launch an Explore agent (`subagent_type=Explore`) that reads ALL files created or modified across every group. The audit checks:

1. **Import consistency** — Every `import` / `from X import Y` / `require` / `import {} from` resolves to an existing module and symbol. No dangling references.
2. **Interface contracts** — Function/method signatures match between callers and callees. If Group 1 defined `def process(data: dict)` but Group 2 calls `process(data, strict=True)`, that's a mismatch.
3. **Re-exports** — If a new module was created, its symbols are exported from the package's `__init__.py` or barrel `index.ts` file.
4. **Event/channel/key consistency** — String literals used as event names, channel names, config keys, or dict keys match across files.
5. **No dead code** — No `getattr` for fields that don't exist, no unused imports introduced by the parallel agents.
6. **Type alignment** — If both Python and TypeScript files were modified, Pydantic model fields match TypeScript interfaces (field names, types, optionality).

The audit agent should return a numbered list of issues with severity:

```
Audit Results:
1. [ERROR] src/foo.py:12 imports `bar.Widget` but bar/__init__.py does not export Widget
2. [WARN]  web/src/App.tsx:45 imports unused `OldComponent`
3. [OK]    All event names consistent across 4 files
```

### Step 7: Report

Summarize the implementation:

```
## Parallel Implementation Complete

**Groups:** N agents ran concurrently
**Files created:** X
**Files modified:** Y
**Agent results:** N/N succeeded

### Audit Summary
- Errors: X (must fix)
- Warnings: Y (should fix)
- Checks passed: Z

### Issues Found
1. [ERROR] ... — [suggested fix]
2. [WARN]  ... — [suggested fix]
```

If the audit found errors:
- Offer to fix them: "I found N errors. Want me to fix them now?"
- If the user agrees, fix them directly (these are typically small cross-file fixes, no need for parallel agents).

If the audit is clean:
- Report success and suggest next steps (run tests, build, commit).

## Notes

- **Max 4 parallel agents.** Beyond 4, context sizes grow too large and diminishing returns set in. If the plan has 5+ groups worth of files, merge the smallest groups.
- **Paste file contents, don't rely on file reads.** Agents reading the same files concurrently can cause inconsistencies. Each agent gets its needed file contents directly in its prompt.
- **The partition is the critical step.** A bad partition (overlapping files, split dependencies) causes merge conflicts. Spend time getting it right.
- **Always audit.** Even if every agent succeeds, cross-file consistency is not guaranteed. The audit step catches integration bugs that no single agent can see.
- **This skill complements plan mode.** A typical workflow is: plan mode (design) -> `/parallel-implement` (execute) -> verify (test). This skill handles the middle step.
