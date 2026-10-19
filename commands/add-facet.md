# add-facet

Add a new search facet to the person search system

## Arguments
- `$ARGUMENTS` - Name of the facet (e.g., `seniority`, `location`, `skills`)

## What This Does

Creates a new search facet following the established pattern. Facets filter search results based on specific criteria.

## Steps I Will Take

### 1. Create the Facet Class

Location: `packs/search/app/public/search/facets/{name}.rb`

```ruby
# frozen_string_literal: true

module Search
  module Facets
    class {ClassName} < Facet
      source :local  # or :data_universe for DU-powered facets

      def build_query
        return if value.blank?

        BooleanQuery.new.must(
          { terms: { {field_name}: value } },
        )
      end
    end
  end
end
```

### 2. Register the Facet

Edit `packs/search/app/public/search/facet_registry.rb`:

```ruby
Search::FacetRegistry.register(:person) do
  # ... existing facets ...
  facet :{name}, Search::Facets::{ClassName}
  # Use `multiple: true` for array-of-objects facets like employments
end
```

### 3. Add to OpenSearch Index (if needed)

If the facet requires a new field in the search index:

1. Add field to person mapping in `packs/search/app/services/search/person_index.rb`
2. Add field population in `packs/search/app/services/search/person_document.rb`
3. Run reindex: `bin/rails opensearch:reindex`

## Pattern Reference

**Simple facet (single value):**
```ruby
class Groups < Facet
  source :local

  def build_query
    return if value.blank?
    BooleanQuery.new.must({ terms: { group_ids: value } })
  end
end
```

**Multiple facet (array of objects):**
```ruby
class Employment < Facet
  source :local

  def build_query
    return if value.blank?

    nested_queries = value.filter_map do |filter|
      build_nested_query(filter)
    end

    BooleanQuery.new.must(*nested_queries)
  end
end
```

**Facet with custom validation:**
```ruby
def build_query
  return if value.blank?
  return unless valid_values.include?(value)

  BooleanQuery.new.must(...)
end
```

## Existing Facets to Reference

| Facet | Type | File |
|-------|------|------|
| Query | Text search | `facets/query.rb` |
| Groups | ID filter | `facets/groups.rb` |
| Lists | ID filter | `facets/lists.rb` |
| ConnectedTo | ID filter | `facets/connected_to.rb` |
| Employment | Nested multiple | `facets/employment.rb` |
| CandidateSegment | Enum filter | `facets/candidate_segment.rb` |

## Testing

Add tests in `packs/search/test/public/search/facets/{name}_test.rb`:

```ruby
# frozen_string_literal: true

require "test_helper"

module Search
  module Facets
    class {ClassName}Test < ActiveSupport::TestCase
      describe "{ClassName}" do
        it "builds query with valid value" do
          facet = {ClassName}.new(["value1", "value2"])
          query = facet.build_query

          assert_equal({ terms: { {field}: ["value1", "value2"] } }, query.to_h[:bool][:must].first)
        end

        it "returns nil for blank value" do
          facet = {ClassName}.new(nil)
          assert_nil facet.build_query
        end
      end
    end
  end
end
```

## Usage Example

```bash
/add-facet seniority
```

I will:
1. Create `packs/search/app/public/search/facets/seniority.rb`
2. Register in `facet_registry.rb`
3. Create test file
4. Explain any index changes needed
