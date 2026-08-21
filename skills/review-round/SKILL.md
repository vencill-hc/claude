---
name: review-round
description: Handle a round of PR review comments end to end in gdulabs repos - fetch threads, triage, implement or push back, draft (never post) replies for Vanessa, save the round to the workpod. Use when asked to "address the review comments", "respond to the review", "move the PR forward", or when a PR has new reviewer feedback. Not for performing a review of someone else's PR (use pr-code-review).
---

# Review Round

The recurring loop for responding to reviewer feedback on Vanessa's PRs. Judgment rules come from superpowers:receiving-code-review (invoke it first); this skill is the repo- and user-specific mechanics around it.

## Fetch

```sh
gh pr view <N> --json title,body,state,baseRefName,headRefName
gh api repos/{owner}/{repo}/pulls/<N>/comments --paginate \
  --jq '.[] | "=== id:\(.id) in_reply_to:\(.in_reply_to_id // "none") \(.user.login) @ \(.path):\(.line // .original_line)\n\(.body)\n"'
gh api repos/{owner}/{repo}/pulls/<N>/reviews --jq '.[] | "=== \(.user.login) [\(.state)]:\n\(.body)\n"'
```

Then check `git log` against the comment timestamps: earlier rounds may have already addressed some threads (commits like "Consolidate avatar host validation" landed before the comment was read). Don't re-do addressed work.

## Triage

Per superpowers:receiving-code-review: verify each item against the codebase before implementing, push back with technical reasoning when warranted. House precedents worth knowing:

- Copilot flags `YAML.load_file` as unsafe; Ruby 3.4 ships Psych 5 which safe-loads by default. Change if harmless, but say so.
- Copilot flags own-profile fixtures as "personal data"; deliberate self-captured fixtures are fine, keep as-is.
- Scope-cut requests (a maintainer asking to defer a subsystem): find the minimal delta that keeps the fix's production path. Ask what the fix actually needs vs what existed for tooling; revert files to main verbatim where possible.

## Implement and Verify

Run the affected tests, rubocop, and packwerk before claiming done. Environment bring-up for data-universe-rails is fully documented in `universe-expert/references/rails_repo_test_environment.md` (PATH fixes, lo0 alias, minimal docker service set, `db:prepare`). Stop the docker stack after (`docker compose stop`, keep volumes).

## Communicate

- NEVER post comments, review replies, or reviews as Vanessa. Draft the reply text per thread and hand her the command:
  `gh api repos/{owner}/{repo}/pulls/<N>/comments/<thread-id>/replies -f body='...'`
- Reply drafts go through editorialize (abstract end of the dial; her existing replies on the PR are the register sample). Factual, cites commit hashes, pushes back plainly, no thanks.
- PR body edits are allowed directly (`gh pr edit`, established 2026-08-20) and go through the pr-body skill. If the round changed scope, the body's testing story probably changed too.
- Commits: push to the PR branch freely; that is the work she asked for.

## Save

Log the round to the workpod thread (`wp-log`), tick any completed plan items, append reviewer-decision rationale to `notes.md`, refresh `state.md` Status/Next step. Record what was drafted-but-not-posted so the next session knows the replies may still be pending.
