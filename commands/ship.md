# ship

Review changes and create a pull request

## What This Does

Reviews your implemented changes for quality issues, fixes any critical problems, then creates a well-formatted pull request.

## Steps I Will Take

### 1. Review Changes

Get the full context of what changed:
- Run `git status` to see modified/new files
- Run `git diff main...HEAD` to see all changes
- Run `git log main...HEAD` to understand commit history

### 2. Code Review Analysis

**Look for Critical Issues:**
- 🚨 Unused code (methods defined but never called, unused imports)
- 🚨 Unnecessary code (commented out code, over-engineered abstractions)
- 🚨 Overly defensive code:
  - Unnecessary nil checks where types/framework guarantee non-nil
  - Redundant render? checks in ViewComponents (component's render? already handles this)
  - Error handling for scenarios that can't happen
  - Validation at non-boundary points (trust internal code, only validate user input/external APIs)
  - Defensive checks where Rails/framework features already handle the case
- 🚨 Debug artifacts (console.log, binding.pry, Rails.logger.debug)
- 🚨 Security issues (.html_safe without sanitization, XSS vulnerabilities)
- 🚨 N+1 queries (missing .includes())
- 🚨 Missing tests for new functionality

**Check for Warnings:**
- ⚠️ Complex methods (>15 lines, could be extracted)
- ⚠️ Duplicate code patterns
- ⚠️ Controllers with business logic (should be in services)
- ⚠️ Missing error handling
- ⚠️ Performance concerns
- ⚠️ Hardcoded values that should be constants

**Verify Quality:**
- ✓ Follows established patterns from the codebase
- ✓ Tests are comprehensive
- ✓ Code is readable and self-documenting
- ✓ Respects packwerk boundaries
- ✓ No conflicts with main branch

### 3. Fix Critical Issues

If I find any 🚨 critical issues:
- Fix them immediately
- Run tests to ensure fixes work
- Explain what was fixed and why

If only ⚠️ warnings exist:
- Report them but ask if you want them fixed
- Many warnings are judgment calls

### 4. Prepare for Shipment

- Ensure all tests are passing
- Check that working tree is clean or all changes are committed
- Verify branch is up to date with remote (or needs push)

### 5. Create Pull Request

**Push commits if needed:**
- Use `git push -u origin <branch>` if not yet pushed

**Generate PR description:**
- Create concise summary of changes
- Focus on what and why, not how
- Follow project PR template (no Testing section, no claude mentions)
- Include relevant Linear ticket if available

**Create PR with gh CLI:**
```bash
gh pr create --title "Title from Linear ticket or branch" --body "$(cat <<'EOF'
## Summary
- Bullet points of key changes

## Changes
- Detailed list of modifications

Resolves SEARCH-XXXX
EOF
)"
```

### 6. Return PR URL

Provide the PR URL so you can:
- Review it on GitHub
- Share with team
- Track CI status

## Example Output

```markdown
## Code Review Summary

Reviewed 8 files with 342 lines changed.

### ✅ Good Practices Observed
- Controllers are thin, business logic in services
- N+1 prevention with .includes() in SearchService
- Components properly namespaced
- Tests match existing patterns
- Security: All user input sanitized

### 🚨 Critical Issues Fixed
1. **Removed debug statement** in project_filter_controller.js:24
   - Leftover console.log() would clutter browser console

2. **Removed overly defensive code** in FilterMenuComponent:12
   - Removed `<% if render? %>` wrapper - component's render? method already controls rendering
   - Rails framework guarantees this check happens automatically

3. **Added missing test** for FilterService#apply_filters
   - Edge case with empty filters wasn't covered

### ⚠️ Minor Suggestions (not blocking)
- Consider extracting FilterMenuComponent#build_options to helper (19 lines)
- Hard-coded filter types could be moved to constant

All tests passing ✓
Ready to ship!

---

Pushing commits...
Creating PR...

PR created: https://github.com/huntclub/artemis/pull/1234
```

## Usage

```bash
# Basic usage
/ship

# After reviewing, I'll create the PR automatically
```

## What Gets Reviewed

I focus on **actionable issues** that affect:
1. **Correctness:** Does the code work? Are there bugs?
2. **Security:** Any XSS, injection, or data leak risks?
3. **Performance:** N+1 queries, inefficient algorithms?
4. **Maintainability:** Is it readable? Does it follow patterns?
5. **Completeness:** Are tests adequate? Is error handling present?

I skip nitpicks unless they materially impact quality.

## PR Description Format

Following project guidelines:
- **No Claude mentions** in PR description
- **No Testing section** (tests should be self-evident)
- **No Impact section** (too much boilerplate)
- **Simple and direct** - what changed and why

```markdown
## Summary
- Added filtering functionality to projects list
- Implemented cursor pagination for performance
- Created reusable FilterMenuComponent

## Changes
- New ProjectsFilterService handles filter logic with N+1 prevention
- FilterMenuComponent with Turbo Frame integration
- Stimulus controller for dropdown interactions
- Tests for all new functionality

Resolves SEARCH-1234
```

## Important Notes

- I review the DIFF, not just what I implemented (catches merge issues)
- I fix critical issues automatically, ask about warnings
- I follow project PR conventions strictly
- I ensure tests pass before creating PR
- I return the PR URL when done

## When to Use

Use `/ship` after:
1. `/implement` has finished
2. You've verified the implementation works
3. You're ready to create a PR

The workflow: `/plan` → approve → `/implement` → `/ship` ✨
