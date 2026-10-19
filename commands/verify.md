# verify

Run comprehensive verification checks before creating a PR

## What This Does

Runs all quality gates to ensure changes are safe to ship. This command MUST pass before any AI-generated PR is created. It acts as a safety net to catch issues before they reach human reviewers.

## Verification Checklist

### 1. Test Suite (Critical)
```bash
bin/rails test
```
- ALL tests must pass
- No skipped tests in modified files
- If tests fail, abort immediately

### 2. Static Analysis (Critical)
```bash
bin/rubocop
```
- No RuboCop violations
- Auto-fix what can be fixed
- Abort if unfixable violations remain

### 3. Package Boundaries (Critical)
```bash
bin/packwerk check
```
- No Packwerk boundary violations
- Respect package dependencies

### 4. Security Scan (Critical)
Check for common security issues:
- [ ] No `.html_safe` without proper sanitization
- [ ] No hardcoded secrets, API keys, or passwords
- [ ] No `eval()` or dynamic code execution
- [ ] No SQL injection vulnerabilities (raw SQL with user input)
- [ ] No mass assignment vulnerabilities
- [ ] No exposed debug endpoints or statements

### 5. Code Quality (Critical)
- [ ] No `binding.pry`, `debugger`, `byebug` statements
- [ ] No `console.log`, `console.debug` in JS
- [ ] No `puts`, `p`, `pp` debug statements in Ruby
- [ ] No commented-out code blocks
- [ ] No TODO/FIXME that should be addressed

### 6. Change Size Analysis (Warning)
Analyze the diff:
```bash
git diff main --stat
```
- **Green**: < 200 lines changed
- **Yellow**: 200-500 lines changed (acceptable)
- **Red**: > 500 lines changed (requires justification)

Report file count and line changes.

### 7. N+1 Query Check (Warning)
Scan new/modified code for potential N+1 patterns:
- Loops that access associations without `.includes()`
- New scopes without eager loading considerations

### 8. Test Coverage (Warning)
Verify new code has tests:
- New models have model tests
- New controllers have controller tests
- New services have service tests
- New components have component tests

## Output Format

```markdown
# Verification Report

## Summary
- **Status**: [PASSED | FAILED]
- **Tests**: X passed, Y failed
- **RuboCop**: X offenses (Y auto-fixed)
- **Packwerk**: [Clean | X violations]
- **Security**: [Clean | X issues found]
- **Change Size**: X files, Y insertions, Z deletions

## Critical Issues (Must Fix)
[List any blocking issues]

## Warnings (Should Review)
[List any non-blocking concerns]

## Verification Checklist
- [x] All tests pass
- [x] RuboCop clean
- [x] Packwerk boundaries respected
- [x] No security issues
- [x] No debug statements
- [ ] Test coverage for new code (missing: app/services/new_service.rb)

## Recommendation
[SAFE TO SHIP | NEEDS FIXES | NEEDS HUMAN REVIEW]
```

## Exit Codes

- **0**: All checks passed, safe to create PR
- **1**: Critical issues found, do not create PR
- **2**: Warnings found, PR can be created but flag for review

## Steps I Will Take

### Phase 1: Run Test Suite
```bash
bin/rails test 2>&1
```
- Capture output
- Parse for failures
- Abort if any test fails

### Phase 2: Run RuboCop
```bash
bin/rubocop -a 2>&1
```
- Auto-fix violations
- Check for remaining issues
- Commit auto-fixes if any

### Phase 3: Run Packwerk
```bash
bin/packwerk check 2>&1
```
- Check boundary violations
- Report any issues

### Phase 4: Security Scan
Use grep to find security anti-patterns:
```bash
# Check for dangerous patterns
grep -r "\.html_safe" --include="*.rb" --include="*.erb" app/
grep -r "eval(" --include="*.rb" app/
grep -r "secret\|password\|api_key" --include="*.rb" app/ | grep -v "ENV\|secrets\|credentials"
```

### Phase 5: Debug Statement Scan
```bash
# Ruby debug statements
grep -rn "binding\.pry\|byebug\|debugger" --include="*.rb" app/ lib/

# JS debug statements
grep -rn "console\.log\|console\.debug" --include="*.js" app/javascript/

# Print statements
grep -rn "^[[:space:]]*puts\|^[[:space:]]*p[[:space:]]\|^[[:space:]]*pp[[:space:]]" --include="*.rb" app/
```

### Phase 6: Analyze Change Size
```bash
git diff main --stat
git diff main --numstat | awk '{add+=$1; del+=$2} END {print "+"add, "-"del}'
```

### Phase 7: Check Test Coverage
For each new file in app/, verify corresponding test exists:
- `app/models/foo.rb` → `test/models/foo_test.rb`
- `app/controllers/foo_controller.rb` → `test/controllers/foo_controller_test.rb`
- `app/services/foo_service.rb` → `test/services/foo_service_test.rb`
- `app/components/foo_component.rb` → `test/components/foo_component_test.rb`

### Phase 8: Generate Report
Compile all results into verification report.

## Usage

```bash
# Run before shipping
/verify

# Typically called by /triage before PR creation
```

## Integration with /triage

The `/triage` command MUST run `/verify` before creating any PR:

1. Implementation complete
2. Run `/verify`
3. If FAILED → abort, update Linear with issues
4. If PASSED → proceed to PR creation

## What This Catches

**Real examples of issues this prevents:**

1. **Forgotten debug statement** → Caught by debug scan
2. **Broken test from implementation** → Caught by test suite
3. **RuboCop style violation** → Auto-fixed or caught
4. **N+1 query introduced** → Flagged for review
5. **Missing test for new service** → Warned about coverage
6. **Hardcoded API key** → Caught by security scan
7. **Package boundary crossed** → Caught by Packwerk

## Important Notes

- This command is READ-ONLY except for RuboCop auto-fixes
- All checks must pass before any AI-generated PR is created
- Warnings don't block PR but are included in PR description
- Human reviewers should still do thorough review
