# ViewComponent Patterns

Reference for creating ViewComponents in Artemis.

## File Structure

```
app/components/
└── {namespace}/
    ├── {component}.rb              # Ruby class
    ├── {component}.html.erb        # Main template
    └── {component}/                # Nested components (optional)
        ├── {nested}.html.erb
        └── ...
```

## Basic Component

```ruby
# app/components/ui/card.rb
module UI
  class Card < ViewComponent::Base
    def initialize(title:, variant: :default)
      @title = title
      @variant = variant
    end

    private

    def variant_class
      case @variant
      when :primary then "card-primary"
      when :secondary then "card-secondary"
      else "card-default"
      end
    end
  end
end
```

```erb
<%# app/components/ui/card.html.erb %>
<div class="card <%= variant_class %>">
  <h3 class="card-title"><%= @title %></h3>
  <div class="card-body">
    <%= content %>
  </div>
</div>
```

## Slots Pattern

Use `renders_one` for single slots, `renders_many` for collections:

```ruby
module UI
  class Modal < ViewComponent::Base
    renders_one :header, ->(title: nil, subtitle: nil, &block) {
      ModalHeader.new(title: title, subtitle: subtitle, &block)
    }
    renders_one :body
    renders_one :footer, ->(**args, &block) {
      ModalFooter.new(**args, &block)
    }

    def initialize(title: nil, size: :md)
      @title = title
      @size = size
    end
  end
end
```

Usage:

```erb
<%= render UI::Modal.new(title: 'Edit') do |modal| %>
  <% modal.with_body do %>
    <p>Body content</p>
  <% end %>
  <% modal.with_footer do %>
    <button class="btn">Save</button>
  <% end %>
<% end %>
```

## Nested Components

For complex components, nest component classes inside the parent:

```ruby
# app/components/ui/modal.rb
module UI
  class Modal < ViewComponent::Base
    # Main component code...

    class ModalHeader < ViewComponent::Base
      def initialize(title: nil, subtitle: nil, closable: true)
        @title = title
        @subtitle = subtitle
        @closable = closable
      end
    end

    class ModalFooter < ViewComponent::Base
      def initialize(align: :end)
        @align = align
      end

      def alignment_class
        case @align
        when :between then "justify-between"
        when :start then "justify-start"
        else "justify-end"
        end
      end
    end
  end
end
```

Templates go in subdirectory:
- `app/components/ui/modal/modal_header.html.erb`
- `app/components/ui/modal/modal_footer.html.erb`

## Stimulus Integration

Add data attributes via `stimulus_data` helper method:

```ruby
def stimulus_data
  {
    'data-controller': 'dialog-modal',
    'data-dialog-modal-closable-value': @closable,
    'data-action': 'turbo:submit-end->dialog-modal#handleSubmit'
  }
end
```

**Important:** Use string keys with `'data-'` prefix. `tag.attributes` does NOT auto-prefix.

```erb
<div <%= tag.attributes(stimulus_data) %>>
  ...
</div>
```

## Turbo Frame Integration

For modal/overlay patterns:

```ruby
class Modal < ViewComponent::Base
  include Turbo::FramesHelper

  # In template:
  # <%= turbo_frame_tag :modal, target: :_top do %>
  #   ...
  # <% end %>
end
```

## Size Variants Pattern

```ruby
SIZE_CLASSES = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-3xl',
  full: 'max-w-4xl'
}.freeze

def size_class
  SIZE_CLASSES.fetch(@size, SIZE_CLASSES[:md])
end
```

## Testing Components

```ruby
# test/components/ui/modal_test.rb
class UI::ModalTest < ViewComponent::TestCase
  include Turbo::FramesHelper

  def with_current_person(person = nil, &block)
    Current.set(person: person, &block)
  end

  describe "rendering" do
    it "renders with title" do
      with_current_person do
        render_inline(UI::Modal.new(title: 'Test'))
        assert_selector '.modal-title', text: 'Test'
      end
    end
  end
end
```

## Common Gotchas

1. **Namespace conflicts** - Use `UI::` not `Stage::` when `Stage` is also a model
2. **Missing formats** - Add `formats: [:html]` when rendering HTML partials from turbo_stream
3. **Both view files** - Check for both `.html.erb` and `.turbo_stream.erb` when migrating
