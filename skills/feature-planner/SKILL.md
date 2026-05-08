---
name: feature-planner
description: Plan new features by fetching Linear tickets, researching codebase patterns, and creating implementation plans broken into small PRs. Use when user says "plan this feature", "create a plan", or asks to implement something that needs planning first.
---

# Feature Planner

Plan new features systematically by understanding requirements, researching existing patterns, and breaking work into manageable PRs.

## Instructions

### 1. Gather Requirements
- If user provides a Linear ticket ID (e.g., "SEARCH-1234"), fetch it using `mcp__linear__get_issue`
- If user provides a description, work from that
- Clarify any ambiguous requirements with the user

### 2. Research Existing Patterns
Search the codebase to understand how similar features work:
- Use Grep to find similar models, controllers, or components
- Read example files to understand established patterns
- Identify reusable components or services
- Note any architectural constraints (e.g., Packwerk boundaries)
- Check domain-specific CLAUDE.md files

### 3. Identify Files to Modify
Create a comprehensive list of files that will need changes:
- **Models**: New models or modifications to existing ones
- **Controllers**: New actions or controllers needed
- **Views/Components**: ViewComponents (namespaced properly)
- **Services**: Background jobs, API integrations, service objects
- **Tests**: Test files for each new/modified file (Minitest::Spec format)
- **Migrations**: Database schema changes
- **Routes**: New routes or modifications

### 4. Break Into Small PRs
If the feature is large (>500 lines of changes):
- Split into logical, independently reviewable PRs
- Each PR should be 200-500 lines ideally
- Ensure each PR is functional on its own
- Order PRs by dependencies (foundation first)

Example breakdown:
- PR 1: Database schema and models (200 lines)
- PR 2: Core business logic and services (300 lines)
- PR 3: Controllers and API endpoints (250 lines)
- PR 4: UI components and views (400 lines)

### 5. Create Implementation Checklist
Generate a detailed checklist with:
- Specific tasks in implementation order
- File paths to create or modify
- Pattern files to reference
- Dependencies between tasks
- Testing requirements

### 6. Present the Plan
Format the plan clearly:

```markdown
## Feature: [Name]
[Brief description from Linear or user]

## Research Findings
- [Pattern 1]: Found in [file_path:line]
- [Pattern 2]: [component] handles similar functionality
- [Reusable code]: Can leverage [existing service/component]

## Files to Modify
**Models**
- [ ] app/models/new_model.rb (create)
- [ ] app/models/existing_model.rb (modify - add association)

**Controllers**
- [ ] app/controllers/new_controller.rb (create)

**ViewComponents** (remember to namespace)
- [ ] app/components/domain/new_component.rb (create)

**Services**
- [ ] app/services/domain/new_service.rb (create)

**Tests** (Minitest::Spec format)
- [ ] test/models/new_model_test.rb (create)
- [ ] test/controllers/new_controller_test.rb (create)

[... continue for all file types ...]

## PR Breakdown
**PR 1: Database and Models** (~200 lines)
- Migration for new tables
- Model definitions
- Basic validations and associations
- Tests

**PR 2: Business Logic** (~300 lines)
[... continue ...]

## Implementation Checklist
1. [ ] Create migration for `new_table`
2. [ ] Add `NewModel` with validations
3. [ ] Add association to `ExistingModel`
4. [ ] Write model tests
[... continue with all tasks ...]

## Notes
- [Any important considerations]
- [Potential gotchas from .claude/GOTCHAS.md]
- [Security considerations]
```

## Artemis-Specific Considerations

### Bucket/Recording/Recordable Pattern
If working with projects, playbooks, groups, or contact lists:
- Bucket is the container
- Recording wraps content with status, position, parent/child
- Recordable is the actual content
- Always use `bucket.record()` to create
- Query through `bucket.recordings`

### Person/Contact/User Pattern
If working with users and contacts:
- Users have TWO Person records
- Use `user.contact.person` for networking
- Never use User persons for connections

### ViewComponents
- Always namespace (e.g., `StageComponents::`)
- Use `render?` method, not template conditionals
- Check existing components in same domain

### Services
- Use CursorPagination concern for paginated results
- Use `.includes()` to prevent N+1 queries
- Cache AI responses with pattern: `ai_response:model:#{model}:prompt_hash:#{hash}`

### Background Jobs
- Use `:default` queue
- Add delays for rate limiting
- Use parent/worker pattern for batch processing

## Notes

- Always search for existing functionality before planning new code
- Consider the "simplest solution" philosophy
- Include test files in every plan
- Reference specific file paths from research findings
- Account for Rails conventions and project architecture
- Don't over-engineer - start simple, add complexity only when needed
- Prefer Turbo/Hotwire patterns over custom JS
