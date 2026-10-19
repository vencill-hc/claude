# implement

Execute the approved implementation plan

## What This Does

Implements the feature by following the plan you approved, referencing the specific example files that were identified during planning.

## Steps I Will Take

### 1. Review the Plan
- Re-read the implementation plan from the conversation history
- Note the pattern files to reference
- Understand the sequence of steps
- Identify any dependencies between steps

### 2. For Each Implementation Step

**Read Pattern Files:**
- Open the example files specified in the plan
- Review their structure, naming, and conventions
- Understand the patterns to follow

**Implement Following the Pattern:**
- Create new files matching the pattern structure
- Use similar naming conventions
- Follow the same architectural approach
- Keep code consistent with examples

**Write Tests:**
- Match existing test patterns from similar features
- Cover key behaviors and edge cases
- Ensure tests pass before moving to next step

**Verify:**
- Run tests to ensure they pass
- Check for common issues (N+1 queries, unused code)
- Ensure code follows RuboCop standards

### 3. Handle Errors
- If tests fail, debug and fix immediately
- If pattern doesn't fit perfectly, adapt pragmatically
- If blocked, ask for guidance

### 4. Final Check
Before marking as complete:
- [ ] All tests passing
- [ ] No debug statements left
- [ ] Follows patterns from example files
- [ ] Controllers are thin
- [ ] No N+1 queries
- [ ] Security considerations addressed

### 5. Summary
Provide a brief summary of what was implemented:
- Files created/modified
- Tests added
- Any deviations from the plan (and why)
- Ready for code review

## Usage

```bash
/implement
```

That's it. I'll execute the plan we discussed and approved.

## What Makes This Effective

**The plan already identified the patterns to follow**, so implementation becomes:
1. Read the example file
2. Follow its pattern
3. Test it works
4. Move to next step

Instead of making architectural decisions during implementation, you're following proven patterns that were researched up front.

## Example Implementation Flow

```markdown
Step 1: Creating FilterComponent following contacts/filter_menu_component.rb...

✓ Created app/components/projects/filter_menu_component.rb
✓ Created app/components/projects/filter_menu_component.html.erb
✓ Added Stimulus controller app/javascript/controllers/project_filter_controller.js
✓ Tests added in test/components/projects/filter_menu_component_test.rb
✓ All tests passing (4 examples, 0 failures)

Step 2: Building service layer following people/search_service.rb...

✓ Created app/services/projects/filter_service.rb
✓ Included CursorPagination concern
✓ Added .includes() to prevent N+1 queries
✓ Tests added in test/services/projects/filter_service_test.rb
✓ All tests passing (6 examples, 0 failures)

...

Implementation complete!

Files created:
- app/components/projects/filter_menu_component.rb
- app/components/projects/filter_menu_component.html.erb
- app/javascript/controllers/project_filter_controller.js
- app/services/projects/filter_service.rb
- app/controllers/projects/filter_options_controller.rb
- test/components/projects/filter_menu_component_test.rb
- test/services/projects/filter_service_test.rb
- test/controllers/projects/filter_options_controller_test.rb

Total: ~380 lines

All tests passing ✓
Ready for /ship
```

## Important Notes

- I implement exactly what the plan specified
- If I need to deviate from the plan, I'll explain why
- I run tests continuously to catch issues early
- I don't skip steps or take shortcuts
- I follow the example files religiously

## When to Use

Use `/implement` after:
1. Running `/plan` to research and create a plan
2. Reviewing and approving the plan
3. You're ready for me to execute

Then use `/ship` to review and create the PR.
