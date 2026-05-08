# Format and Cube Design

Principles for designing balanced, engaging Limited environments.

## GRBS: Game-Ruining Bullshit

### Definition

GRBS refers to cards or interactions that end games without meaningful player agency. The game is "ruined" when:
- One player had no reasonable counterplay
- The outcome felt predetermined
- Interaction was impossible or impractical

### Examples of GRBS

**High GRBS cards:**
- Sol Ring (too much acceleration)
- True-Name Nemesis (unanswerable in many formats)
- Emrakul, the Aeons Torn (protection from everything)
- Channel + Fireball (turn 1 kill)

**GRBS mechanics:**
- Free spells (Hogaak, Force of Will in the wrong context)
- Uncounterable + hexproof + indestructible
- Infinite combos without interaction points
- Mana acceleration beyond format norms

### GRBS Tolerance by Power Level

| Power Level | GRBS Tolerance | Example Format |
|-------------|----------------|----------------|
| Vintage Cube | Very High | Fast mana, combo, broken cards |
| Legacy Cube | High | Powerful but some limits |
| Modern Cube | Medium | Efficiency, less cheese |
| Peasant Cube | Low | Interaction must matter |
| Pauper Cube | Very Low | Grindy, fair games |

### Managing GRBS in Design

**Accept some GRBS:**
- Defines format power level
- Creates memorable moments
- Differentiates from other formats

**Limit GRBS through:**
- Providing answers at same rate as threats
- Cutting most egregious offenders
- Ensuring interaction points exist
- Power banding (see below)

## Decks Not Cards

### The Riptide Lab Philosophy

From Riptide Lab's cube community: design environments where drafters build **decks**, not collections of individually powerful cards.

**"Decks Not Cards" means:**
- Synergy should beat raw power
- Archetypes should be clearly defined
- Build-arounds should be rewarded
- Good stuff piles should be suboptimal

### Implementation

**Signpost uncommons:**
- Gold cards that clearly say "draft this archetype"
- Example: Psychatog signals UB graveyard

**Synergy payoffs:**
- Cards that are weak alone, strong in context
- Example: Burning Vengeance in flashback deck

**Archetype density:**
- Enough support cards that synergy is achievable
- Not so many that decks build themselves

### Common Design Failure

**"Good stuff" dominates** when:
- Individual card power exceeds synergy payoffs
- Not enough support for archetypes
- Signposts are too weak
- Good cards go in every deck

**Fix:** Strengthen archetype payoffs OR weaken generically good cards.

## Power Banding

### Ceiling/Floor Flattening

Power banding means narrowing the gap between the best and worst cards:
- Cut the highest-ceiling cards (reduces blowouts)
- Cut the lowest-floor cards (raises average quality)

### Why Power Band?

**Benefits:**
- More consistent draft experience
- Skill matters more than opens
- Synergy can compete with power
- Games are interactive

**Costs:**
- Less "epic" moments
- Some archetypes lose key cards
- Format may feel samey

### Power Banding in Practice

**Before:** Sol Ring (too high), Goblin Piker (too low)
**After:** Neither included; middle-power cards fill slots

**Example band for Peasant Cube:**
- No cards that win the game alone
- No cards that are embarrassing to play
- Sweet spot: efficient, interesting, interactive

### Finding Your Band

Ask:
1. What power level creates the games I want?
2. What's the most powerful card I'm comfortable with?
3. What's the weakest card that's still playable?

Everything outside that range gets cut.

## Fixing Density

### How Fixing Shapes Format Speed

Mana fixing density directly impacts format:

**High fixing density:**
- 3+ color decks viable
- Slower format (spending picks on fixing)
- Card quality matters (can play best cards)
- Synergy across colors possible

**Low fixing density:**
- 2-color only viable
- Faster format (more threats picked)
- Aggro stronger (consistent mana)
- Color commitment matters

### Fixing Density Guidelines

| Format Goal | Fixing Targets |
|-------------|----------------|
| Fast/Aggro | ~1 dual per drafter |
| Balanced | ~2 duals per drafter |
| Slow/Grindy | ~3+ duals per drafter |
| 3-color normal | 3.5+ duals per drafter |

### Fixing Quality Matters

**Premium fixing:**
- Fetchlands
- Shocklands
- Original duals
- Fast lands

**Medium fixing:**
- Check lands
- Pain lands
- Filter lands

**Weak fixing:**
- Tap lands
- Bounce lands
- Vivid lands

Premium fixing enables aggro while fixing. Weak fixing taxes tempo.

### Format Speed Interaction

Fixing interacts with:
- Average CMC of playables
- Presence of mana sinks
- Multicolor payoffs
- Aggro card density

More fixing + higher curve = slower format.
Less fixing + lower curve = faster format.

## Pillar Cards

### Best-At-Role Definition

**Pillar cards** are the best cards at their specific role in a format. They define what's possible:

- Best 1-drop aggro creature → sets aggro baseline
- Best unconditional removal → sets interaction standard
- Best card draw spell → sets control ceiling

### How Pillars Define Formats

Every archetype has pillar cards that make it viable:

**Mono-Red Aggro pillars:**
- Best 1-drop (Goblin Guide, Monastery Swiftspear)
- Best burn spell (Lightning Bolt)
- Best reach (Fireblast, Light Up the Stage)

**UW Control pillars:**
- Best wrath (Supreme Verdict, Wrath of God)
- Best counterspell (Counterspell, Mana Leak)
- Best card advantage (Teferi, Fact or Fiction)

### Pillar Removal Impact

Removing a pillar card can:
- Kill an archetype entirely
- Shift archetype power level
- Change format dynamics

**Example:** Removing Counterspell from cube makes blue control significantly weaker. Either accept this or find replacement pillar (Mana Drain, Force of Will).

### Identifying Your Pillars

For each archetype:
1. What card is this archetype built around?
2. What cards enable the core strategy?
3. What cards are always first-picked for this deck?

Those are your pillars. Protect them.

## Format Design Process

### Step 1: Define Goals

- What power level?
- How fast should games be?
- How many viable archetypes?
- What play patterns do you want?

### Step 2: Establish Archetypes

- 2-color pairs minimum
- Consider 3-color options
- Define each archetype's game plan
- Identify pillar cards for each

### Step 3: Set Power Band

- Choose ceiling (most powerful acceptable card)
- Choose floor (weakest playable card)
- Cut outside the band

### Step 4: Balance Fixing

- Match fixing to format speed goals
- Consider fixing quality distribution
- Test 3-color viability

### Step 5: Check Dialogue

- Do threats have answers?
- Are answers efficient enough?
- Is interaction possible?

### Step 6: Iterate

- Draft and play
- Note unfun moments (GRBS)
- Note unviable archetypes (missing pillars)
- Adjust and repeat

## Common Design Mistakes

### 1. Power Level Inconsistency
Mixing Vintage Cube cards with Peasant Cube cards. Pick a level and stick to it.

### 2. Unsupported Archetypes
Signposting an archetype without enough support cards. Either commit or remove.

### 3. No Answers to Key Threats
Including bombs without including answers. Check your dialogue.

### 4. Fixing/Speed Mismatch
Slow fixing with aggro cards, or fast fixing with only slow decks.

### 5. Good Stuff Dominance
When the "best deck" is just best cards in good colors, synergy isn't rewarded enough.

### 6. Ignoring As-Fan

**As-fan:** How often a card type appears in a booster pack.

If you want aggro viable, aggro cards need high as-fan. If you want synergy, synergy pieces need high as-fan.

## Testing and Iteration

### Metrics to Track

- Archetype win rates
- Card pick rates
- Game length distribution
- Player enjoyment

### Red Flags

- One archetype dominates
- Cards never making decks (floor too low)
- Cards always first-picked (ceiling too high)
- Games ending before interaction
- Games going too long

### The Feedback Loop

1. Draft
2. Play games
3. Note problems
4. Hypothesize causes
5. Make targeted changes
6. Return to step 1

Good cube design is iterative. No cube is perfect on first draft.
