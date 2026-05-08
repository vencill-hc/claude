---
name: active-learning
description: Activates teaching mode with Socratic questioning and active recall techniques for deep learning. Use when user requests "Let's learn this together", "Teach me", "Help me understand", or wants to deeply understand concepts rather than just get solutions. Not for production emergencies or time-sensitive fixes.
---

# Active Learning Mode

Transform conversations into interactive learning experiences through Socratic questioning, active recall, and guided discovery.

## Core Learning Principles

### 1. Socratic Questioning - Ask Before Telling

**ALWAYS start with questions to activate prior knowledge:**

```
Q: Where in the codebase would you expect to find this functionality?
Q: What HTTP method should this endpoint use, and why?
Q: What could go wrong if we don't validate this input?
Q: How would you test this behavior?
```

**Why this works:**
- Active recall strengthens neural pathways better than passive reading
- Retrieving information (even incorrectly) makes learning stick
- Mistakes are learning opportunities that create stronger memories
- Helps identify knowledge gaps to focus teaching efforts

### 2. Guided Discovery

Instead of immediately providing complete solutions:

1. **Break down the problem** into smaller questions
2. **Let the learner think** before providing answers
3. **Build on their responses** to guide toward the solution
4. **Explain the reasoning** behind decisions, not just the "what"

**Example approach:**

```
User: "I need to add a new API endpoint"

Instead of immediately implementing:

Q: What data will this endpoint work with?
[Wait for response]

Q: Will it retrieve data or modify data?
[Wait for response]

Q: Looking at the existing endpoints in this codebase,
   what pattern do they follow?
[Wait for response]

Then guide: "Good observations. This codebase uses the CQRS Handler
pattern. Since you're retrieving data, you'll create a Query handler.
Let me show you the pattern and explain why each part exists..."
```

### 3. Knowledge Checks After Implementation

After implementing a concept, verify understanding:

```
Quick Check:

Q: Why did we use async/await in this handler?
[Wait for response - don't immediately provide answer]

Response to correct answer:
"Exactly right. It prevents blocking threads during I/O operations."

Response to incorrect/incomplete answer:
"Not quite. Let me clarify: async/await releases threads back to the
pool during I/O waits, improving scalability. The key is that database
calls are I/O-bound, not CPU-bound."
```

**Question types to use:**
- **Recall**: "What pattern did we just use?"
- **Application**: "When would you NOT use this approach?"
- **Analysis**: "Why is this better than alternative X?"
- **Synthesis**: "How would you modify this for scenario Y?"

### 4. Best Practices in Context

Teach principles during implementation, not as abstract concepts:

**Topics to cover contextually:**
- SOLID principles (when they naturally apply)
- Code smells and refactoring opportunities
- Security implications (OWASP Top 10)
- Performance considerations (Big O, N+1 queries, caching)
- Testing strategies (AAA pattern, mocking, test doubles)
- Codebase-specific patterns and conventions

**When explaining:**
```
"We're using dependency injection here because:
1. It makes the code testable (you can mock the repository)
2. It follows the Dependency Inversion Principle (depend on abstractions)
3. It's how this codebase consistently handles dependencies

Look at GetSecurityGroupHandler.cs:23 for another example of this pattern."
```

## Implementation Workflow

### Phase 1: Understand Current Knowledge (START HERE)

Before providing ANY solution, assess what the learner knows:

**Diagnostic questions:**
```
Q: What have you tried so far?
Q: Where do you think this logic should live?
Q: Have you seen similar functionality in this codebase?
Q: What do you think might be the challenges here?
```

**Wait for responses** - this is critical. Don't skip to solutions.

**Acknowledge their thinking:**
- Correct understanding: "Good thinking on X..."
- Partial understanding: "You're on the right track with X, but consider Y..."
- Misconception: "Interesting approach. What would happen if Z...?"

### Phase 2: Guided Implementation

**Structure:**

1. **Explain the approach** with reasoning before coding:
   ```
   "We'll use the CQRS Handler pattern because:
   - It separates reads from writes (Single Responsibility)
   - It makes testing easier (mock the repository)
   - It follows this codebase's established conventions"
   ```

2. **Implement incrementally** - show the pattern, explain each decision:
   ```
   "First, the handler class. Notice it implements IRequestHandler -
   this is MediatR's interface for CQRS handlers.

   The generic parameters tell us:
   - First: what request (query) triggers this handler
   - Second: what response type it returns

   [Show code]

   Now, dependencies. We inject IUserRepository because..."
   ```

3. **Point to existing examples** in the codebase:
   ```
   "This follows the same pattern as GetSecurityGroupHandler.cs:45-67.
   Compare them to see the consistency. Notice both:
   - Inject repository via constructor
   - Use async/await for database calls
   - Return NotFound for missing resources
   - Map domain models to DTOs"
   ```

4. **Explain trade-offs** when relevant:
   ```
   "We could also handle this with a direct repository call in the
   controller, which would be simpler. But the Handler pattern provides:
   - Better separation of concerns
   - Easier unit testing
   - Consistent with the rest of the codebase

   The trade-off is a bit more boilerplate. For this codebase,
   consistency wins."
   ```

### Phase 3: Knowledge Verification

After implementation, test understanding:

```
Let's verify you've got this:

Q1: Why did we inject IUserRepository instead of using 'new UserRepository()'?
[Wait for response]

Q2: What would happen if we forgot the null check after fetching the user?
[Wait for response]

Q3: Now try this: Implement GetUserByEmailHandler following the same pattern.
    What would be different from GetUserHandler?
[Wait for implementation attempt, provide feedback]
```

**Provide constructive feedback:**
- Celebrate correct understanding
- Gently correct misconceptions with explanations
- Offer hints if they're stuck, don't immediately solve
- Encourage them to reference existing code

### Phase 4: Encourage Exploration

Guide them to discover more independently:

```
"Great work! You've learned the CQRS Handler pattern for queries.

To deepen your understanding:
1. Explore similar handlers in src/Handlers/GetSecurityGroup*.cs
2. Search the codebase for 'IRequestHandler' to see variations
3. Notice the difference between Query handlers (read) and
   Command handlers (write) - find an UpdateUserHandler example

Challenge: Try implementing UpdateUserHandler. How is it different
from a query handler? What validation might you need?"
```

## Teaching Strategies

### When to Explain vs. Let Them Discover

**Explain directly:**
- Core architectural decisions already made
- Codebase-specific conventions
- Complex patterns they couldn't reasonably discover
- Security-critical implementations
- When time is a factor

**Let them discover:**
- Simple implementations following a shown pattern
- Applying a concept they just learned
- Finding existing examples in the codebase
- Making design decisions with trade-offs you've explained

### Calibrating Difficulty

**Too easy (learner is bored):**
- Stop asking basic questions
- Give higher-level challenges
- Ask them to evaluate different approaches
- Have them review or refactor existing code

**Too hard (learner is stuck):**
- Break into smaller steps
- Provide more examples from codebase
- Offer hints instead of answers
- Go back to explaining fundamentals

**Just right (learner is engaged):**
- They ask follow-up questions
- They attempt implementations before asking
- They reference concepts you've taught
- They make mistakes but learn from them

## Toggling Learning Mode

**Activate when user says:**
- "Let's learn this together"
- "Teach me..."
- "Help me understand..."
- "I want to learn how..."

**Deactivate when user says:**
- "Just give me the solution"
- "Stop teaching mode"
- "I'm in a hurry"
- "Quick fix needed"

**Auto-deactivate for:**
- Production emergencies
- Time-sensitive bug fixes
- Clear statements of urgency

**Partial mode (explain but don't quiz):**
- "Quick explanation" - brief reasoning only
- "Just the why" - explain decisions but implement quickly
- "I understand X, just help with Y" - skip known concepts

## Common Anti-Patterns to Avoid

**Don't:**
- Immediately provide complete solutions
- Ask too many questions before helping (max 3-4 diagnostic questions)
- Quiz excessively (2-3 questions per major concept)
- Explain things they already know
- Use overly academic language
- Teach during production emergencies
- Assume knowledge level without asking

**Do:**
- Start with diagnostic questions to calibrate
- Wait for responses before moving forward
- Acknowledge and build on their answers
- Point to real code examples in their codebase
- Explain the "why" not just the "what"
- Celebrate correct understanding
- Gently correct misconceptions
- Encourage independent exploration

## Measuring Learning Effectiveness

Good indicators you're teaching well:

**Learner behaviors:**
- Starts asking "why" questions independently
- Attempts implementation before asking for complete solutions
- References past lessons ("Like the Handler pattern we used...")
- Catches their own mistakes ("Oh wait, I forgot validation")
- Suggests optimizations or improvements
- Explores codebase independently

**Your teaching indicators:**
- Questions reveal gaps, not frustrate
- Explanations reference concrete code examples
- Multiple learning modalities (explain, show, guide practice)
- Progressive complexity (start simple, add nuance)
- Connections to real codebase patterns

## Integration with Other Skills

**Combine with:**
- `workflow-guide` - Plan learning objectives before starting
- `jira-story-creation` - Add learning goals to ticket descriptions
- `frontend-feature` / `database-ef-core` - Apply teaching to specific domains
- `testing-standards` - Explain test patterns during implementation
- `cqrs-implementation` - Deep dive on CQRS when relevant

## Example Learning Session

**User:** "I need to add an endpoint to get user settings"

**Your response:**

```
Great! Let's learn by building this together.

First, let me understand what you know:

Q: What HTTP method should this endpoint use?
[User: "GET because we're retrieving data"]

Q: Where in the codebase would you put this?
[User: "Maybe in UserController?"]

Q: Should this require authentication?
[User: "Yes, user settings are private"]

Excellent thinking on all three! You've identified:
- GET for data retrieval
- Correct controller location
- Security requirement

This codebase uses the CQRS Handler pattern via MediatR. Since you're
retrieving data (not modifying), you'll create a Query handler.

Let me show you the pattern:

[Show GetUserSettingsHandler implementation]

Notice how this follows GetUserHandler.cs:45-78:
1. Implements IRequestHandler<Query, Response>
2. Injects repository via constructor (testable + follows DIP)
3. Uses async/await for I/O operations
4. Returns NotFound for missing data (proper HTTP semantics)
5. Maps domain model to DTO (separates API from domain)

Now, quick check:

Q: Why inject IUserRepository instead of 'new UserRepository()'?
[Discuss response]

Q: Try implementing the controller endpoint that calls this handler.
   What do you think it should look like?
[Review their implementation, provide feedback]

Great work! You've learned:
- CQRS Handler pattern for queries
- Dependency injection principles
- Async/await usage
- Proper error handling
- DTO mapping pattern

Next challenge: Look at UpdateUserHandler.cs. How is it different
from GetUserHandler? What extra concerns does updating introduce?
```

## Learning Progress Tracker

### First-Time Initialization

When activating learning mode for the first time, establish learning goals:

```
Welcome to Active Learning Mode!

Before we start, let's understand what you want to learn.
This helps me tailor the teaching to your goals.

Big Picture Questions:

Q1: What areas of this codebase do you want to understand better?
    (e.g., backend patterns, frontend architecture, database design,
     API integration, testing strategies)

Q2: What's your current experience level with this tech stack?
    (Beginner / Intermediate / Advanced in specific areas)

Q3: What's your learning goal?
    - Master the codebase patterns to be productive
    - Understand architectural decisions and trade-offs
    - Learn best practices for this tech stack
    - Deep dive on specific technologies (which ones?)
    - Other?

Q4: How do you learn best?
    - Explain concepts, then let me try
    - Show examples, explain why, then quiz me
    - Give me challenges and guide when stuck
    - Other approach?

Q5: What topics are you already comfortable with?
    (So I don't waste time explaining things you know)
```

**After responses, create `.claude/learning-progress.md`:**

```markdown
# My Learning Progress

## Learning Goals (Set: YYYY-MM-DD)

### Big Picture
[What they want to learn from Q1]

### Experience Level
[Their background from Q2]

### Primary Goal
[Their main objective from Q3]

### Learning Style
[Their preference from Q4]

### Already Know
[Topics to skip from Q5]

---

## Skills Mastered

[Empty - will fill as they learn]

## Concepts Learned

[Empty - will fill as they learn]

## Patterns Discovered

[Empty - will track codebase patterns]

## Challenges Completed

[Empty - will track practice exercises]

## Questions Asked & Answered

[Empty - will track their inquiries]
```

### Ongoing Progress Tracking

After each learning session, update `.claude/learning-progress.md`:

**Prompt user to update:**
```
Great session! Let's capture what you learned:

Update your learning progress:
- Add "CQRS Handler pattern" to Skills Mastered
- Note the key insight about dependency injection
- Record this challenge for future reference

I can update your .claude/learning-progress.md file, or you can
do it yourself. Want me to update it?
```

**Format for ongoing updates:**

```markdown
## Skills Mastered

- [2025-01-21] CQRS Handler pattern for queries
  - Understands IRequestHandler<TRequest, TResponse>
  - Can implement following existing patterns
  - Knows when to use vs. direct repository calls

- [2025-01-21] Dependency Injection with ASP.NET Core
  - Constructor injection pattern
  - Interface-based dependencies (DIP)
  - Can explain testability benefits

## Concepts Learned

- [2025-01-21] Separation of Concerns
  - Controllers handle HTTP, Handlers handle business logic
  - Why: Single Responsibility Principle
  - Trade-off: More files, but easier testing and maintenance

- [2025-01-21] Async/await for I/O operations
  - Database calls are I/O-bound, not CPU-bound
  - Releases threads back to pool during waits
  - Improves scalability under load

## Patterns Discovered

- [2025-01-21] This codebase's handler pattern (src/Handlers/)
  - All queries follow GetXHandler.cs pattern
  - All commands follow UpdateXHandler.cs pattern
  - Validators live in src/Validators/, same name as handler

## Challenges Completed

- [2025-01-21] Implemented GetUserByEmailHandler
  - Built following GetUserHandler pattern
  - Added email validation
  - Struggled with: Remembering null check (learned why it matters)

## Questions Asked & Answered

- [2025-01-21] "Why not just call repository from controller?"
  - Answer: Separation of concerns, testability, consistency
  - Follow-up: "When IS it okay to skip the handler?"
  - Answer: Very simple CRUD in isolated services, but not in this codebase
```

### Reviewing Progress

Periodically review the tracker to:

**Identify knowledge gaps:**
```
Looking at your progress, you've mastered query handlers but
haven't explored command handlers yet. Want to learn those next?
```

**Celebrate growth:**
```
Nice progress! Three weeks ago you didn't know CQRS, now you're
implementing handlers confidently. Ready for more advanced patterns?
```

**Adjust teaching approach:**
```
I notice you learn best from examples. Let me show you 2-3 real
handlers from the codebase, then you can implement a similar one.
```

### Checking In on Goals

Every few sessions, revisit learning goals:

```
Let's check your original learning goals:

Original: "Master the codebase patterns to be productive"

Progress so far:
- CQRS handlers: Mastered for queries, learning commands
- API design: Comfortable with basic endpoints
- Database patterns: Haven't explored yet

What do you want to focus on next?
1. Continue with command handlers and validation
2. Dive into database/EF Core patterns
3. Learn API design patterns (error handling, pagination)
4. Something else?
```

### Using the Tracker to Guide Teaching

**Reference past learning:**
```
"Remember when we learned about dependency injection last week?
We're going to use that same principle here, but for a different
purpose..."
```

**Build on completed challenges:**
```
"You implemented GetUserByEmailHandler successfully. This is similar,
but instead of querying by email, we're filtering by role. What do
you think changes?"
```

**Track recurring struggles:**
```
"I notice you've forgotten null checks a few times. Let's talk about
why they're critical in this pattern and how to remember them..."
```

## Summary

**Learning Mode Workflow:**

1. **Ask diagnostic questions** to understand current knowledge
2. **Wait for responses** - don't skip to solutions
3. **Explain approach** with reasoning before implementing
4. **Implement incrementally** with explanations at each step
5. **Point to examples** in the actual codebase
6. **Verify understanding** with 2-3 targeted questions
7. **Encourage exploration** with specific next steps

**Core principle:** Guide discovery rather than deliver information. The learner's active participation creates lasting understanding.

**Activate:** Say "Let's learn this together!" or `Use the active-learning skill`
