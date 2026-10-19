# build

Automatically plan and implement a feature from a Linear ticket using background agents

## Arguments
- `$ARGUMENTS` - Linear ticket URL or ID (e.g., `https://linear.app/...` or `SEARCH-1234`)

## What This Does

Combines `/plan` and `/implement` into a single automated workflow by running both as background agents. This lets you kick off a feature implementation and let it run autonomously.

## Steps I Will Take

### 1. Create Git Worktree
- Extract Linear ticket ID from `$ARGUMENTS` (e.g., SEARCH-1234)
- Create a new git worktree at `../artemis-{TICKET_ID}` with branch `tim/{TICKET_ID}` based on main
- Copy `.env.development` and `.env.development.local` from `~/dev/artemis` to the new worktree
- Change to the new worktree directory

### 2. Launch Planning Agent
- Start a background agent to execute the `/plan` command
- The agent will:
  - Fetch the Linear ticket details
  - Research codebase patterns
  - Identify example files to follow
  - Create a detailed implementation plan
- Wait for the planning agent to complete
- Report the plan summary

### 3. Launch Implementation Agent
- Start a background agent to execute the `/implement` command
- The agent will:
  - Follow the plan created in step 1
  - Read pattern files identified during planning
  - Implement the feature following established patterns
  - Write tests matching existing test patterns
  - Verify all tests pass
- Wait for the implementation agent to complete
- Report the implementation summary

### 4. Final Report
Provide a comprehensive summary:
- **Plan created:** Files to reference, key patterns, implementation steps
- **Implementation completed:** Files created/modified, tests added, results
- **Ready for:** `/ship` to review and create PR

## Usage Examples

```bash
# With Linear URL
/build https://linear.app/huntclub/issue/SEARCH-1234/add-candidate-filtering

# With ticket ID only
/build SEARCH-1234
```

## What Makes This Powerful

**Single command workflow:**
- Traditional: `/plan SEARCH-1234` → review → `/implement` → `/ship`
- Automated: `/build SEARCH-1234` → `/ship`

**Background execution:**
- Both agents run autonomously without manual intervention
- You get back control immediately
- Progress is reported as agents complete

**Pattern-following implementation:**
- Planning agent researches real examples from your codebase
- Implementation agent follows those proven patterns
- Results in consistent, maintainable code

## Example Output

```markdown
🚀 Starting automated implementation for SEARCH-1234

## Phase 1: Setup Worktree
Creating new git worktree at ../artemis-SEARCH-1234 with branch tim/SEARCH-1234...
Copying environment files from ~/dev/artemis...

✅ Worktree Ready!
- Branch: tim/SEARCH-1234
- Path: /Users/tim/dev/artemis-SEARCH-1234
- Environment files copied

---

## Phase 2: Planning
Launching planning agent to research codebase patterns...

✅ Planning Complete!

**Pattern Research Summary:**
- Found 3 similar features to reference
- Key files: app/components/contacts/filter_menu_component.rb
- Patterns: Turbo Frames, Stimulus controllers, Service layer with cursor pagination
- Estimated size: ~350 lines

**Implementation Steps:**
1. Create FilterComponent (follow contacts/filter_menu_component.rb)
2. Build service layer (follow people/search_service.rb)
3. Add controller endpoint (follow contacts/filter_options_controller.rb)
4. Write tests matching existing patterns

---

## Phase 3: Implementation
Launching implementation agent to build the feature...

✅ Implementation Complete!

**Files Created:**
- app/components/projects/filter_menu_component.rb
- app/components/projects/filter_menu_component.html.erb
- app/javascript/controllers/project_filter_controller.js
- app/services/projects/filter_service.rb
- app/controllers/projects/filter_options_controller.rb
- 3 test files

**Results:**
- Total: ~380 lines
- All tests passing ✓
- Follows codebase patterns ✓

---

## ✨ Ready for Review

Run `/ship` to review changes and create the pull request.
```

## Important Notes

- Both agents run autonomously without requiring approval between steps
- The implementation agent automatically proceeds with the plan from the first agent
- If either agent encounters an error, it will be reported
- You can still review the work with `/ship` before creating the PR
- This is best for straightforward features; complex features may benefit from manual review between planning and implementation

## When to Use

**Good for:**
- Standard CRUD features following existing patterns
- UI components similar to existing ones
- Service integrations matching established patterns
- Database changes with clear requirements

**Maybe skip for:**
- Architectural changes affecting multiple systems
- Features requiring design decisions
- Complex refactorings
- Anything where you want to review the plan first

## The Full Workflow

1. `/build SEARCH-1234` - Automatically plan and implement
2. `/ship` - Review, fix issues, create PR
3. Done! ✨

## Error Handling

If the planning agent fails:
- Error details will be reported
- Implementation agent will not be launched
- You can run `/plan SEARCH-1234` manually to debug

If the implementation agent fails:
- Plan will already be available in conversation history
- Error details will be reported
- You can run `/implement` manually to retry
