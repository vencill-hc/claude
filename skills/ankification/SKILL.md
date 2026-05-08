---
name: ankification
description: |
  Create Anki flashcards from notes or content for spaced repetition learning.

  Triggers: "make flashcards", "create Anki cards", "ankify this", "I want to study this",
  "I want to memorize this", "help me learn this", "make cards from this note",
  "create the anki card file", wanting to remember something long-term, use spaced repetition,
  or create SRS prompts. Use for converting a single note or piece of content into flashcards.
---

# Ankification

Transform content into effective Anki flashcards for long-term retention.

## Workflow

1. **Check config** - Look for `.claude-skills.yaml` in working directory or parents for `ankification.output` and `ankification.default_deck`
2. **Identify source** - Read the content to ankify. Ask which note if unclear.
3. **Set deck** - Use config `default_deck` or default to `Programming::Claude-Code`
4. **Set output** - Use config path, ask user, or fallback to `~/Documents/obsidian/claude-code/anki/`
5. **Analyze content** - Identify every discrete piece of knowledge (always more than you think)
6. **Generate cards** - Use START/END format. See [references/card-guide.md](references/card-guide.md) for patterns.
7. **Verify quality** - Each card must be: focused, precise, consistent, tractable, effortful

## Core Principle

> "Write more cards than feels natural."

Each concept needs 3-7 cards. Lists of N items need N+ cards. Fine-grained cards don't increase workload—they make learning reliable and reveal gaps.

## Card Format (Obsidian_to_Anki)

```markdown
START
Basic
Front: Question here?
Back: Answer here

→ [[Source Note Title]]
Tags: deck-name topic
END
```

### Card Types

- **Basic** - Standard Q&A
- **Cloze** - `{{c1::term}}` for definitions (one cloze per card)
- **Basic (and reversed card)** - Creates two cards for bidirectional recall

For detailed patterns, examples, and anti-patterns, see [references/card-guide.md](references/card-guide.md).

## Breaking Down Knowledge

| Content Type | Expected Cards |
|--------------|----------------|
| Simple fact | 1-2 |
| Definition + example | 3-4 |
| Concept with nuance | 5-10 |
| Procedure (5 steps) | 8-15 |
| Comparison (A vs B) | 4-6 |

**Lists → Multiple cards:** A list of 5 items = at least 5 cards, not 1 card with 5 clozes.

**Concepts → Multiple angles:** Definition, mechanism, cause, effect, comparison, application, example, significance.

## Quick Quality Check

- [ ] Each card tests ONE piece of knowledge
- [ ] Lists broken into separate cards
- [ ] No yes/no questions
- [ ] Short questions (avoid pattern-matching bait)
- [ ] Answers formatted for readability (bold, lists)

## Output File Format

```markdown
---
created: {{date}}
updated: {{date}}
author: claude
source: "[[Original Note]]"
source_hash: "{{first 8 chars of MD5}}"
deck: "{{deck-name}}"
card_count: {{number}}
tags:
  - anki/pending
  - deck/{{deck-name}}
cssclasses:
  - anki-cards
---

# {{Topic}} - Anki Cards

TARGET DECK
{{deck-name}}

## Source Notes
- [[Source Note]]

---

START
Basic
Front: {{Question}}
Back: {{Answer}}

→ [[Source Note]]
Tags: {{deck-name}} {{topic}}
END
```

**Filename:** `{{Note Title}} - Cards.md`

## Config

```yaml
ankification:
  output: ./anki/  # relative to config file
  default_deck: "Programming::Claude-Code"
```

---
*See [references/card-guide.md](references/card-guide.md) for comprehensive card patterns, examples, and anti-patterns.*
