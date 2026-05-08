#!/usr/bin/env ruby
# frozen_string_literal: true

# Generate a Lookbook preview for a ViewComponent
#
# Usage: ruby generate_lookbook_preview.rb UI::Modal
#        ruby generate_lookbook_preview.rb modal (infers UI:: namespace)

require 'fileutils'

def generate_preview(namespace, name, component_class)
  <<~RUBY
    # frozen_string_literal: true

    module #{namespace}
      class #{name}Preview < ViewComponent::Preview
        # @label Default
        # @display bg_color "#f5f5f5"
        def default
          render #{component_class}.new do |component|
            # TODO: Configure component slots
          end
        end

        # Add more preview variants below:
        #
        # # @label With Footer
        # # @display bg_color "#f5f5f5"
        # def with_footer
        #   render #{component_class}.new do |component|
        #     component.with_footer do
        #       # footer content
        #     end
        #   end
        # end
        #
        # # @label Small Size
        # # @display bg_color "#f5f5f5"
        # def small
        #   render #{component_class}.new(size: :sm) do |component|
        #     # content
        #   end
        # end
      end
    end
  RUBY
end

def main
  component_name = ARGV[0]
  unless component_name
    puts 'Usage: ruby generate_lookbook_preview.rb <ComponentName>'
    puts '  e.g., ruby generate_lookbook_preview.rb UI::Modal'
    exit 1
  end

  # Normalize component name
  if component_name.include?('::')
    namespace, name = component_name.split('::')
  else
    namespace = 'UI'
    name = component_name.split('_').map(&:capitalize).join
  end

  # Build paths
  preview_dir = File.join('test', 'components', 'previews', namespace.downcase)
  preview_file = File.join(preview_dir, "#{underscore(name)}_preview.rb")
  component_class = "#{namespace}::#{name}"

  # Check if component exists
  component_file = File.join('app', 'components', namespace.downcase, "#{underscore(name)}.rb")
  unless File.exist?(component_file)
    puts "Warning: Component file not found at #{component_file}"
    puts 'Generating preview anyway...'
  end

  # Create directory
  FileUtils.mkdir_p(preview_dir)

  # Generate preview content
  content = generate_preview(namespace, name, component_class)

  # Write file
  if File.exist?(preview_file)
    puts "Preview already exists at #{preview_file}"
    print 'Overwrite? (y/N): '
    answer = $stdin.gets.chomp.downcase
    exit 0 unless answer == 'y'
  end

  File.write(preview_file, content)
  puts "Created: #{preview_file}"
  puts "\nView at: http://localhost:3000/lookbook/inspect/#{namespace.downcase}/#{underscore(name)}"
end

def underscore(str)
  str.gsub(/([A-Z])/) { "_#{Regexp.last_match(1).downcase}" }.sub(/^_/, '')
end

main if __FILE__ == $PROGRAM_NAME
