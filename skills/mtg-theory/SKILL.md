---
name: mtg-theory
description: Magic: The Gathering strategic theory for card evaluation, format design, and gameplay analysis. Use when evaluating MTG cards, discussing cube/draft design, analyzing matchups, or when user mentions concepts like "card advantage", "tempo", "who's the beatdown", "quadrant theory", "BREAD", or cube design principles like "GRBS" or "decks not cards".
---

# MTG Theory

Strategic theory for card evaluation and format design across all power levels.

## Quick Reference

### The Three Fundamental Resources

**Cards** — Who has more options (actual + virtual)
- Actual: Physical cards in hand
- Virtual: Cards that "don't count" (lands when flooded, removal with no targets)
- Card advantage compounds; early advantages snowball

**Tempo** — Who's using mana more efficiently over time
- Mana equals time; wasted mana is wasted development
- Tempo-positive plays: spend less mana than opponent to answer threats
- Tempo-negative plays: 2-for-1 yourself but develop faster

**Life** — A resource that converts to cards at ~2:1 (Philosophy of Fire)
- 20 life ≈ 7 Shocks worth of damage
- The only life point that matters is the last one
- Aggro decks "buy" cards by dealing damage efficiently

### Role Assignment (Who's the Beatdown)

Every game has exactly two roles:
- **Beatdown**: Must end the game before inevitability kicks in
- **Control**: Must survive until inevitability favors them

**"Misassignment of Role = Game Loss"** — Mike Flores

Role is determined by:
1. Which deck wins the long game (inevitability)
2. Current board/life/card state
3. Matchup context (same deck can be beatdown or control)

Role can shift mid-game as resources change.

### Card Evaluation (Quadrant Theory)

Evaluate cards across 4 board states:

| Quadrant | Board State | Good Cards |
|----------|-------------|------------|
| **Developing** | Early game, establishing board | Efficient creatures, ramp, fixing |
| **Parity** | Stalled, neither ahead | Card draw, evasion, removal |
| **Ahead** | Winning, need to close | Haste, protection, reach |
| **Behind** | Losing, need comeback | Wraths, walls, lifegain |

**Premium cards work in 3+ quadrants.** Most Limited bombs are good when ahead AND behind.

### CABS: Cards Affecting Board State

In Limited, prioritize cards that change the board:
- Creatures (especially with ETB effects)
- Removal
- Combat tricks (context-dependent)
- Auras/Equipment

De-prioritize pure card draw without board impact in aggressive formats.

### The Dialogue Framework

Cards are either **questions** or **answers**:
- Questions: Threats requiring response (creatures, planeswalkers)
- Answers: Removal, counters, interaction

**Temporal mismatch**: Cheap questions + expensive answers = aggro format. Expensive questions + cheap answers = control format.

Format health requires answer-to-question ratio balance.

## Common Evaluation Errors

### 1. Ignoring Virtual Card Advantage
"I 2-for-1'd them!" doesn't matter if those cards weren't going to impact the game anyway.

### 2. Role Misassignment
Playing control with the beatdown deck. Playing aggro when you have inevitability.

### 3. Single-Quadrant Evaluation
"This card is great when I'm winning!" — So is everything else.

### 4. Ignoring Format Context
Shock is unplayable in Vintage, premium in Pauper. Cards exist in formats, not vacuums.

### 5. Ceiling-Only Evaluation
"This card COULD win the game!" — What does it do when you're behind?

### 6. BREAD Over-Application
Bombs > Removal is not universal. Some formats punish expensive cards.

## Format Design Principles

### GRBS: Game-Ruining Bullshit
Cards that end games without meaningful interaction. Tolerance varies by power level:
- **Vintage Cube**: High GRBS tolerance (fast mana, combo)
- **Peasant Cube**: Low GRBS tolerance (interaction matters)

### Decks Not Cards
Design so drafters build archetypes, not piles of good cards.
- Synergy should beat raw power
- Pillar cards define what's possible in each archetype
- Gold cards as signposts

### Power Banding
Flatten the power curve by cutting:
- Highest-ceiling cards (reduces variance)
- Lowest-floor cards (raises average quality)

### Fixing Density
More fixing = slower format = higher curve = more card advantage matters.
Less fixing = faster format = aggro viable = tempo matters more.

## Detailed References

For comprehensive coverage, see:

- **Core Resources**: `references/core-resources.md` — Card advantage (actual vs virtual), tempo, Philosophy of Fire
- **Strategic Frameworks**: `references/strategic-frameworks.md` — Who's the Beatdown, inevitability, fundamental turn, big/small games
- **Card Evaluation**: `references/card-evaluation.md` — Quadrant theory, BREAD/CABS, dialogue framework with examples
- **Format Design**: `references/format-design.md` — GRBS, decks-not-cards, power banding, fixing, pillar cards

## Card Lookup

When evaluating specific cards, use the Scryfall API:
```
https://api.scryfall.com/cards/named?fuzzy={card_name}
```

This provides oracle text, mana cost, type line, and format legality for accurate evaluation.

## Applying Theory

When asked to evaluate a card or discuss strategy:

1. **Identify the format context** (Standard, Limited, Cube power level)
2. **Apply Quadrant Theory** — How does it perform in each board state?
3. **Consider the dialogue** — Is it a question or answer? What's the temporal cost?
4. **Check role implications** — Does it help beatdown or control strategies?
5. **Evaluate floor and ceiling** — What's the worst case? Best case?
6. **Compare to format pillars** — How does it stack against best-in-slot options?
