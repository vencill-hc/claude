# plan

Create an implementation plan from a Linear ticket by researching codebase patterns

## Arguments
- `$ARGUMENTS` - Linear ticket URL or ID (e.g., `https://linear.app/...` or `SEARCH-1234`)

## What This Does

This command researches your codebase to understand how similar features are built, then creates a detailed implementation plan that references specific example files to follow.

**The key innovation:** Instead of guessing at patterns, this command actively searches and reads your codebase to find real examples, then includes those file paths in the plan so implementation can follow proven patterns.

## Steps I Will Take

### 1. Fetch the Linear Ticket
- Use Linear MCP to get ticket details
- Extract requirements, description, and acceptance criteria
- Understand what needs to be built

### 2. Identify Feature Type
Determine what kind of work this is:
- UI component or page?
- Backend service or API?
- Background job or integration?
- Database migration or model change?
- Full-stack feature with multiple layers?

### 3. Research Phase (The Critical Part)

For each layer of the feature, I will:

**Search for similar features:**
- Use Glob to find files with similar names
- Use Grep to find similar patterns (class names, method signatures)
- Check relevant directories (components, services, jobs, etc.)

**Read the best examples:**
- Pick 2-3 files that demonstrate the pattern
- Read them fully to understand structure and conventions
- Note specific techniques (N+1 prevention, Turbo integration, etc.)

**Document for reference:**
- List file paths to reference during implementation
- Note key patterns and conventions observed
- Identify reusable components or base classes
- Flag any gotchas or special considerations

### 4. Create the Plan

Output a structured plan with:

**Pattern Research Summary:**
- Files to reference (with full paths)
- Key patterns observed
- Reusable components identified
- Special conventions to follow

**Implementation Steps:**
- Ordered steps for implementation
- Which pattern file(s) to reference for each step
- Testing approach matching existing patterns
- Estimated size (aiming for 200-500 lines)

**Dependencies & Considerations:**
- Database changes needed
- Packwerk boundary implications
- External API integrations
- Performance considerations

### 5. Exit Plan Mode
- Present the plan for your approval
- Wait for confirmation before implementing

## Example Research Output

When researching a filter UI feature, I might output:

```markdown
## Pattern Research

### Similar Features Found:

1. **app/components/contacts/filter_menu_component.rb** ⭐ Best match
   - Complete filter UI with multi-select
   - Uses Turbo Frames for dynamic updates
   - Stimulus controller for dropdown interactions
   - DaisyUI components for styling

2. **app/services/people/search_service.rb** ⭐ Service layer pattern
   - Cursor pagination implementation
   - N+1 prevention with .includes()
   - Filter parameter handling

3. **app/controllers/contacts/filter_options_controller.rb**
   - Shows controller pattern for filter endpoints
   - Turbo Stream responses

4. **test/components/contacts/filter_menu_component_test.rb**
   - Test pattern for components with interactions
   - How to test Turbo streams

### Key Conventions Observed:
- Components namespaced: `[Domain]::[Name]Component`
- Services use cursor pagination via `CursorPagination` concern
- Controllers delegate to service objects
- Tests mirror implementation directory structure

### Reusable:
- `CursorPagination` concern (app/services/concerns/cursor_pagination.rb)
- `ModalComponent` for overlay UI
- `MenuController` stimulus controller pattern

## Implementation Plan

**Step 1: Create Filter Component**
- Follow: contacts/filter_menu_component.rb
- Create: `app/components/projects/filter_menu_component.rb`
- Add Stimulus controller following menu_controller.js pattern

**Step 2: Build Service Layer**
- Follow: people/search_service.rb
- Create: `app/services/projects/filter_service.rb`
- Include CursorPagination concern
- Use .includes() to prevent N+1

**Step 3: Add Controller Endpoint**
- Follow: contacts/filter_options_controller.rb
- Create: `app/controllers/projects/filter_options_controller.rb`
- Return Turbo Stream responses

**Step 4: Tests**
- Follow: test/components/contacts/filter_menu_component_test.rb
- Add component tests
- Add service tests
- Add controller integration tests

**Estimated Size:** ~350 lines
```

## Usage Examples

```bash
# With Linear URL
/plan https://linear.app/huntclub/issue/SEARCH-1234/add-candidate-filtering

# With ticket ID only
/plan SEARCH-1234

# I'll fetch the ticket, research the codebase, and create a detailed plan
```

## Why This Works

**Before:** You implement based on general knowledge, maybe miss patterns, code feels inconsistent

**After:** You implement following specific examples from the codebase, code feels cohesive and follows established conventions

The research phase is what makes this powerful. By loading real examples into the plan, implementation becomes pattern-following instead of pattern-guessing.

## Important Notes

- I stay in **read-only mode** during planning
- I do NOT make any code changes or commits
- I exit plan mode and wait for your approval
- You can ask me to adjust the plan before implementing
- The file paths in the plan become your implementation guide
