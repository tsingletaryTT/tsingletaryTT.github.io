#!/usr/bin/env ruby
# Liquid preflight for the GitHub Pages build.
#
# jekyll-optional-front-matter (bundled with github-pages) makes EVERY .md file a page and
# renders Liquid in it, fenced code blocks included. A markdown file that merely *quotes* a
# Liquid tag will fail the remote build — which is exactly how CLAUDE.md broke it once.
# Jekyll 3.9 will not run on this Mac, so this parses every file Jekyll would render and
# reports syntax errors locally.
#
#   GEM_HOME=/tmp/gems gem install liquid --no-document
#   GEM_HOME=/tmp/gems ruby script/preflight.rb
require "yaml"
require "liquid"

# Plain Liquid doesn't know Jekyll's own tags or the plugin tags github-pages loads, so
# register no-op stubs. Without these, a perfectly valid {% seo %} reads as a syntax error
# and drowns out the real ones.
NOOP_TAGS  = %w[seo feed_meta gist highlight endhighlight avatar]
BLOCK_TAGS = %w[highlight]
ENVIRONMENT = Liquid::Environment.build do |env|
  (NOOP_TAGS - BLOCK_TAGS).each do |name|
    env.register_tag(name, Class.new(Liquid::Tag) { def render(_ctx) = "" })
  end
  BLOCK_TAGS.each do |name|
    env.register_tag(name, Class.new(Liquid::Block) { def render(_ctx) = "" })
  end
end

config   = YAML.load_file("_config.yml")
excluded = Array(config["exclude"])

def excluded?(path, patterns)
  patterns.any? { |p| p.end_with?("/") ? path.start_with?(p) : path == p }
end

candidates = Dir.glob("**/*.{md,markdown,html}").reject do |f|
  f.start_with?("_site/", "vendor/", "node_modules/") || excluded?(f, excluded)
end

failures = []
candidates.sort.each do |file|
  begin
    Liquid::Template.parse(File.read(file), environment: ENVIRONMENT)
    puts "  ok    #{file}"
  rescue Liquid::SyntaxError => e
    puts "  FAIL  #{file} — #{e.message}"
    failures << file
  end
end

puts
if failures.empty?
  puts "Liquid preflight passed (#{candidates.size} files Jekyll would render)."
else
  puts "Liquid preflight FAILED for: #{failures.join(', ')}"
  puts "Either wrap the offending tags in raw/endraw, or add the file to `exclude` in _config.yml."
  exit 1
end
