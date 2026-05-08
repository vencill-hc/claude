# Active Learning Skill

Transforms Claude Code conversations into interactive learning experiences through Socratic questioning and guided discovery.

## When to Use

Trigger this skill when:
- User says "Let's learn this together"
- User says "Teach me" or "Help me understand"
- User wants to deeply understand concepts rather than just get solutions
- User is learning a new technology or codebase

**Not for:** Production emergencies or time-sensitive fixes where you need quick solutions.

## What It Does

Instead of immediately providing solutions, Claude will:

1. **Ask questions first** to activate your prior knowledge
2. **Break down problems** into smaller, digestible questions
3. **Guide you to discover** solutions through iterative questioning
4. **Explain the reasoning** behind decisions, not just the "what"
5. **Build on your responses** to deepen understanding

## Example Interaction

```
User: I need to add a new API endpoint

Claude (with skill):
Q: What data will this endpoint work with?
[Waits for your response]

Q: Will it retrieve data or modify data?
[Waits for your response]

Q: Based on that, what HTTP method should this endpoint use?
[Guides you to the answer]
```

## Learning Principles Applied

- **Active Recall**: Retrieving information strengthens memory better than passive reading
- **Socratic Method**: Questions reveal gaps and build understanding
- **Guided Discovery**: Learning by doing creates lasting knowledge
- **Mistake-Friendly**: Wrong answers are valuable learning opportunities

## Usage

Copy the `SKILL.md` file to your project's `.claude/skills/active-learning/` directory, or reference this skill from your Claude Code configuration.
