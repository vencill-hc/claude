---
description: Perform a "look back and look forward" gap analysis on recent work. Identifies patterns that should become skills, analyzes remaining work, and automatically generates new skills for future sessions.
---

# Kung Fu: Gap Analysis & Skill Development

Perform retrospective analysis of recent development work, identify repeating patterns, analyze remaining work, and generate new skills to capture institutional knowledge.

## Overview

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│   LOOK BACK     │────▶│    GAP ANALYSIS      │────▶│   LOOK FORWARD      │
│                 │     │                      │     │                     │
│ • Recent commits│     │ • Pattern detection  │     │ • Remaining work    │
│ • Session work  │     │ • Error patterns     │     │ • Skill requirements│
│ • Lessons learned│    │ • Skill gaps         │     │ • Skill generation  │
└─────────────────┘     └──────────────────────┘     └─────────────────────┘
```

## Phase 1: Look Back - Analyze Recent Work

### 1.1 Gather Context

Review the following sources to understand recent work:

1. **Git History:**
   ```bash
   git log --oneline -20
   git diff HEAD~5..HEAD --stat
   ```

2. **Session Documentation:**
   - Check for `_*` directories (e.g., `_NetSuite-Integration/`)
   - Read `SESSION-SUMMARY.md` if present
   - Read `ACTIVE-LEARNING-JOURNAL.md` if present

3. **Todo List History:**
   - Review completed tasks in current session
   - Note any patterns in task types

4. **Build/Error History:**
   - Note common error patterns encountered
   - Document fixes applied

### 1.2 Pattern Detection Questions

For each significant piece of work, ask:

| Question | If Yes → |
|----------|----------|
| Did I create similar code structures 2+ times? | **Pattern for generator skill** |
| Did I encounter Entity4-specific errors repeatedly? | **Pattern for fixer/guide skill** |
| Did I need to research the same thing twice? | **Pattern for reference skill** |
| Did I follow a multi-step workflow? | **Pattern for workflow skill** |
| Did I use domain-specific knowledge? | **Pattern for domain skill** |

### 1.3 Work Distribution Analysis

Calculate and document:

```
Main Context Work:
- [ ] File edits (count)
- [ ] Error fixes (count)
- [ ] Research/exploration (time estimate)

Agent/Skill Work:
- [ ] Tasks delegated to agents
- [ ] Skills invoked
- [ ] Agent success rate

Efficiency Metrics:
- Context usage: [High/Medium/Low]
- Could more work have been delegated? [Yes/No]
- What blocked delegation?
```

## Phase 2: Gap Analysis - Identify Missing Skills

### 2.1 Skill Gap Categories

| Category | Indicators | Skill Type |
|----------|------------|------------|
| **Code Generation** | Created similar files 2+ times | `*-generator` |
| **Error Patterns** | Fixed same type of error multiple times | `*-fixer` or `*-patterns` |
| **Workflow** | Followed same steps repeatedly | `*-workflow` |
| **Integration** | Connected to external system | `*-integration` |
| **Frontend UI** | Built similar components | `*-fe` |
| **Testing** | Wrote similar tests | `*-testing` |

### 2.2 Gap Identification Template

For each identified gap:

```markdown
## Gap: [Name]

**Evidence:**
- [What work triggered this need?]
- [How many times did this pattern appear?]

**Current Approach:**
- [How was this handled manually?]

**Proposed Skill:**
- Name: `[skill-name]`
- Type: [generator/fixer/workflow/reference]
- Trigger: [When should this skill be used?]
- Output: [What does the skill produce?]

**Value Assessment:**
- Time saved per use: [estimate]
- Frequency of use: [high/medium/low]
- Priority: [1=critical, 2=high, 3=medium, 4=low]
```

## Phase 3: Look Forward - Analyze Remaining Work

### 3.1 Identify Remaining Work

Review project documentation for upcoming work:

1. **Project Plans:**
   - Implementation guides
   - Epic/story descriptions
   - Architecture documents

2. **Work Breakdown:**
   - List remaining tasks/features
   - Categorize by type (backend, frontend, integration, tests)
   - Note dependencies

### 3.2 Predict Future Skill Needs

For each remaining work item:

| Work Item | Agent-Suitable? | Required Skills | Gap? |
|-----------|-----------------|-----------------|------|
| [Item 1]  | [Yes/No/Partial]| [List skills]   | [Y/N]|
| [Item 2]  | [Yes/No/Partial]| [List skills]   | [Y/N]|

### 3.3 Prioritization Matrix

```
                    HIGH FREQUENCY
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         │   AUTOMATE    │   MUST HAVE   │
         │   LATER       │   SKILL       │
  LOW    │               │               │   HIGH
  VALUE  ├───────────────┼───────────────┤   VALUE
         │               │               │
         │   SKIP        │   NICE TO     │
         │               │   HAVE        │
         │               │               │
         └───────────────┼───────────────┘
                         │
                    LOW FREQUENCY
```

## Phase 4: Skill Generation

### 4.1 Skill Creation Checklist

For each skill to create:

- [ ] Create directory: `.claude/skills/[skill-name]/`
- [ ] Create `SKILL.md` with frontmatter
- [ ] Include practical examples from actual work
- [ ] Document common mistakes and fixes
- [ ] Add templates where applicable
- [ ] Test by invoking skill

### 4.2 Skill Template Structure

```markdown
---
name: [skill-name]
description: [One-line description for skill list. Include trigger phrases.]
---

# [Skill Title]

[When to use this skill - 2-3 sentences]

## [Section 1: Core Concept]
[Explanation with code examples]

## [Section 2: Templates]
[Copy-paste ready templates]

## [Section 3: Common Mistakes]
[What goes wrong and how to fix]

## [Section 4: Quick Reference]
[Table or checklist for fast lookup]
```

### 4.3 Validation

After creating skills:

1. Verify skill appears in `/skills` list
2. Test skill invocation
3. Confirm examples are accurate
4. Check for Entity4-specific patterns

## Phase 5: Output Summary

Generate a summary report:

```markdown
# Kung Fu Analysis Report

**Date:** [date]
**Session/Epic:** [name]
**Analyst:** Claude

## Look Back Summary
- Commits analyzed: [N]
- Main patterns identified: [N]
- Error patterns found: [N]

## Skills Created
| Skill | Type | Priority | Value |
|-------|------|----------|-------|
| [name] | [type] | [1-4] | [desc] |

## Remaining Work Analysis
- Total items: [N]
- Agent-suitable: [N] ([%])
- Skills needed: [N]
- Gaps identified: [N]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Next Session Prep
- [ ] Review new skills
- [ ] Update SESSION-SUMMARY.md
- [ ] [Other prep items]
```

## Execution Notes

- Run this analysis at natural breakpoints (end of day, end of feature, end of epic)
- Focus on patterns that appeared 2+ times
- Prioritize skills that will be used in upcoming work
- Keep skills focused and single-purpose
- Update existing skills rather than creating duplicates
