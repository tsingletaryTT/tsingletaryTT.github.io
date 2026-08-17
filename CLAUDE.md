# tsingletaryTT.github.io

Taylor Singletary's personal site — "Everything Taylor Singletary does for Tenstorrent."
Jekyll on GitHub Pages, served at https://tsingletarytt.github.io.

## Shape of the repo

* `index.md` — the whole homepage: hero, **Selected Work**, **Contributing To**, and a
  three-post **Writing** preview. It's all Liquid over data files; there is no per-project
  page.
* `_data/projects.yml` — drives Selected Work. One entry per project:
  `name`, `lang` (free-text, e.g. `Python · MCP server`), `desc` (folded block scalar),
  `url` (GitHub), and optional `site` (a live GitHub Pages demo → renders a "Live site" link).
  **Order is editorial, not chronological** — newest/most substantial first.
* `_data/contributions.yml` — the Contributing To grid; `repo: org/name` only, rendered by
  splitting on `/`.
* `_layouts/{default,post}.html`, `assets/css/style.css` — dark editorial hybrid design.
* `_posts/` — writing archive, surfaced by `writing.md`. Permalinks are `/writing/:y/:m/:d/:title/`.

## Local build caveat (as of 2026-08-17)

`bundle exec jekyll build` **does not run on this Mac**. The pinned toolchain is Jekyll 3.9
(via the `github-pages` gem), and neither installed Ruby works:

* system Ruby 2.6 — too old for the `bundler 4.0.3` pin in `Gemfile.lock`
* Homebrew Ruby 4.0.1 (the only Cellar version, despite `ruby@3.4` symlinks) — too new;
  Jekyll 3.9 crashes on it

GitHub Pages builds on its own Ruby, so this only blocks local preview. To sanity-check a
data-file change without a full build, render the Liquid loop directly against the YAML:

```bash
GEM_HOME=/tmp/gems gem install liquid --no-document
GEM_HOME=/tmp/gems ruby -ryaml -rliquid -e '
  tpl = Liquid::Template.parse(File.read("index.md")[/{% for project.*?{% endfor %}/m])
  puts tpl.render!("site" => {"data" => {"projects" => YAML.load_file("_data/projects.yml")}})'
```

(Use a current `liquid` — the 4.0.3 that ships with Homebrew Ruby calls `String#tainted?`,
removed in Ruby 3.2+, and every variable renders as `Liquid error: internal`.)

Installing a real Ruby 3.x would fix the build properly; nobody has done it yet.

## What happened

**2026-08-17 — add latest public repos.** Prompt: *"Let's update this repo to include my
latest public repos on tsingletaryTT, tt-tnt, tt-boltz-demo, tt-gozer — missing any others?"*

* **`tt-boltz-demo` doesn't exist.** The repo is **`tt-bio-demo`**; the "boltz" association is
  real but upstream — it wraps [`moritztng/tt-bio`](https://github.com/moritztng/tt-bio), which
  runs Boltz-2 (among other models) on Tenstorrent hardware. A follow-up prompt asked for that
  connection to be explicit *in the description*, not just implied by the name, so the desc now
  names both the upstream repo and Boltz-2.
* Answering "missing any others?" — diffed all public non-fork, non-archived repos against
  `projects.yml` and found **`tt-demo-maker`** also absent; added it alongside the three asked
  for. Descriptions were written from each repo's actual README, not from the GitHub blurb.
* **`tt-zork-and-more` belongs in the list** — added on Taylor's correction: *"it's a fork but
  not really."* GitHub marks it a fork of `historicalsource/zork1`, which is only where the
  original 1977 source came from; everything on top (the three-stage Blackhole port, the
  RISC-V Z-machine kernel, the LLM remix layer) is original work. **Don't filter this repo
  list by `isFork` alone** — check what the fork actually contains.
* **`tt-cli` removed** at Taylor's request (it had been on the list since `cd18109`). No reason
  given, so don't re-add it from a repo-diff sweep — its absence is intentional.
* Deliberately **left out**, as outside "latest": `tt-jukebox` (Jan 2026). Also skipped: this
  site's own repo, the archived `tt-local-generator` / `tt-toplike-rs` (both moved to the
  `tenstorrent` org and already listed under Contributing To), and genuine upstream forks
  where the work isn't Taylor's (freeciv, freeciv-web, tt-studio, tt-top, analyze_synths,
  tt-installer-gentoo).
