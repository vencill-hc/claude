---
name: rails-dev
description: Write Rails code following Artemis project conventions and best practices. Use when implementing Rails features, creating controllers/models/services/views, adding ViewComponents, implementing Turbo/Hotwire features, or writing Rails tests.
---

# Rails Development

## Core Principles

**Always follow these rules:**
1. **Simplest solution first** - Don't add complexity until proven necessary
2. **Controllers are thin** - Move business logic to service objects
3. **Database-first** - Check DB for fresh data before expensive operations
4. **Prevent N+1** - Use `.includes()` for associations, filter in memory
5. **Test everything** - Add tests for all new functionality (Minitest::Spec)
6. **Turbo over JavaScript** - Prefer Hotwire/Turbo to custom JS
7. **Security by default** - Never use `.html_safe` without sanitization
8. **Use DaisyUI components** - Always use DaisyUI component classes for UI consistency

## Implementation Workflow

### 1. Before Writing Code
- Search for existing functionality (components, services, helpers)
- Check if similar patterns exist in the codebase
- Plan minimal file changes - only modify what's necessary
- Read domain-specific CLAUDE.md files in affected directories

### 2. Controllers (Keep Thin)
```ruby
# BAD - logic in controller
def create
  if contact.restricted?
    redirect_to root_path, alert: "Restricted"
  elsif some_other_condition?
    # more logic...
  end
end

# GOOD - use service object
def create
  result = ContactService.new(contact).process_overrides(reason)
  redirect_to result.path, notice: result.message
end
```

### 3. Service Layer

**Database-first pattern:**
```ruby
class CandidateService
  def sync_data
    # Check DB first, avoid expensive operations
    return if candidate.synced_recently?

    # Do expensive operation
    external_api.fetch_data
  end
end
```

### 4. ViewComponents

**Namespace to avoid conflicts:**
```ruby
# app/components/stage_components/card_component.rb
module StageComponents
  class CardComponent < ViewComponent::Base
    def initialize(stage:)
      @stage = stage
    end

    private

    def render?
      @stage.present?
    end
  end
end
```

**Component rules:**
- Namespace to avoid Rails model conflicts
- `render?` method determines visibility
- Don't wrap content in `<% if render? %>`

### 5. Background Jobs (Sidekiq)

```ruby
class MyJob < ApplicationJob
  queue_as :default  # Always use :default

  def perform(id)
    sleep(30) if dealing_with_rate_limits
  end
end
```

### 6. Turbo/Hotwire

**Prefer Turbo streams over JS:**
```ruby
# app/views/candidates/update.turbo_stream.erb
<%= turbo_stream.replace "candidate_#{@candidate.id}" do %>
  <%= render @candidate %>
<% end %>
```

### 7. Preventing N+1 Queries

```ruby
# BAD
candidates.each { |c| c.contacts.each { |x| ... } }

# GOOD
candidates.includes(:contacts).each { |c| c.contacts.each { |x| ... } }
```

### 8. Testing (Minitest::Spec)

```ruby
class MyServiceTest < ActiveSupport::TestCase
  describe "processing" do
    it "processes valid data" do
      service = MyService.new(resource)
      assert service.process
    end
  end
end
```

## Artemis-Specific Patterns

### Bucket/Recording/Recordable
- Bucket: Container (Project, Playbook, Group, ContactList)
- Recording: Wrapper with status, position, parent/child
- Recordable: Actual content (Candidate, Stage, Task, etc.)
- Use `bucket.record()` to create, query through `bucket.recordings`

### Person/Contact/User
- Users have TWO Person records (User + Contact personable)
- Use `user.contact.person` for networking connections
- Never use User persons for connections

### AI/Cache Pattern
```ruby
cache_key = "ai_response:model:#{model}:prompt_hash:#{Digest::MD5.hexdigest(prompt)}"
Rails.cache.fetch(cache_key) { OpenAI.complete(prompt) }
```

### Packwerk Boundaries
- Respect package boundaries (packs/people, packs/search, etc.)
- Run `bin/packwerk check` to verify

## DaisyUI Components

Always use DaisyUI classes:
```erb
<button class="btn btn-primary">Primary</button>
<span class="badge badge-success">Active</span>
<input type="text" class="input" placeholder="Text">
```

## Checklist Before Committing

- [ ] Controllers are thin (< 10 lines per action)
- [ ] Business logic in service objects
- [ ] No N+1 queries (use `.includes()`)
- [ ] Tests added (Minitest::Spec format)
- [ ] No `.html_safe` without sanitization
- [ ] ViewComponents namespaced
- [ ] Turbo used instead of custom JS where possible
- [ ] DaisyUI component classes used
- [ ] Ran `bin/rails test path/to/test.rb`
- [ ] Ran `bin/rubocop -a`

## Commands

```bash
bin/rails test                    # All tests
bin/rails test path/test.rb:42    # Specific line
bin/rubocop -a                    # Auto-fix style
bin/packwerk check                # Check boundaries
bin/dev                           # Start server
```
