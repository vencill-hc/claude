# Lookbook Preview Reference

Lookbook provides visual documentation for ViewComponents at `/lookbook` in development.

## Creating Previews

### ⚠️ MANDATORY: Use the Generation Script

**ALWAYS start with the generation script:**

```bash
ruby .claude/skills/frontend-developer/scripts/generate_lookbook_preview.rb UI::Modal
```

This ensures correct structure, naming, and boilerplate. Customize the output as needed.

**Common mistakes when creating previews manually:**
- Using `render_inline` instead of `render` (causes "undefined method" error)
- Wrong file location or naming convention
- Missing rubocop-required trailing commas
- Using double quotes instead of single quotes

### File Structure

```
test/components/previews/
└── {namespace}/
    └── {component}_preview.rb
```

Example: `UI::Modal` → `test/components/previews/ui/modal_preview.rb`

### Basic Preview Class

```ruby
# frozen_string_literal: true

module UI
  class ModalPreview < ViewComponent::Preview
    # @label Default
    # @display bg_color "#f5f5f5"
    def default
      render UI::Modal.new(title: 'Modal Title') do |modal|
        modal.with_body do
          '<div class="modal-body-padding"><p>Body content.</p></div>'.html_safe
        end
      end
    end
  end
end
```

## Annotations

| Annotation | Purpose | Example |
|------------|---------|---------|
| `@label` | Display name in sidebar | `@label With Icon` |
| `@display bg_color` | Preview background color | `@display bg_color "#f5f5f5"` |
| `@param` | Interactive parameter control | `@param title text "Default Title"` |
| `@hidden` | Hide from sidebar | `@hidden true` |

### Parameter Types

```ruby
# Text input
# @param title text "Enter title"

# Select dropdown
# @param size select { choices: [sm, md, lg] }

# Toggle
# @param closable toggle

# Number
# @param count number
```

## Standard Variants

For most components, include these preview methods:

1. **`default`** - Minimal required params
2. **`with_{slot}`** - Each slot demonstrated
3. **Size variants** - `small`, `medium`, `large` if applicable
4. **State variants** - `loading`, `disabled`, `error` if applicable
5. **Edge cases** - Long content, empty states, etc.

## Configuration

Lookbook configuration in `config/initializers/lookbook.rb`:

```ruby
if Rails.env.development?
  Rails.application.config.lookbook.preview_controller = 'LookbookPreviewController'
  Rails.application.config.lookbook.preview_layout = 'component_preview'
  Rails.application.config.view_component.default_preview_layout = 'component_preview'
  Rails.application.config.view_component.preview_paths = [Rails.root.join('test/components/previews')]
end
```

## Preview Layout

The preview layout at `app/views/layouts/component_preview.html.erb` must include:

- CSS stylesheets (`tailwind`, `application`)
- JavaScript (`javascript_importmap_tags`)
- Turbo frame tag if using modals: `<%= turbo_frame_tag :modal %>`

## Troubleshooting

### Preview not appearing
- Restart dev server after creating first preview
- Verify namespace matches: `UI::ModalPreview` for `UI::Modal`
- Check `preview_paths` configuration

### Assets not loading
- Ensure `component_preview.html.erb` includes all asset tags
- Clear asset cache: `rm -rf public/assets tmp/cache`

### Turbo Frame components
- Add `<%= turbo_frame_tag :modal %>` to preview layout
- Ensure Stimulus controllers are loaded via importmap
