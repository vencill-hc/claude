---
name: frontend-developer
description: Implementation toolkit for frontend development. Use when building ViewComponents, Stimulus controllers, or UI features. Provides patterns, scripts, and documentation workflows. For design guidance, invoke the frontend-design skill first.
---

# Frontend Developer Toolkit

Implementation resources for building production-ready frontend code in Artemis.

## When to Use

- Implementing ViewComponents from design specs
- Creating Stimulus controllers for interactivity
- Adding Lookbook previews for documentation
- Following established patterns and conventions

## Design vs Implementation

This skill handles **implementation**. For aesthetic direction:
1. Invoke the `frontend-design` skill first to get design guidance
2. Return here for implementation patterns and scripts

## Quick Reference

### ViewComponents

**Location:** `app/components/{namespace}/`

**Structure:**
```
app/components/ui/
├── modal.rb                    # Ruby class with slots
├── modal.html.erb              # Main template
└── modal/                      # Nested component templates
    ├── modal_header.html.erb
    └── modal_footer.html.erb
```

**Key patterns:** See [references/viewcomponent-patterns.md](references/viewcomponent-patterns.md)

### Stimulus Controllers

**Location:** `app/javascript/controllers/`

**Naming:** `{feature}_controller.js` → `data-controller="{feature}"`

**Data attributes:** Use explicit `'data-controller':` keys, NOT `controller:` (tag.attributes doesn't auto-prefix)

### CSS

**Complex styles:** `@layer components` in `app/assets/tailwind/application.css`
**Simple styles:** Tailwind utilities inline

### Lookbook Previews

**Location:** `test/components/previews/{namespace}/{component}_preview.rb`

**⚠️ MANDATORY: Always use the generation script:**
```bash
ruby .claude/skills/frontend-developer/scripts/generate_lookbook_preview.rb UI::Modal
```

**NEVER create preview files manually from scratch.** The script ensures:
- Correct file location and naming
- Proper `render` method usage (NOT `render_inline`)
- Rubocop-compliant boilerplate
- Standard annotations (`@label`, `@display bg_color`)

After running the script, customize the generated preview as needed.

**Full reference:** See [references/lookbook-previews.md](references/lookbook-previews.md)

## Bundled Resources

### References

| File | Purpose |
|------|---------|
| [viewcomponent-patterns.md](references/viewcomponent-patterns.md) | Component structure, slots, nesting, Stimulus integration |
| [lookbook-previews.md](references/lookbook-previews.md) | Creating visual documentation previews |

### Scripts

| Script | Purpose |
|--------|---------|
| [generate_lookbook_preview.rb](scripts/generate_lookbook_preview.rb) | Scaffold a Lookbook preview for a component |

## Common Gotchas

1. **Data attributes** - `tag.attributes` doesn't auto-prefix `data-`, use `'data-controller':` explicitly
2. **Dual view files** - Both `.html.erb` and `.turbo_stream.erb` may exist for same action
3. **Asset caching** - Clear with `rm -rf public/assets tmp/cache` if changes don't appear
4. **Lookbook config** - Use `=` not `<<` for `preview_paths` (it may be nil)
5. **Namespace conflicts** - Use `UI::` not `Stage::` when `Stage` is also a model

## Workflow

1. **Get design** - Invoke `frontend-design` skill if aesthetic guidance needed
2. **Implement component** - Follow [viewcomponent-patterns.md](references/viewcomponent-patterns.md)
3. **Add Lookbook preview** - Use script or follow [lookbook-previews.md](references/lookbook-previews.md)
4. **Write tests** - Delegate to `test-writer` agent
