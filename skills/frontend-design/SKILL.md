---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build ViewComponents, pages, or interfaces. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Tech Stack

This codebase uses:
- **Rails 8.0** with **Hotwire** (Turbo + Stimulus)
- **Tailwind CSS** for styling
- **ViewComponents** for reusable UI (`app/components/`)
- **Stimulus controllers** (`app/javascript/controllers/`)
- **Import maps** (no npm/webpack build step)
- **@floating-ui/dom** for popovers and positioning
- **ERB templates** with Turbo Frames/Streams

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (ViewComponents, ERB, Tailwind, Stimulus) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Use a **monochromatic (grayscale) palette** as the foundation. There is NO standard accent color for general UI elements. The DaisyUI `primary` color is reserved ONLY for primary CTAs and critical attention moments. Use `bg-base-100/200/300`, `text-base-content`, and `border-base-300` for standard UI. Semantic colors (`success`, `error`, `warning`) should only be used for their intended meaning.
- **Motion**: Use CSS animations and Tailwind's transition utilities for effects and micro-interactions. For orchestrated sequences, use Stimulus controllers with `animation-delay` and CSS keyframes. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use Turbo Frame transitions and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

### Color Constraints (CRITICAL)

**DO NOT** use accent colors (`primary`, `secondary`, `accent`) for:
- Navigation active states → Use `bg-base-300 font-semibold`
- Tab selections → Use grayscale
- Data-driven pills/tags → Use monochromatic variants
- Icons → Use `text-base-content/60`
- Loading spinners → Use `text-base-content/60`
- Form focus rings → Use `focus:ring-base-300`
- Borders/highlights → Use `border-base-300`

**DO** use DaisyUI `primary` (`btn-primary`) for:
- Primary CTA buttons (Save, Submit, Continue)
- Critical badges requiring immediate attention

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly accent colors used liberally, gradients, or colored highlights), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.