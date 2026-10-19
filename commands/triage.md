# triage

Automatically analyze, implement, and create a PR for a Linear ticket tagged with "🤖 claude"

---

## 🚨🚨🚨 MANDATORY: E2E TEST BEFORE PR 🚨🚨🚨

**YOU CANNOT CREATE A PR WITHOUT A PASSING PLAYWRIGHT E2E TEST.**

This is not optional. This is not "nice to have". This is a HARD BLOCKER.

**The E2E test MUST:**
1. Navigate to the actual page where the feature/fix exists
2. Click through the user workflow described in the ticket
3. Verify the expected behavior works
4. Capture a screenshot as proof

**If the E2E test fails:** Fix the code and re-run. Do NOT create a PR with failing tests.
**If you cannot write an E2E test:** STOP and report on Linear. Do NOT create a PR.

**Why this matters:** Unit tests verify code executes. E2E tests verify the feature WORKS for users. A PR without E2E proof is gambling that it works.

---

## What /triage Does (High-Level)

1. **Fetches ticket** from Linear and downloads any attached images
2. **Checks for open questions** - stops if previous run asked questions that haven't been answered
3. **Checks blocking dependencies** - if ticket is blocked, waits for blockers or rebases on their branches
4. **Handles follow-up instructions** - if human replied with an instruction (e.g., "yes, break into smaller tickets"), EXECUTES it
5. **Classifies** the ticket (bug/feature/refactor) and assesses complexity
6. **Validates understanding** - asks clarifying questions on Linear if requirements are unclear
7. **Plans implementation** using `Explore` and `Plan` agents
8. **Implements** by delegating to specialized agents (`frontend-developer`, `backend-developer`, etc.)
9. **Verifies** with RuboCop and full test suite
10. **🚨 RUNS E2E TEST** - Uses `e2e-verifier` agent to write and run Playwright test
11. **🚨 E2E MUST PASS** - If it fails, fix and re-run (up to 3 times). NO PR if test fails.
12. **Creates PR** with screenshot from passing E2E test attached
13. **Reports** results back to Linear ticket

**Special Case - Breaking Into Smaller Tickets:**
When a ticket is too complex and you recommend breaking it up, and the human approves, triage will:
- Create sub-tickets in Linear with proper descriptions and dependencies
- **Run `/triage` on ALL sub-tickets in parallel** using background agents
- Each agent uses a git worktree for isolation
- **Dependent agents create STACKED PRs** based on blocker branches (no waiting!)
- All PRs are created immediately, each targeting its blocker's branch
- Report progress back to the parent ticket

## Linear Status Management

The triage command automatically updates the Linear ticket status as work progresses:

| Stage | Status | When |
|-------|--------|------|
| Start work | **In Progress** | After creating branch (step 1) |
| Need clarification | **Triage** | When asking questions or waiting for answers |
| PR created | **In Review** | After successful PR creation (step 8) |
| Blocked/Failed | **Triage** | When implementation fails or is blocked |

Use `mcp__linear__update_issue` with `state: "Status Name"` to update status.

**Key Principles:**
- Orchestrator only - delegates all code changes to specialized agents
- Proof required - won't create PR without demonstrable evidence fix works
- Fails early - stops and reports on Linear rather than shipping uncertain code

---

## ⚠️ PROOF IS MANDATORY - READ THIS FIRST

**You MUST prove your fix works before creating a PR. Unit tests are NOT proof.**

A PR without proof is gambling that it works. If you cannot demonstrate the fix works from the USER's perspective (not just that code executes), you MUST:
1. Stop and report on Linear why you can't prove it
2. NOT create a PR

**User-visible** means anything users will SEE or RECEIVE: browser UI, emails, PDFs, exports, notifications. Email signature spacing is user-visible because users SEE the emails.

See **Section 7c: PROOF REQUIREMENT** for details on what counts as proof.

---

## 🚨 CRITICAL REQUIREMENT: PLAYWRIGHT TEST + SCREENSHOT

**YOU MUST WRITE A PLAYWRIGHT TEST AND ATTACH A SCREENSHOT TO THE PR.**

This is NON-NEGOTIABLE. Every PR MUST include:
1. **A Playwright E2E test** that verifies the fix/feature works
2. **A screenshot** attached to the PR description proving the fix works

**The E2E test MUST PASS.** If the test fails:
1. Analyze the failure (is it your code or the test?)
2. Fix the issue using the appropriate agent
3. Re-run the test
4. Repeat until it passes (up to 3 attempts)

**NO EXCEPTIONS.** If you cannot write a Playwright test:
- STOP immediately
- Post on Linear explaining WHY you cannot write the test
- DO NOT create a PR

Use the `e2e-verifier` agent to create the test and capture the screenshot. The screenshot MUST be embedded in the PR description.

---

## Key Principle: Orchestrate, Don't Implement

**This command is an ORCHESTRATOR. It coordinates specialized agents but NEVER writes code directly.**

- Use `Explore` agent for codebase research
- Use `Plan` agent for implementation planning
- Use `frontend-developer` agent for UI/template changes
- Use `backend-developer` agent for backend changes (controllers, services, models)
- Use `test-writer` agent for tests
- Use `code-reviewer` agent for review
- Use `triage-verifier` agent for running checks before PR creation

If you find yourself using Grep, Glob, Read, or Edit tools directly (except for initial ticket analysis), STOP and delegate to the appropriate agent instead.

## Arguments
- `$ARGUMENTS` - Linear ticket URL or ID (e.g., `https://linear.app/...` or `SEARCH-1234`)

## What This Does

This command is designed for automated execution via GitHub Actions. When a Linear ticket is tagged with "claude-auto", this command will:
1. Fetch and analyze the ticket
2. Classify the ticket type (bug, feature, refactoring, etc.)
3. Route to the appropriate implementation workflow (via specialized agents)
4. Create a PR with the solution

## Steps I Will Take

### 0. Read Learnings First

**BEFORE doing anything else, read `.claude/TRIAGE_LEARNINGS.md`** to avoid repeating past mistakes. This file contains:
- Common test failure causes and fixes
- Playwright setup gotchas
- Implementation patterns to follow
- Recent learnings from failed triage runs

Also **check for recent PR comments** on merged ai-generated PRs:
```bash
gh pr list --state merged --label ai-generated --limit 5 --json number,title
```

If there are recent merged PRs, check for review comments that haven't been processed yet and extract learnings.

If you encounter a new failure pattern or gotcha during this run, **update the learnings file** before completing.

### 1. Setup Branch (Supports Concurrent Execution)

- Extract Linear ticket ID from `$ARGUMENTS` (e.g., SEARCH-1234)
- Fetch latest from origin: `git fetch origin main`

**For concurrent execution (multiple triage runs at once), use git worktrees:**

```bash
# Create a worktree for this ticket (allows parallel work without conflicts)
TICKET_ID="SEARCH-1234"
WORKTREE_PATH="/tmp/artemis-${TICKET_ID}"

# Remove old worktree if exists
git worktree remove "$WORKTREE_PATH" --force 2>/dev/null || true

# Fetch all branches first
git fetch origin

# Determine base branch (for stacked PRs, use blocker's branch)
BLOCKER_BRANCH=""  # Set this if ticket has a blocker, e.g., "claude/SEARCH-1233"

if [ -n "$BLOCKER_BRANCH" ]; then
  # Check if blocker branch exists
  if git ls-remote --heads origin "$BLOCKER_BRANCH" | grep -q "$BLOCKER_BRANCH"; then
    # STACKED PR: Base on blocker's branch
    BASE_BRANCH="origin/$BLOCKER_BRANCH"
    echo "Creating STACKED PR based on $BLOCKER_BRANCH"
  else
    # Blocker branch doesn't exist yet - poll briefly (see section 2b)
    BASE_BRANCH="origin/main"
  fi
else
  # No blocker - base on main
  BASE_BRANCH="origin/main"
fi

# Create new worktree with branch from determined base
git worktree add -b "claude/${TICKET_ID}" "$WORKTREE_PATH" "$BASE_BRANCH"

# All subsequent commands run in the worktree directory
cd "$WORKTREE_PATH"
```

**For single execution (normal case):**
```bash
# Ensure working directory is clean (stash or warn if uncommitted changes)
git fetch origin
# Use origin/main for standalone, or origin/claude/BLOCKER for stacked PRs
git checkout -b claude/{TICKET_ID} origin/main
```

**After branch setup:**
- **Update Linear status to "In Progress"** using `mcp__linear__update_issue` with `state: "In Progress"`

**Cleanup (after PR created or triage complete):**
```bash
# Return to main repo and remove worktree
cd /Users/tim/dev/artemis
git worktree remove "$WORKTREE_PATH" --force
```

### 2. Fetch Ticket Details

Use Linear MCP tools to get full ticket context:
- `mcp__linear__get_issue` with the ticket ID
- `mcp__linear__list_comments` to get any additional context (including answers to previous questions)
- Extract: title, description, labels, priority, acceptance criteria

**IMPORTANT - Image Handling:**
- Linear image URLs have **5-minute expiration** signatures
- Images MUST be fetched IMMEDIATELY after getting the issue
- To view images:
  1. Extract image URL from description (markdown format: `![...](URL)`)
  2. Download via curl: `curl -s "URL" -o /tmp/linear-image.png`
  3. Use Read tool: `Read /tmp/linear-image.png`
- Images often contain CRITICAL context (UI screenshots showing exactly which page/feature)
- If image fetch fails, ASK for clarification in a Linear comment

**IMPORTANT - Check for Open Questions (MUST DO BEFORE PROCEEDING):**
- Read ALL comments on the ticket using `mcp__linear__list_comments`
- Look for comments from "Claude Code triage" or "Claude Triage" containing questions
- Check if those questions have been answered by a human (reply to the comment, or subsequent comment)

**If you find UNANSWERED questions from a previous triage run:**
1. **STOP IMMEDIATELY** - do not proceed with implementation
2. Post a brief comment: "🤖 Waiting for answers to questions asked on [date]. Skipping this ticket for now."
3. **Ensure Linear status is "Triage"** (should already be, but verify) - this indicates waiting for human input
4. Exit cleanly (no PR, no error status)
5. The ticket will be picked up again on the next triage run after questions are answered

**How to detect unanswered questions:**
- Your previous comments contain phrases like "Clarification Needed", "need some clarification", or end with "?"
- No subsequent human comment addresses the question
- Human comments like "good question, let me check" don't count as answers

### 2b. Check Blocking Dependencies - Stacked PRs (For Sub-Tickets)

**If this ticket has blocking dependencies (blockedBy relations), use STACKED PRs - don't wait for merges.**

Use `mcp__linear__get_issue` with `includeRelations: true` to get blocking issues.

**Stacked PR Strategy (NO WAITING):**

Instead of waiting for blocker PRs to be merged, we create "stacked PRs" where each dependent PR is based on its blocker's branch. This allows all work to proceed in parallel.

```
For each blocking ticket:
  1. Check if blocker has a remote branch: git ls-remote origin claude/SEARCH-XXXX
  2. If branch exists → Base your branch on it (stacked PR)
  3. If no branch yet → Poll briefly (max 5 min) then report and exit

If blocker branch exists:
  → Create your branch based on blocker's branch
  → Create PR targeting blocker's branch (not main)
  → This is a "stacked PR"

If blocker is "Blocked" or "Cancelled":
  → Report issue on Linear and exit
```

**Creating Stacked PRs:**

When a blocker has a branch but PR isn't merged yet, create a stacked PR:

```bash
# Fetch all remote branches
git fetch origin

# Check if blocker branch exists
if git ls-remote --heads origin claude/SEARCH-XXXX | grep -q claude/SEARCH-XXXX; then
  # Create your branch based on the blocker's branch (STACKED PR)
  git checkout -b claude/SEARCH-YYYY origin/claude/SEARCH-XXXX
  echo "Creating stacked PR based on claude/SEARCH-XXXX"
else
  # Blocker branch doesn't exist yet - brief wait
  echo "Blocker branch not found, waiting briefly..."
fi
```

**Brief Polling (Only if blocker branch doesn't exist yet):**

If the blocker branch doesn't exist, poll briefly (max 5 minutes) to give it time to be pushed:

```bash
MAX_WAIT=300  # 5 minutes (not 30!)
POLL_INTERVAL=30  # 30 seconds
elapsed=0

while [ $elapsed -lt $MAX_WAIT ]; do
  git fetch origin
  if git ls-remote --heads origin claude/SEARCH-XXXX | grep -q claude/SEARCH-XXXX; then
    echo "✅ Blocker branch found!"
    break
  fi
  sleep $POLL_INTERVAL
  elapsed=$((elapsed + POLL_INTERVAL))
done

if [ $elapsed -ge $MAX_WAIT ]; then
  # Post comment and exit - blocker hasn't started yet
  echo "🤖 Blocker SEARCH-XXXX branch not found after 5 min. Will retry later."
fi
```

**PR Creation for Stacked PRs:**

When creating a PR for a ticket that depends on another:

```bash
# IMPORTANT: Target the blocker's branch, not main!
gh pr create \
  --title "[AI] SEARCH-YYYY: Title" \
  --base claude/SEARCH-XXXX \  # <-- Target blocker's branch!
  --body "..."
```

**After Blocker PR is Merged:**

Once the blocker PR is merged to main:
1. The dependent PR's base automatically updates (GitHub handles this)
2. OR manually rebase: `git rebase origin/main && git push --force-with-lease`

**Stacked PR Benefits:**
- All work proceeds in parallel immediately
- No waiting/polling for merges
- Each PR shows only its own changes (cleaner review)
- PRs can be reviewed in parallel
- After merge, dependent PRs auto-update their base

---

### 2c. Handle Follow-Up Instructions (EXECUTE, DON'T STOP)

**CRITICAL: When a human replies to your question/recommendation with an instruction, EXECUTE IT - don't just acknowledge and stop.**

After checking for questions, look for **actionable responses** from humans. These are comments that:
1. Reply to a previous triage comment (your question or recommendation)
2. Contain an instruction or approval (e.g., "yes", "do it", "break it up", "proceed with X")

**Common Follow-Up Instructions and How to Handle Them:**

| Human Response | Action to Take |
|----------------|----------------|
| "Yes, break this into smaller tickets" | Create sub-tickets and run /triage on each (see below) |
| "Yes, proceed with Phase 1 only" | Scope implementation to Phase 1, continue with triage |
| "Use approach X" | Update your plan to use approach X, continue with triage |
| "Skip the E2E test for this one" | Note the exception, proceed without E2E (rare) |
| "Focus on [specific part]" | Narrow scope to that part, continue with triage |

**Detecting Actionable Responses:**
```
Previous triage comment contains: "Should I break this into smaller tickets?"
                                  OR "Recommendation: Break into smaller tickets"
                                  OR "What I can do now: Start with Phase 1"

Human reply contains: "yes" / "do it" / "proceed" / "break it" / "go ahead" / "sounds good"

→ This is an INSTRUCTION TO EXECUTE, not just acknowledgment
```

**IMPORTANT:** The ticket status may be "Duplicate", "Canceled", or another terminal state if you previously recommended breaking it up. Check the human's instruction - if they said "yes, break into smaller tickets", the terminal status is EXPECTED. Proceed with creating sub-tickets.

---

### 2d. Breaking Into Smaller Tickets (Parallel Sub-Triage)

When instructed to break a ticket into smaller tickets, follow this workflow:

**Step 1: Identify Sub-Tickets (USER-FACING FEATURES ONLY)**

**🚨 CRITICAL: Each sub-ticket MUST deliver user-visible functionality.**

**DO NOT split by technical layers:**
- ❌ "Phase 1: Data Model" → "Phase 2: Backend API" → "Phase 3: UI Components"
- ❌ Backend-only PRs that users can't see or use
- ❌ Frontend-only PRs without the backend to support them

**DO split by user-facing features:**
- ✅ Each PR delivers something a user can actually DO
- ✅ First PR is a minimal working feature (even if basic)
- ✅ Subsequent PRs add more capabilities users can use

**Example - Kanban Board Feature:**
```
❌ BAD (layer-based splits):
1. Data model for statuses
2. Backend API for status management
3. ViewComponents for board
4. View toggle UI
5. Drag-drop functionality

✅ GOOD (feature-based splits):
1. Basic board view with default columns (users can SEE their contacts organized)
2. Create/edit/delete custom statuses (users can CUSTOMIZE their board)
3. Drag contacts between columns (users can MOVE contacts)
```

**The test:** After merging each PR, can a user do something NEW they couldn't before? If not, combine it with the next PR.

**Step 2: Create Sub-Tickets in Linear**

For each sub-ticket, use `mcp__linear__create_issue`:

```
mcp__linear__create_issue with:
- team: Same as parent ticket
- title: "[Parent-ID] Phase N: Brief description"
- project: Same as parent ticket (if applicable)
- labels: Same labels as parent + "🤖 claude" (for auto-triage)
- description: |
    ## Parent Ticket
    This is part of [SEARCH-XXXX](linear-url): {parent title}

    ## Scope
    {Description of what this sub-ticket covers}

    ## Technical Details
    {Relevant technical details from parent ticket for this phase}

    ## Acceptance Criteria
    - [ ] {Specific criteria for this phase}

    ## Dependencies
    - Blocked by: {Previous phase ticket if applicable}
    - Blocks: {Next phase ticket if applicable}

    ---
    *Auto-created from parent ticket by Claude Code triage*
```

**Step 3: Run /triage on ALL Sub-Tickets in Parallel (Stacked PRs)**

**CRITICAL: ALWAYS launch ALL sub-tickets concurrently using `run_in_background: true`. Each agent creates stacked PRs based on blocker branches.**

Each sub-triage agent will:
1. Use git worktrees to avoid conflicts
2. Check if its blocker has a branch pushed
3. Base its branch on the blocker's branch (creating a stacked PR)
4. Create PR targeting the blocker's branch, not main

**Launch ALL sub-tickets in a single message with multiple Task calls:**

```
# Example: Kanban board broken into user-facing features
# Each sub-ticket delivers something users can DO

Task(subagent_type: "general-purpose", run_in_background: true,
     prompt: "Run /triage on SEARCH-XXXXa (Basic board view). Use worktree at /tmp/artemis-SEARCH-XXXXa. No blockers - base on origin/main.")

Task(subagent_type: "general-purpose", run_in_background: true,
     prompt: "Run /triage on SEARCH-XXXXb (Custom status management). Use worktree at /tmp/artemis-SEARCH-XXXXb. Blocked by SEARCH-XXXXa - create STACKED PR.")

Task(subagent_type: "general-purpose", run_in_background: true,
     prompt: "Run /triage on SEARCH-XXXXc (Drag-drop). Use worktree at /tmp/artemis-SEARCH-XXXXc. Blocked by SEARCH-XXXXa - create STACKED PR.")
```

**Why stacked PRs instead of waiting?**
- ALL work proceeds immediately in parallel
- No polling/waiting for merges (saves 30+ minutes per dependent ticket)
- Each PR shows only its own changes (easier to review)
- PRs can be reviewed and approved in parallel
- After merging, GitHub auto-updates dependent PR bases
- Maximizes throughput - entire feature can be implemented in one session

**Step 4: Update Parent Ticket**

After creating sub-tickets:
1. Update parent ticket status to "Done" or leave as "Duplicate"
2. Add a comment listing all created sub-tickets:

```
🤖 **Triage Report - Broken Into Sub-Tickets**

As requested, I've broken this ticket into smaller, user-facing features:

**Sub-Tickets Created:**
1. [SEARCH-XXXXa](url): Basic board view with default columns
   - Users can: View contacts organized in a Kanban board
2. [SEARCH-XXXXb](url): Custom status management
   - Users can: Create, edit, delete their own status columns
3. [SEARCH-XXXXc](url): Drag-drop between columns
   - Users can: Move contacts between statuses by dragging

**Each PR delivers user-visible functionality.** After merging PR #1, users can already use the board view (even without customization). Each subsequent PR adds more capabilities.

**Execution:** Running /triage on each sub-ticket in parallel.

---
*Claude Code triage*
```

**Step 5: Monitor and Report**

Use `TaskOutput` to check on background agents periodically:
```
TaskOutput(task_id: "{agent-id}", block: false)
```

When all agents complete, post a summary to the parent ticket:
```
🤖 **Sub-Ticket Triage Complete**

| Ticket | Status | PR |
|--------|--------|-----|
| SEARCH-1777a | ✅ PR Created | #1801 |
| SEARCH-1777b | ✅ PR Created | #1802 |
| SEARCH-1777c | ⏳ In Progress | - |
| SEARCH-1777d | ✅ PR Created | #1803 |

---
*Claude Code triage*
```

---

### 3. Classify Ticket Type

Analyze the ticket content to determine the type of work:

**Bug Fix** (keywords: "bug", "error", "broken", "fix", "not working", "crash", "fails"):
- Has reproduction steps or error messages
- Describes unexpected behavior
- References existing functionality that's broken

**Feature** (keywords: "add", "new", "implement", "create", "build"):
- Describes new functionality
- Has acceptance criteria for new behavior
- Introduces new concepts or UI

**Refactoring** (keywords: "refactor", "improve", "optimize", "clean up", "migrate"):
- Improves existing code structure
- Performance optimization
- Technical debt reduction

**Documentation** (keywords: "document", "readme", "update docs"):
- Documentation changes only
- No code changes expected

### 3b. Complexity Assessment

After classification, assess the complexity to determine the workflow:

**Simple Fix** (1-2 files, < 20 lines):
- CSS/styling class changes
- Copy/text changes
- Single field additions
- Simple validation fixes

**Standard Fix** (3-5 files, 20-100 lines):
- New component with existing patterns
- Bug fixes requiring debugging
- Feature additions with clear scope

**Complex Feature** (5+ files, 100+ lines):
- New workflows or user journeys
- Cross-cutting changes
- Architectural decisions needed

| Complexity | Workflow |
|------------|----------|
| Simple | Use `frontend-developer` or `backend-developer` agent directly |
| Standard | Use `Plan` agent first, then implementation agent |
| Complex | Use `Explore` agent, then `Plan` agent, then implementation |

**IMPORTANT:** Even for simple fixes, you MUST delegate to an agent. The only direct tool use allowed in triage is:
- `mcp__linear__*` for ticket operations
- `Bash` for git operations
- `Read` for viewing Linear images

### 4. Validate Understanding (CRITICAL)

Before planning implementation, validate that you correctly understand the request:

1. **Summarize the User's Goal**
   - What is the user trying to accomplish? (not what you think they want)
   - What workflow are they describing? (e.g., "from contact search, add people to a project")
   - What problem are they experiencing?

2. **Identify Ambiguities**
   - Are there images you couldn't view that might contain critical context?
   - Is the described workflow clear, or could it mean multiple things?
   - Are there specific UI elements, pages, or features mentioned that you need to locate?

3. **Ask Clarifying Questions via Linear Comment**
   If ANY of the following are true, POST A LINEAR COMMENT asking for clarification:
   - You cannot view attached images
   - The ticket could describe multiple different features
   - You're unsure which part of the codebase is involved
   - The acceptance criteria are vague or missing

   Use `mcp__linear__create_comment` with a comment like:
   ```
   🤖 **Claude Triage - Clarification Needed**

   I'm analyzing this ticket but need some clarification before proceeding:

   1. [Specific question about the feature/bug]
   2. [Question about which UI/page this affects]
   3. I noticed there's an image attachment but I cannot view it. Could you describe what it shows?

   Once clarified, I'll continue with implementation.

   ---
   *Automated message from Claude Code triage*
   ```

4. **If Questions Asked, STOP**
   - Do NOT proceed with implementation if you've asked questions
   - **Update Linear status back to "Triage"** using `mcp__linear__update_issue` with `state: "Triage"` (indicates waiting for human input)
   - The next /triage run will check for answers in comments

5. **If Understanding is Clear, Proceed**
   - Only continue to planning if you're confident in your understanding
   - Document your interpretation in the plan so humans can verify

### 5. Plan Implementation

**Use the Task tool with agents for all planning and research. Do NOT manually search the codebase.**

1. **Research with Agents**
   Use Task tool → `Explore` agent to:
   - Find similar existing implementations
   - Identify files that will need changes
   - Understand current patterns in the affected area
   - Find relevant tests to use as examples
   - Read architecture docs (`.claude/PATTERNS.md`, domain CLAUDE.md files)

2. **Create Implementation Plan**
   Use Task tool → `Plan` agent to:
   - Analyze the Explore agent's findings
   - List specific files to create/modify
   - Outline the approach for each change
   - Identify any new dependencies or migrations needed
   - Estimate scope (lines of code, number of files)

3. **Assess Confidence**
   - Apply confidence scoring (see below)
   - If Low Confidence: abort and document findings in Linear
   - If Medium/High: proceed with implementation

4. **Document Plan**
   - The Plan agent will output a structured plan
   - Review the plan before proceeding to implementation

### 6. Execute Implementation

**CRITICAL: ALWAYS use the Task tool to delegate implementation to specialized agents. NEVER implement code directly in the triage flow.**

The triage command is an orchestrator - it coordinates agents but does NOT write code itself. This ensures:
- Proper context isolation for each task
- Consistent use of codebase patterns
- Better code quality through specialized agents

Based on ticket classification, delegate to the appropriate agent workflow:

**For Bugs:**
1. Use Task tool → `linear-bug-analyzer` agent to investigate root cause and create a fix plan
2. Use Task tool → `debugger` agent if needed to trace complex issues
3. Use Task tool → `frontend-developer` agent (for UI bugs) OR `backend-developer` agent (for backend bugs) to implement the fix
4. Use Task tool → `test-writer` agent to add regression tests
5. Use Task tool → `triage-verifier` agent to run all checks
6. Use Task tool → `code-reviewer` agent to review changes

**For Features:**
1. Use Task tool → `Plan` agent to research codebase patterns and create implementation plan
2. Use Task tool → `frontend-developer` agent (for UI features: ViewComponents, Stimulus, templates, ERB)
3. Use Task tool → `contact-list-backend` agent (for contact list backend work)
4. Use Task tool → `backend-developer` agent (for other backend features: controllers, services, models)
5. Use Task tool → `test-writer` agent to add tests
6. Use Task tool → `triage-verifier` agent to run all checks
7. Use Task tool → `code-reviewer` agent to review changes

**For Refactoring:**
1. Use Task tool → `Plan` agent to create refactoring plan
2. Use Task tool → `backend-developer` agent to execute the refactoring
3. Use Task tool → `test-writer` agent to verify existing tests still pass
4. Use Task tool → `triage-verifier` agent to run all checks
5. Use Task tool → `code-reviewer` agent to review changes

**For Documentation:**
1. Use Task tool → `backend-developer` agent to update docs
2. No code review needed for pure docs

**Agent Selection Guide:**
| Change Type | Primary Agent |
|-------------|---------------|
| ERB templates, ViewComponents, Stimulus | `frontend-developer` |
| Controllers, Services, Models | `backend-developer` |
| Contact list features | `contact-list-frontend` or `contact-list-backend` |
| Test files (Minitest) | `test-writer` |
| E2E tests + visual proof | `e2e-verifier` |
| Bug investigation | `linear-bug-analyzer` → `debugger` |
| Pre-PR verification | `triage-verifier` |
| Code review | `code-reviewer` |
| Codebase exploration | `Explore` |
| Implementation planning | `Plan` |
| CSS/styling fixes | `styling-fixer` |

### 6b. 🚨 RUN PLAYWRIGHT E2E TEST (MANDATORY - DO NOT SKIP)

**IMMEDIATELY after implementation, BEFORE running the verification gate, you MUST:**

1. **Use Task tool → `e2e-verifier` agent** with:
   - The ticket description and acceptance criteria
   - The user workflow that needs to be tested
   - Files that were changed

2. **The e2e-verifier agent will:**
   - Write a Playwright test that navigates to the affected pages
   - Click through the actual user workflow (not just check page loads)
   - Verify the expected behavior works
   - Capture screenshots as proof
   - Run the test and report results

3. **If the E2E test FAILS:**
   - Analyze the failure (is it your code or the test?)
   - Use the appropriate implementation agent to fix the issue
   - Re-run e2e-verifier
   - Repeat up to 3 times

4. **If the E2E test still fails after 3 attempts:**
   - **DO NOT proceed to verification gate**
   - **DO NOT create a PR**
   - Post detailed failure report on Linear
   - Exit triage

**The E2E test must verify the ACTUAL USER WORKFLOW, not just that pages load.**

Example: For a Kanban board feature, the E2E test must:
- Navigate to a contact list
- Switch to board view
- Verify the board renders with columns
- Create a new status (click button, fill form, submit)
- Verify the new status column appears
- Drag a contact to a different column
- Verify the contact moved

**DO NOT PROCEED TO STEP 7 WITHOUT A PASSING E2E TEST.**

---

### 7. Verification Gate (REQUIRED)

Use Task tool → `triage-verifier` agent to run comprehensive checks. This is a HARD GATE - no PR will be created unless verification passes.

**Critical Checks (must pass):**
- [ ] **FULL test suite passes** (`bin/rails test` - runs ALL tests, not just changed files)
- [ ] RuboCop clean (`bin/rubocop`)
- [ ] No security issues (no hardcoded secrets, no unsafe .html_safe)
- [ ] No debug statements (binding.pry, console.log, puts)

**🚨 FULL TEST SUITE IS MANDATORY:**
You MUST run `bin/rails test` (the complete test suite) before creating a PR. This ensures your changes don't break existing functionality elsewhere in the codebase. Running only tests for changed files is NOT sufficient.

**Warning Checks (flagged in PR):**
- [ ] Change size < 500 lines
- [ ] Test coverage for new files
- [ ] No potential N+1 queries

**If verification fails:**
1. Attempt to fix issues automatically (up to 3 attempts)
2. If still failing, abort and update Linear with:
   - Verification report
   - Specific failures
   - Recommendation for manual handling
3. Do NOT create a partial or failing PR

### 7b. Functional Testing (REQUIRED for UI Features)

**CRITICAL:** Automated tests alone are NOT sufficient for UI features. You MUST think through the user's actual workflow and verify edge cases.

**For any feature involving:**
- Checkboxes, toggles, or selection UI
- Bulk/batch operations
- State transitions (show/hide, enable/disable)
- User interactions that trigger JS/Stimulus

**You MUST verify these scenarios mentally or document them:**

1. **Happy Path**
   - Does the primary use case work? (e.g., "select all → action bar appears")
   - Walk through the EXACT user flow from the ticket

2. **Edge Cases for Selection/Bulk Operations**
   - Single item selection
   - Multiple item selection (2+)
   - Select all (bulk)
   - Deselect some after select all (partial/indeterminate state)
   - Deselect all
   - Empty state (no items to select)

3. **State Transitions**
   - Going from 0 → 1 selected
   - Going from 0 → N selected (bulk operation - DIFFERENT from 0→1!)
   - Going from N → 0 selected
   - Going from N → partial selected

4. **Integration Points**
   - Does this feature interact with other UI elements?
   - Are there existing handlers that might conflict?
   - Does the feature work with infinite scroll / pagination?

**Common Bug Patterns to Watch For:**
- `=== 1` vs `>= 1` checks (bulk operations skip the "exactly 1" state)
- Animation/transition triggers that only fire on specific counts
- Form data not being updated for bulk selections
- Race conditions with async operations

**Document in PR:**
Include a "Functional Testing Checklist" section noting which scenarios were considered.

### 7c. PROOF REQUIREMENT - YOU MUST PROVE THE FIX WORKS

**Unit tests are NOT proof. Unit tests verify code behavior, not that the user's problem is solved.**

> **CRITICAL PHILOSOPHY:** A PR without proof is a PR you're gambling with. It is ALWAYS better to stop and report on Linear than to ship code you haven't proven works.

> **THE LESSON FROM SEARCH-1660:** A unit test checking `signature.strip` works does NOT prove users won't see extra spacing in their emails. The only proof would be:
> 1. An E2E test that sends an email and verifies no extra spacing, OR
> 2. A manual test with screenshot showing the email output, OR
> 3. An integration test that renders the actual email HTML and asserts correct output

**What counts as PROOF:**

| Proof Type | When Valid | Example |
|------------|------------|---------|
| E2E Test (Playwright) | UI in browser | Navigate to page, verify element/content |
| Integration Test | Email/PDF/export output | Render email, assert HTML structure |
| Screenshot/Video | Visual issues | Screenshot showing correct appearance |
| Console Output | Background jobs, data processing | Logs showing expected behavior |
| Database State | Data integrity fixes | Query showing correct values |

**What does NOT count as PROOF:**

| Not Proof | Why Not | What Would Be Proof |
|-----------|---------|---------------------|
| "Unit test passes" | Tests the code, not the outcome | Integration/E2E test of actual output |
| "Code looks correct" | Your judgment isn't proof | Test that verifies behavior |
| "Similar to existing code" | Existing code might be wrong too | Test that this specific case works |
| "RuboCop passes" | Style check, not behavior | Functional test |
| "I'm confident" | Confidence is not evidence | Documented verification |

### 7c-2. BEFORE/AFTER TEST PROOF - MANDATORY FOR NON-UI BUG FIXES

**For backend bug fixes (services, models, jobs, etc.), you MUST demonstrate before/after proof using tests.**

> **THE LESSON FROM SEARCH-1798:** A test that passes on the fix branch is NOT enough. You must show the test FAILS on main (proving the bug exists) and PASSES on your branch (proving your fix works).

**Required Steps:**

1. **Write a test that reproduces the bug scenario**
   - The test should assert the EXPECTED behavior (what SHOULD happen)
   - This test will FAIL on main because the bug exists

2. **Run the test on main (WITHOUT your fix)**
   ```bash
   git stash && git checkout main
   # Add ONLY the test file (not the fix)
   bin/rails test path/to/test.rb:LINE
   # Should FAIL - this proves the bug exists
   ```

3. **Run the test on your fix branch (WITH your fix)**
   ```bash
   git checkout claude/SEARCH-XXXX
   bin/rails test path/to/test.rb:LINE
   # Should PASS - this proves your fix works
   ```

4. **Include both results in your PR and Linear comment**

**Example Before/After Proof (from SEARCH-1798):**

```
**BEFORE (main branch - without fix):**
$ bin/rails test test/services/introduction_response_service_test.rb:107

Failure:
--- expected
+++ actual
-#<Person id: "..." first_name: "Leslie" ...>
+nil

1 runs, 4 assertions, 1 failures

**AFTER (claude/SEARCH-1798 branch - with fix):**
$ bin/rails test test/services/introduction_response_service_test.rb:125

1 runs, 4 assertions, 0 failures, 0 errors, 0 skips
```

**Why This Matters:**
- A passing test only proves code executes correctly NOW
- It does NOT prove the bug ever existed or that your change fixed it
- Before/after proof makes it UNDENIABLE the fix works

**This is MANDATORY for:**
- Service layer bugs
- Model bugs
- Background job bugs
- Any non-UI bug fix

### 7d. E2E Test - MANDATORY FOR USER-VISIBLE ISSUES

**"User-visible" means ANYTHING the user will eventually see or receive, not just browser UI.**

User-visible includes:
- Browser UI (pages, components, modals)
- **Emails** (outreach, notifications, confirmations)
- **PDFs** (reports, exports, attachments)
- **Exports** (CSV, Excel downloads)
- **Notifications** (in-app, push, SMS)
- **API responses** that power external UIs

> **CRITICAL LESSON:** Email signature spacing (SEARCH-1660) is USER-VISIBLE because users SEE the emails. The fix required proof that emails render correctly, not just that a `.strip` call works.

**E2E/Integration Test is MANDATORY when:**
- The bug/feature affects what users SEE anywhere (browser, email, PDF, export)
- The ticket mentions visual issues (blank, missing, wrong content, spacing)
- The ticket includes screenshots or Loom videos showing the problem
- The ticket describes something "appearing", "displaying", or being "sent" to users
- The fix involves rendering, formatting, or display logic

**🚨 Playwright test is ALWAYS required.** The only rare exception:
- PURELY internal processing with ZERO user-visible output (metrics, logs, internal instrumentation)
- Even then, you MUST write a test - just use a different test strategy (integration test, before/after proof)
- When in doubt: WRITE THE PLAYWRIGHT TEST

**THE KEY QUESTION:** Will a user eventually SEE or RECEIVE the output of this code?
- **If YES (browser, email, PDF, export, notification):** Playwright test is MANDATORY
- **If NO (purely internal processing):** Still write a test, but integration/unit test is acceptable

**NEVER skip testing for:**
- Email formatting, content, or delivery
- PDF generation or content
- Export files (CSV, Excel, etc.)
- Any issue with "spacing", "blank", "missing", "wrong", "broken" in the description
- Any ticket with screenshots or videos showing the problem

### 7e. E2E Test & Visual Evidence (Use `e2e-verifier` Agent) - 🚨 MANDATORY

**YOU MUST use Task tool → `e2e-verifier` agent to create, run, and capture evidence from E2E tests.**

**This step is NON-NEGOTIABLE. Every PR requires a Playwright test, GIF, and screenshot.**

The `e2e-verifier` agent will:
1. Check auth prerequisites
2. Create a Playwright test that verifies ALL requirements in a single workflow
3. Run the test with video recording enabled (headless mode)
4. Convert the video to GIF for easy PR viewing
5. **READ AND ANALYZE the GIF/screenshot** to verify ALL requirements are visible
6. If any requirement is missing, update the test and re-run
7. Return paths to evidence files for PR attachment

**CRITICAL: The agent MUST read the visual evidence and verify each requirement is covered.**

### 🔄 E2E TEST MUST PASS - FIX AND RETRY LOOP

**The E2E test MUST PASS before you can create a PR. If it fails, you MUST fix the issues and re-run until it passes.**

**This is the required workflow:**

1. **Run the E2E test** via `e2e-verifier` agent
2. **If the test PASSES** → Proceed to PR creation (Step 8)
3. **If the test FAILS** → Analyze the failure and fix the issue:
   - Read the error message carefully
   - Determine if the issue is in your implementation code OR the test itself
   - Use the appropriate agent (`frontend-developer`, `backend-developer`, etc.) to fix the code
   - OR fix the test if it has incorrect selectors/assertions
4. **Re-run the E2E test** via `e2e-verifier` agent
5. **Repeat steps 2-4** until the test passes (up to 3 fix attempts)

**Common E2E test failures and how to fix them:**
| Failure Type | Likely Cause | Fix Approach |
|--------------|--------------|--------------|
| Element not found | Wrong selector, element not rendered | Check component renders correctly, fix selector |
| Timeout waiting | Page not loading, Turbo issues | Add proper waits, check for JS errors |
| Assertion failed | Implementation doesn't match expected behavior | Fix the implementation code |
| Navigation failed | Wrong URL, auth issues | Check routes, verify auth setup |

**CRITICAL: Do NOT skip to PR creation if the E2E test is failing.** A failing E2E test means your implementation is broken or incomplete. The test exists to prove the fix works - if it fails, the fix doesn't work.

**Only after 3 failed fix attempts** should you stop and report on Linear (see "WHEN E2E TEST FAILS" below).

**Invoke the agent with:**
- Description of what to verify
- **List of ALL acceptance criteria/requirements from the ticket**
- The user workflow from the ticket (pages, actions, expected results)
- Files that were changed (for context)

**The agent returns:**
- Test file path: `e2e/{feature}.spec.ts`
- GIF: `e2e/screenshots/fix-demo.gif` - **Complete workflow covering ALL requirements**
- Screenshot: `e2e/screenshots/fix-evidence.png` - Final state
- Video: `test-results/{test-name}/video.webm` - Full recording
- **Requirements verification table** showing each requirement is covered in the GIF

**What the E2E Test Must Prove:**
- **For bug fixes:** The bug no longer reproduces when following the exact steps from the ticket
- **For features:** The user can complete the workflow exactly as described in acceptance criteria
- **For styling fixes:** The element has the correct visual properties/classes
- **For form changes:** Form submission works and produces expected results

**CRITICAL:** The E2E test must check the ACTUAL USER-VISIBLE result, not just that code executed. Don't just verify an event was created - verify the activity feed shows the correct content.

**Example E2E Test Structure:**
```typescript
// e2e/outreach-template-form.spec.ts
import { test, expect, Page } from '@playwright/test';

async function waitForTurboLoad(page: Page) {
  await page.waitForFunction(() =>
    !document.documentElement.hasAttribute('data-turbo-preview')
  , { timeout: 10000 });
  await page.waitForTimeout(300);
}

test.describe('Outreach Template Form', () => {
  test.use({ storageState: './e2e/.auth/user.json' });

  test('From dropdown has DaisyUI styling', async ({ page }) => {
    const accountSlug = process.env.ACCOUNT_SLUG || 'your-account-slug';

    // Navigate to projects
    await page.goto(`/${accountSlug}/projects?status=active&view=my`);
    await waitForTurboLoad(page);

    // Click into a project and navigate to outreach templates
    // ... navigation steps ...

    // Verify the select has DaisyUI classes
    const fromSelect = page.locator('select[name="outreach_template[sender_selection]"]');
    const classAttribute = await fromSelect.getAttribute('class');
    expect(classAttribute).toContain('select');
    expect(classAttribute).toContain('select-sm');
  });
});
```

---

### WHEN E2E TEST FAILS AFTER 3 FIX ATTEMPTS - STOP AND REPORT

**⚠️ This section only applies AFTER you have attempted to fix and re-run the test 3 times (see "FIX AND RETRY LOOP" above).**

**If the E2E test still fails after 3 fix attempts, DO NOT CREATE A PR. Instead:**

1. **Stop implementation immediately**
2. **Post a detailed comment on the Linear ticket:**

```
🤖 **Claude Triage - Implementation Blocked**

I implemented a fix for this ticket but could not verify it works correctly.

**What I tried:**
- [Describe the implementation approach]
- [List files modified]

**E2E Test Result:**
- Test file: `e2e/[test-name].spec.ts`
- Failure: [Describe what failed]
- Error message: [Include relevant error]

**Why I stopped:**
The E2E test should prove the fix works, but it's failing. Creating a PR without proof would risk shipping a broken fix.

**Possible issues:**
1. [Theory 1 about what might be wrong]
2. [Theory 2]

**Recommendation:**
- [ ] Manual investigation needed
- [ ] OR: Clarify the expected behavior in this ticket

**Branch with partial work:** `claude/SEARCH-XXXX`

---
*Automated message from Claude Code triage*
```

3. **Update ticket status** to indicate blocked/needs-attention
4. **Do NOT create a PR**

---

### WHEN E2E TEST CANNOT BE WRITTEN - STOP AND REPORT

**If you cannot write an E2E test for a UI change (e.g., can't navigate to the page, can't find the element, auth issues), DO NOT CREATE A PR. Instead:**

1. **Stop implementation immediately**
2. **Post a detailed comment on the Linear ticket:**

```
🤖 **Claude Triage - Cannot Verify Implementation**

I implemented changes for this ticket but cannot write an E2E test to verify correctness.

**What I implemented:**
- [Describe the changes]
- [List files modified]

**Why I cannot write an E2E test:**
- [Specific blocker: e.g., "Cannot navigate to the affected page", "Element requires specific data state"]

**What I need to proceed:**
1. [Specific information or access needed]
2. [OR alternative verification approach]

**Branch with partial work:** `claude/SEARCH-XXXX`

---
*Automated message from Claude Code triage*
```

3. **Do NOT create a PR** - a PR without proof is worse than no PR

### 7f. Visual Evidence (Handled by `e2e-verifier` Agent) - 🚨 MANDATORY

The `e2e-verifier` agent automatically captures and verifies visual evidence:
- **GIF:** `e2e/screenshots/fix-demo.gif` - **PRIMARY PROOF** - Complete workflow
- **Screenshot:** `e2e/screenshots/fix-evidence.png` - Final state
- **Video:** `test-results/{test-name}/video.webm` - Full recording

**The agent READS the GIF/screenshot to verify ALL requirements are visible.**

**YOU MUST include the GIF and requirements checklist in the PR description:**
```markdown
## Proof

🎬 **[View Demo GIF](https://github.com/huntclub/artemis/blob/{COMMIT_SHA}/e2e/screenshots/fix-demo.gif)** - Complete workflow

### Requirements Verified
| Requirement | Shown in GIF? |
|-------------|---------------|
| Board displays | ✅ 0:02 |
| Can create columns | ✅ 0:05 |
| Can drag contacts | ✅ 0:08 |
```

**🚨 GIF + requirements verification is ALWAYS REQUIRED. NO EXCEPTIONS.**

The GIF proves to human reviewers that ALL requirements work. Without it, the PR cannot be created.

### 8. Create Pull Request (Human Review Required)

---

## 🛑 HARD STOP - PR CREATION GATE 🛑

**Before you run `gh pr create`, you MUST verify ALL of the following:**

| # | Requirement | How to Verify | STOP if... |
|---|-------------|---------------|------------|
| 1 | E2E test EXISTS | `ls e2e/*.spec.ts` shows your test file | No test file exists |
| 2 | E2E test PASSES | `npx playwright test e2e/your-test.spec.ts` exits 0 | Test fails |
| 3 | E2E test covers USER WORKFLOW | Read the test - does it click through ALL requirements? | Test only checks page loads |
| 4 | GIF EXISTS | `ls e2e/screenshots/fix-demo.gif` shows file | No GIF exists |
| 5 | **GIF was READ & VERIFIED** | Agent read the GIF and confirmed ALL requirements are visible | Requirements not verified |
| 6 | Screenshot EXISTS | `ls e2e/screenshots/fix-evidence.png` shows file | No screenshot |
| 7 | Unit tests pass | `bin/rails test` exits 0 | Tests fail |
| 8 | RuboCop clean | `bin/rubocop` exits 0 | Offenses found |

**If ANY of the above fail: DO NOT CREATE PR. Fix the issue or report on Linear.**

---

**PREREQUISITES - ALL must be true before creating PR:**
- [ ] Verification gate passed (tests, rubocop)
- [ ] **PROOF EXISTS** - You have specific, documented evidence the fix works (see 7c)
- [ ] **🚨 PLAYWRIGHT TEST CREATED** - A Playwright E2E test exists in `e2e/` that verifies the fix
- [ ] **🚨 PLAYWRIGHT TEST PASSES** - The test ran successfully (not just created)
- [ ] **🚨 TEST COVERS ALL REQUIREMENTS** - The test clicks through ALL acceptance criteria, not just some
- [ ] **🚨 GIF CREATED** - Video converted to GIF showing complete workflow
- [ ] **🚨 GIF WAS READ & VERIFIED** - Agent read the GIF and confirmed ALL requirements are visible
- [ ] **🚨 REQUIREMENTS TABLE** - PR includes table showing which requirements are visible in GIF

**THE PROOF REQUIREMENT IS NOT OPTIONAL. If you cannot fill in the "PROOF THAT THIS FIX WORKS" section in your Linear comment with specific evidence, DO NOT CREATE A PR.**

**"I'm confident" is not proof. "Unit tests pass" is not proof. You need evidence of the USER-VISIBLE outcome.**

**If you're uncertain whether it works: DO NOT CREATE PR. Stop and comment on Linear instead.**

**IMPORTANT: All AI-generated PRs require human approval before merge. Auto-merge is disabled.**

Create PR using the AI-generated PR template:

**For standalone PRs (no blockers):**
```bash
gh pr create \
  --title "[AI] SEARCH-XXXX: Title from ticket" \
  --body-file .github/AI_PR_TEMPLATE.md \
  --label "ai-generated" \
  --label "needs-review" \
  --reviewer huntclub/searchos
```

**For stacked PRs (has blockers):**
```bash
# IMPORTANT: Use --base to target the blocker's branch!
gh pr create \
  --title "[AI] SEARCH-XXXX: Title from ticket" \
  --base claude/SEARCH-BLOCKER \
  --body-file .github/AI_PR_TEMPLATE.md \
  --label "ai-generated" \
  --label "needs-review" \
  --label "stacked-pr" \
  --reviewer huntclub/searchos
```

**Stacked PR Description Addition:**
When creating a stacked PR, add this to the PR body:
```markdown
## ⚠️ Stacked PR

This PR is based on [#BLOCKER_PR_NUMBER](blocker-pr-url) and should be reviewed/merged AFTER that PR.

**Dependency Chain:**
1. #BLOCKER_PR_NUMBER ← merge first
2. This PR ← merge second

After the base PR is merged, this PR's base will automatically update to `main`.
```

PR will include:
- `ai-generated` label for easy filtering
- `needs-review` label requiring human approval
- SearchOS team as reviewers
- Verification report summary
- Link to Linear ticket
- Reviewer checklist

**PR Description includes:**
- Summary of changes
- Files modified with brief explanations
- Verification results
- Confidence level and any warnings
- Checklist for human reviewer
- **FOR UI-VISIBLE ISSUES: Screenshot showing the fix works** (embed directly in PR description)

**After PR is created:**
- **Update Linear status to "In Review"** using `mcp__linear__update_issue` with `state: "In Review"`

**Including Screenshots in PR:**
Screenshots are committed to the PR branch by the `e2e-verifier` agent.

**IMPORTANT:** Relative paths do NOT work in PR descriptions - GitHub treats them as compare URLs, not file paths. For private repos, `raw.githubusercontent.com` URLs also fail without authentication.

**Use the blob URL with commit SHA:**
```markdown
## Proof

📸 **[View Screenshot](https://github.com/huntclub/artemis/blob/{COMMIT_SHA}/e2e/screenshots/fix-evidence.png)** - Description of what the screenshot shows.
```

Get the commit SHA with `git rev-parse HEAD` after committing. This provides a clickable link for authenticated users (not inline rendering, but functional).

For inline image rendering, a human would need to edit the PR via GitHub web UI and drag-drop the image to upload it to GitHub's CDN.

### 9. Update Linear Ticket

After PR creation (or when blocked), post an execution report to Linear:

**Always post a triage report comment using this format:**

```
🤖 **Triage Report**

**Result:** ✅ PR Created / ❌ Blocked / ⚠️ Needs Clarification

**Classification:** [Bug/Feature/Refactor] | [High/Medium/Low] confidence | ~N lines

**Steps Completed:**
1. ✅ Branch: `claude/SEARCH-XXXX`
2. ✅ Understood: [1-line summary of interpretation]
3. ✅ Found: `path/to/file.rb:NN`
4. ✅ Changed: [brief description]
5. ✅ Tests: 9 passed
6. ✅ Proof: [REQUIRED - see below]

**Files Modified:**
- `app/views/file.erb:38` - [what changed]

**PROOF THAT THIS FIX WORKS:**
[This section is MANDATORY. You must explain HOW you verified the fix works from the user's perspective.]

For user-visible issues, include ONE of:
- E2E test: "`e2e/test.spec.ts` - navigates to [page], verifies [expected behavior]"
- Integration test: "Test renders actual email HTML and asserts no extra `<br>` tags before signature"
- Screenshot: [Attach or link to screenshot showing the fix]
- Manual verification: "Ran `rails runner 'puts SignatureFormatter.format_signature_html("\n\nTest\n\n")'` and confirmed output is `Test` with no leading `<br>` tags"

For non-user-visible issues only:
- "This is internal processing only (describe why). Verified via [logs/metrics/database query]."

**PR:** https://github.com/huntclub/artemis/pull/XXXX

---
*Claude Code triage*
```

**CRITICAL: The "PROOF" section is NOT optional.** If you cannot fill it in with specific evidence, you have not proven the fix works. Go back and create proof before creating a PR.

**BEST PROOF: Show BEFORE vs AFTER.** Demonstrate what the output WAS (broken) vs what it IS NOW (fixed). This makes it undeniable the fix works.

**Examples of GOOD proof statements:**
- "**Before/After:** Rails runner shows old code produced `<br><br>Best regards` (extra spacing), new code produces `Best regards` (no extra spacing)"
- "E2E test `e2e/email-signature.spec.ts` sends an outreach email and verifies the HTML contains no leading `<br>` before the signature text"
- "Integration test renders `append_signature_to_content` with `"\n\nBest,\nJohn\n\n"` and asserts output starts with `Best,` not `<br>`"
- "Screenshot: BEFORE shows 2 blank lines above signature, AFTER shows signature aligned correctly"
- "Rails runner: BEFORE=`<br><br>Test<br><br>` → AFTER=`Test` (whitespace stripped)"

**Examples of BAD proof statements:**
- ❌ "Unit tests pass" (tests the code, not the user experience)
- ❌ "Added .strip which removes whitespace" (describes what, not proves it works)
- ❌ "RuboCop clean" (style check, not functional verification)
- ❌ "E2E: Skipped (trivial fix)" (NEVER skip proof for user-visible issues)
- ❌ "Confident this works" (confidence is not evidence)

**For blocked/failed runs, include:**
```
**Blocked At:** Step N - [description]
**Error:** [brief error message]
**Branch:** `claude/SEARCH-XXXX` (partial work)
```

**Then update Linear status:**
- **If PR created:** Status should already be "In Review" (updated after PR creation)
- **If blocked/failed:** Update status back to "Triage" using `mcp__linear__update_issue` with `state: "Triage"` (needs human attention)
- The report enables debugging failed triage runs

## Confidence Scoring

Before implementing, assess confidence level:

**High Confidence (proceed automatically):**
- Clear requirements with acceptance criteria
- Similar patterns exist in codebase
- Straightforward bug with clear reproduction
- Estimated < 500 lines of changes

**Medium Confidence (proceed with caution):**
- Some ambiguity in requirements
- May require architectural decisions
- Estimated 500-1000 lines

**Low Confidence (abort and document):**
- Unclear or conflicting requirements
- Major architectural changes needed
- Cross-cutting concerns affecting multiple systems
- Estimated > 1000 lines

For low confidence tickets, update Linear with analysis and recommendations instead of implementing.

## Error Handling

**If ticket fetch fails:**
- Log error and abort
- Switch back to previous branch

**If classification is uncertain:**
- Default to "Feature" workflow
- Note uncertainty in PR description

**If implementation fails:**
- Capture error details
- Update Linear ticket with status
- Do not create partial PR

**If tests fail:**
- Attempt to fix up to 3 times
- If still failing, abort and document

**If PR creation fails:**
- Commit changes are preserved on branch
- Log error for manual intervention

## Learning from PR Comments

**After a triage PR is reviewed**, extract learnings from the review comments and store them for future runs.

**When to check for PR learnings:**
- At the start of a triage run, check if there are any recent merged/closed PRs with review comments
- Use `gh pr list --state merged --label ai-generated --json number,title,url` to find recent AI PRs
- For each, use `gh api repos/{owner}/{repo}/pulls/{number}/comments` to get review comments

**What to look for:**
- Code style corrections ("use X instead of Y")
- Pattern violations ("we don't do it this way")
- Missing edge cases ("what about when X happens?")
- Better approaches ("consider using the existing Z helper")

**How to store learnings:**
1. Add to `.claude/TRIAGE_LEARNINGS.md` under "Recent Learnings"
2. Include the PR number and a brief summary of the learning
3. Format as actionable guidance for future runs

**Example learning entry:**
```markdown
### PR #1234: Use existing helper for person lookup
- **Issue:** Created custom SQL query to find person by email
- **Learning:** Use `Person.find_by_email_or_create` helper instead
- **Applies to:** Any code that looks up people by email
```

## Logging Improvements & Issues

When you encounter issues or notice opportunities for improvement during triage, **create a Linear ticket** to track them.

**When to create an improvement ticket:**
- Found confusing code patterns that should be documented
- Test setup is brittle or unclear
- Missing test coverage for common scenarios
- E2E test infrastructure issues (auth, selectors, timing)
- Codebase patterns that caused you to make mistakes

**How to create:**
```
mcp__linear__create_issue with:
- team: "SEARCH"
- title: "[Triage Feedback] Brief description"
- labels: ["triage-feedback"]
- description: |
    **Discovered during:** SEARCH-XXXX triage run

    **Issue:** What problem did you encounter?

    **Suggestion:** How could this be improved?

    ---
    *Auto-created by Claude Code triage*
```

**Also update learnings:**
If the issue affected your implementation, add it to `.claude/TRIAGE_LEARNINGS.md` so future runs avoid the same problem.

## Terminal Output

Print a brief summary to terminal after completion:

```
## SEARCH-XXXX: [Title]
**Result:** ✅ PR #1735 / ❌ Blocked
**Files:** app/views/file.erb (1 line changed)
**Tests:** 9 passed
**Linear:** Report posted
```

The detailed execution report is posted to Linear (see Step 9).

## Safety Rails

This command includes safety measures:
- **No force pushes** - Never overwrites remote branches
- **No destructive operations** - Preserves existing code/data
- **Confidence gating** - Aborts on low-confidence tickets
- **Verification gate** - Must pass `/verify` before PR creation
- **Full test suite required** - Must run `bin/rails test` (ALL tests) and have them pass before PR creation
- **🚨 Playwright test MANDATORY** - Every PR MUST have a Playwright E2E test proving the fix works
- **🚨 E2E test MUST PASS** - If the test fails, fix the issue and re-run until it passes (up to 3 attempts)
- **🚨 GIF MANDATORY** - Every PR MUST have a GIF showing the complete workflow
- **🚨 GIF MUST BE READ & VERIFIED** - Agent MUST read the GIF and verify ALL requirements are visible
- **🚨 Requirements table MANDATORY** - PR MUST include a table showing which requirements are covered
- **Certainty requirement** - You must be POSITIVE ALL requirements are implemented. The GIF is your proof.
- **Fail early philosophy** - It is ALWAYS better to stop and report on Linear than to create a PR you're not certain works
- **Size limits** - Warns on large changes
- **Human review required** - All PRs require human approval, auto-merge disabled
- **Clear labeling** - PRs labeled `ai-generated` and `needs-review`

## Usage

This command is designed for automated execution but can be run manually:

```bash
# Manual execution
/triage SEARCH-1234

# With full URL
/triage https://linear.app/hunt-club/issue/SEARCH-1234/ticket-title
```

## Integration with GitHub Actions

This command is invoked by the `.github/workflows/claude-triage.yml` workflow:
1. Workflow polls Linear for AI-tagged tickets
2. For each ticket, runs `claude "/triage SEARCH-XXXX"`
3. Workflow reports success/failure back to Linear
