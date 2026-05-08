# Card Guide

Comprehensive reference for creating effective Anki cards.

## Table of Contents
- [Five Properties of Good Cards](#five-properties-of-good-cards)
- [Card Types and Syntax](#card-types-and-syntax)
- [Breaking Down Knowledge](#breaking-down-knowledge)
- [Formatting for Readability](#formatting-for-readability)
- [Anti-Patterns](#anti-patterns)
- [Complete Examples](#complete-examples)

---

## Five Properties of Good Cards

Every card should be:

### 1. Focused
One detail per card. Testing multiple things creates inconsistent retrieval.

### 2. Precise
Clear about what's being asked. Vague prompts elicit vague memories.

### 3. Consistent
Same answer every time. Ambiguity causes "retrieval-induced forgetting."

### 4. Tractable
Achievable ~90% recall. If too hard, break down further or add cues.

### 5. Effortful
Requires genuine retrieval, not inference or pattern matching.

---

## Card Types and Syntax

### Basic Card

```markdown
START
Basic
Front: Your question here?
Back: Your answer here

→ [[Source Note]]
Tags: deck-name topic
END
```

### Cloze Deletion

For definitions and key terms. **One cloze per card for lists.**

```markdown
START
Cloze
Text: {{c1::Retrieval practice}} strengthens memory more than passive review.
END
```

### Reverse Card (Bidirectional)

Creates TWO cards automatically. Use for:
- Term ↔ Definition pairs
- Shortcut ↔ Action mappings
- Cause ↔ Effect relationships

```markdown
START
Basic (and reversed card)
Front: What keyboard shortcut activates Plan Mode?
Back: Shift+Tab twice
END
```

This creates:
1. "What keyboard shortcut activates Plan Mode?" → "Shift+Tab twice"
2. "Shift+Tab twice" → "What keyboard shortcut activates Plan Mode?"

**When NOT to use reverse:**
- Conceptual understanding (why/how questions)
- Lists or procedures
- When the reverse would be awkward

### Deep Links to Source Notes

Add after the answer for context when cards are missed:

```markdown
Back: A **single file in the git repo** that stores rules and context

→ [[CLAUDE.md turns team errors into permanent knowledge]]
```

For multiple sources: `→ [[Note A]] | [[Note B]]`

---

## Breaking Down Knowledge

### Lists → Multiple Cards

A list of 5 items = at least 5 cards, not 1 card with 5 clozes.

```markdown
# For "three types of cognitive load"

START
Basic
Front: What is the **first** type of cognitive load?
Back: **Intrinsic** - complexity inherent to the material itself
END

START
Basic
Front: What is the **second** type of cognitive load?
Back: **Extraneous** - complexity from poor presentation or design
END

START
Basic
Front: What is the **third** type of cognitive load?
Back: **Germane** - productive effort that builds schemas
END

START
Basic
Front: How many types of cognitive load are there?
Back: **Three**: intrinsic, extraneous, germane
END
```

### Concepts → Multiple Angles

| Angle | Question Pattern |
|-------|------------------|
| Definition | What is X? |
| Mechanism | How does X work? |
| Cause | What leads to X? |
| Effect | What does X cause? |
| Comparison | How does X differ from Y? |
| Application | When would you use X? |
| Example | Give an example of X |
| Significance | Why does X matter? |

**Example: Retrieval Practice**

```markdown
START
Basic
Front: What is retrieval practice?
Back: The act of recalling information from memory (rather than re-reading it)
END

START
Basic
Front: Why does retrieval practice strengthen memory more than re-reading?
Back: Effortful reconstruction strengthens memory traces; passive exposure only creates familiarity
END

START
Basic
Front: How is retrieval practice different from recognition?
Back: **Retrieval** = generating from memory
**Recognition** = identifying when you see it
END

START
Basic
Front: When should you use retrieval practice while studying?
Back: Immediately after learning, then at spaced intervals - even when difficult
END
```

### Procedures → Decision Points

Don't ask "what are the steps?" - break into individual cards:

```markdown
START
Basic
Front: What's the **first step** when atomizing notes?
Back: Identify key ideas worth remembering long-term (independent of source)
END

START
Basic
Front: After identifying key ideas, what determines if each becomes its own note?
Back: **Can you state it as a complete thought?** If yes, it's atomic enough.
END

START
Basic
Front: What's the title test for atomic notes?
Back: If the title can't be a complete sentence (just a topic label), it's not atomic
END
```

---

## Formatting for Readability

### Bold Key Terms
```markdown
Back: **Intrinsic load** comes from material complexity
**Extraneous load** comes from poor design
```

### Line Breaks for Structure
```markdown
Back: **First step:** Identify the core idea

**Then:** Write it as a complete thought

**Finally:** Add bidirectional links
```

### Bullet Lists (2-4 items)
```markdown
Back: Signs of overfitting:
- Training accuracy >> test accuracy
- Model complexity exceeds data support
- Performance degrades on new data
```

### Code Formatting
```markdown
Back: Link format: `[[Note Title]]`
```

---

## Anti-Patterns

### Yes/No Questions

```markdown
# BAD
Front: Is retrieval practice effective?
Back: Yes

# GOOD
Front: Why is retrieval practice more effective than re-reading?
Back: Retrieval strengthens memory traces; re-reading only creates familiarity
```

### Vague Questions

```markdown
# BAD
Front: Tell me about atomic notes
Back: [wall of text]

# GOOD
Front: What makes a note "atomic"?
Back: Contains **one idea**, developed completely, with a title that's a complete thought
```

### Pattern-Matching Bait

Keep questions short. Long, distinctive wording gets memorized mechanically:

```markdown
# BAD - memorable phrasing
Front: In the sophisticated architecture of evergreen note systems, what elegant mechanism ensures knowledge accumulation?
Back: Dense linking

# GOOD
Front: How do evergreen notes accumulate knowledge over time?
Back: **Dense bidirectional linking** - connecting ideas reveals patterns
```

### Multiple Facts in One Card

```markdown
# BAD
Front: What are the benefits and drawbacks of atomic notes?
Back: [multiple concepts]

# GOOD - separate cards
Front: What's the main benefit of atomic notes?
Back: [one thing]

Front: What's a potential drawback of atomic notes?
Back: [one thing]
```

---

## Complete Examples

### From a Concept Note

**Source:** "CLAUDE.md stores project context"

```markdown
START
Basic
Front: What is CLAUDE.md?
Back: A **single file in the git repo** that stores rules and context for Claude

→ [[CLAUDE.md turns team errors into permanent knowledge]]
Tags: claude-code
END

START
Basic
Front: Where does CLAUDE.md live in a project?
Back: In the **git repository root** (committed with the code)
END

START
Basic
Front: What happens when a team member makes an error with Claude?
Back: The fix gets added to CLAUDE.md, preventing the same error for everyone
END

START
Basic (and reversed card)
Front: What file stores project-specific rules for Claude?
Back: CLAUDE.md
END
```

### From a Procedure Note

**Source:** "How to create atomic notes"

```markdown
START
Basic
Front: What question identifies ideas worth atomizing?
Back: "What here is worth remembering in 5 years, regardless of source?"
END

START
Basic
Front: How do you test if a note title is atomic?
Back: **Can you state it as a complete sentence?** Topic labels fail this test.
END

START
Basic
Front: What's wrong with a note titled "Spaced Repetition"?
Back: It's a **topic label**, not an atomic idea. Better: "Spaced repetition exploits the forgetting curve"
END
```

---

## Tag Conventions

**Export status:**
- `anki/pending` - Not yet exported
- `anki/exported` - Successfully synced
- `anki/needs-update` - Source changed

**Organization:**
- `deck/{{name}}` - Maps to Anki deck
- Spaces separate tags in the Tags line (no commas)

## Source Hash for Updates

The frontmatter `source_hash` (first 8 chars of MD5) enables detecting when source notes change:

1. Compute hash of current source
2. Compare to stored hash
3. If different → cards may need updating
4. Update hash and `updated` date when regenerating
