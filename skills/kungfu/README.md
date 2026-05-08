# Kung Fu: Gap Analysis & Skill Development

Perform retrospective analysis of recent development work, identify repeating patterns, and generate new skills to capture institutional knowledge.

## When to Use

Trigger this skill when:
- End of a development session or sprint
- After completing a major feature or epic
- When patterns keep repeating across sessions
- When you want to improve future Claude interactions

**Best run at:** Natural breakpoints (end of day, end of feature, end of epic)

## What It Does

The skill follows a three-phase approach:

### Phase 1: Look Back
- Analyzes recent git commits and session work
- Reviews completed tasks and patterns
- Identifies recurring error patterns

### Phase 2: Gap Analysis
- Detects patterns that appeared 2+ times
- Categorizes gaps: code generation, error patterns, workflow, integration
- Prioritizes based on frequency and value

### Phase 3: Look Forward
- Analyzes remaining work items
- Predicts future skill needs
- Generates new skills automatically

## Output

The skill produces:
- **Analysis Report**: Summary of patterns found
- **New Skills**: Auto-generated SKILL.md files for identified patterns
- **Recommendations**: Actions to improve future sessions

## Usage

Copy the `SKILL.md` file to your project's `.claude/skills/kungfu/` directory, or reference this skill from your Claude Code configuration.

Invoke with: "Perform a kung fu analysis" or "Let's do a look back and look forward"
