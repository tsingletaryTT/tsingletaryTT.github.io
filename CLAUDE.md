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
  Every entry also carries a figure: `media` (path under `assets/img/projects/`),
  `media_kind` (`clip` · `shot` · `card` · `chart`), `media_alt`, `media_note`, and
  `poster` for clips. Generators for the `card` and `chart` kinds are described below.
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

**2026-08-17 — the tenstorrent-org projects are Taylor's work, not "contributions."** Prompt:
*"include the repos I contribute heavily to from tenstorrent too. tt-vscode-toolkit,
tt-local-generator, tt-toplike, tt-animatediff, tt-quietbox2-guide are all essentially
one-person-projects: me."*

Verified before moving them, via `repos/tenstorrent/<repo>/contributors` — he is
**105/109, 291/293, 54/57, 9/10 and 112/114** commits respectively; everything else is
drive-by commits, Copilot, and bots. So all five became full `projects.yml` entries with
figures, and the three that had been sitting under **Contributing To were removed from
`contributions.yml`** — listing them there framed his own projects as somebody else's.

**The rule now written at the top of `contributions.yml`:** ownership follows authorship, not
the GitHub org. A repo under `tenstorrent/` still belongs in `projects.yml` when Taylor
effectively wrote it. `tt-awesome` moved across on a follow-up prompt — *"put tt-awesome here
too, but not tt-kernel-package-manager"* — and it belongs in Selected Work for exactly the same
reason: the 151 entries are the community's, but the JSON schema, the generator, the Eleventy
site and the submission flow are all his.

**Contributing To is now empty and hidden.** `tt-kernel-package-manager` was the last entry and
Taylor asked for it gone, so `contributions.yml` holds only comments. Removing the entry alone
would have left a section label above an empty grid, so `index.md` wraps that section in
`{% raw %}{% if site.data.contributions and site.data.contributions.size > 0 %}{% endraw %}` —
it disappears while the file is empty and returns by itself when an entry is added. A
comments-only YAML file loads as `false` under this Psych, and the guard is tested against
`false`, `nil` and `[]`.

Ordering: the four largest org projects lead Selected Work, with `tt-animatediff` slotted
beside the other generative work rather than at the top. That is an editorial call, easy to
change by reordering the file.

For `tt-quietbox2-guide` there was no usable asset in the repo — it *is* a website — so its
figure is a headless-Chrome screenshot of the published guide at docs.tenstorrent.com. Also
note `<video loop>` already repeats a clip, so don't `-stream_loop` a short GIF when
transcoding: doing that to tt-animatediff's 1.9-second loop made a 3.7 MB file where 422 KB
does the same job.

**2026-08-17 — the CLAUDE.md in this repo broke the Pages build once.** Worth knowing before
you add any markdown here. `github-pages` loads **jekyll-optional-front-matter**, which makes
every `.md` file a page and renders Liquid inside it — **fenced code blocks do not protect
Liquid tags**. Because the local-preview recipe above quotes a `for` tag, adding CLAUDE.md
failed the remote build with `Syntax Error in 'for loop'`, and the site silently kept serving
the previous deploy.

Two things now guard against it:

* `_config.yml` **excludes `CLAUDE.md` and `.claude/`** — internal notes were never meant to
  be published pages anyway. Don't remove those lines.
* **`script/preflight.rb`** parses every file Jekyll would render and fails on Liquid syntax
  errors, which is the one class of breakage that can't be caught locally (Jekyll 3.9 doesn't
  run on this Mac). Run it before pushing:

      GEM_HOME=/tmp/gems gem install liquid --no-document
      GEM_HOME=/tmp/gems ruby script/preflight.rb

**Also: the Pages API lies about failures.** `gh api .../pages/builds/latest` reported
`status: building` for seven hours after the build had already failed in 32 seconds. Trust the
Actions run instead — `gh run list` and `gh run view <id> --log-failed`.

**2026-08-17 — a visual for every project.** Prompt: *"include something visual from each repo
mentioned. there are goodies with all of them to highlight here."*

Every one of the 16 entries now carries a figure. `projects.yml` gained five optional keys —
`media`, `poster` (clips only), `media_kind`, `media_alt`, `media_note` — and `index.md`
renders them as a `<figure>`. Four kinds, because the repos have four kinds of goodie:

* **`clip`** (5) — `<video autoplay loop muted playsinline>`. Source GIFs/MP4s were
  transcoded to H.264, which is *far* smaller than a GIF: tt-demo-maker's 5.5 MB ouroboros
  GIF became a 1.8 MB MP4. Posters are pulled from **mid-clip**, not frame 1 — several
  first frames are an empty terminal.
* **`shot`** (4) — screenshots as WebP, plus two SVGs that were already vector.
* **`card`** (6) — for the CLI/TUI repos that ship **no images at all** (tt-gozer, tt-warp,
  tt-model-runner, tt-qb-lights, tt-developer-image, tt-claw). Generated SVG "terminal
  cards" from output and diagrams lifted **verbatim** out of each README. Two gotchas:
  leading must be ~1.23× the font size or box-drawing verticals render as dashes, and
  several READMEs' box art is off by a character, so the generator pads before the trailing
  border to square up the right edge (text untouched).
* **`chart`** (1) — tt-tnt has no images but does have `docs/measurements/`, so its figure is
  a per-source loss chart built from its own JSON. Colour went through the `dataviz` skill's
  validator: the site's `--teal` (#4FD1C5) **fails** the dark-mode lightness band at L 0.786,
  so the bars use **#00A99D**, which passes all six checks against the #111318 surface.

Cards render at natural width (`width:auto`) — upscaling monospace to fill the column blurs
it. Clips honour `prefers-reduced-motion` via a small script in `index.md` that swaps autoplay
for controls. Total media weight: **~6.4 MB** across 21 files.

**Verifying this without a Jekyll build:** the Liquid-render trick above was extended into a
real preview — render the Selected Work loop, inline `style.css`, write one HTML file, then
`chrome --headless --screenshot` it and *look*. That is how the unreadable
tt-forge-compiletron frame (a 2204px-wide TUI crushed into a 632px column) was caught; it is
now cropped to `crop=1010:540:0:180`, the pane that actually has content.

**2026-08-18 — the AnimateDiff post went live; only one of the five drafts is indexed.**
Prompt: *"how ready is the animatediff blog post here to just be part of the blog interface
of this site."* → *"let's just have the 06-23 post indexed or made live."*

`_posts/` held five AnimateDiff files: the committed 2026-06-23 "Full Story" plus four
untracked drafts it supersedes. Two of those drafts —
`2026-05-28-animatediff-model-bringup-tutorial.md` and
`2026-05-28-animatediff-ttlang-bringup.md` — were **byte-identical except for one link**,
same title, same date, and they cross-linked a permalink that never existed
(`.../animatediff-model-bringup-tutorial-deep/`). All four moved to **`_drafts/`**, which
Jekyll does not build without `--drafts`. They were left **untracked on purpose**: this
repo is public, so committing superseded drafts would publish claims the Full Story
corrects, even unbuilt.

**The post was the first long-form piece here, and `style.css` had no body-element rules.**
Verified by rendering it with kramdown into the real stylesheet and screenshotting
(the same Liquid/headless-Chrome trick as the project figures). Three things were broken:

* kramdown tables carry no classes and had **zero cell padding** — adjacent columns ran
  together as `Phase 3 skip up1+up21 chip, 8fr`. Now styled by element, with uppercase
  `th` and a `--border` row rule; checked at 760px and 380px.
* the global `* { padding: 0 }` reset left list markers hanging outside the column, and the
  default `<hr>` renders as a **bright 3D groove** — a hard white bar across a `#0a0d12`
  page, **18 times** in this one post.
* figure grids: the content column is **632px** (680 − 2×24), so the `280px` and `220px`
  three-up rows wrapped 2+1 and orphaned the third clip. All widths normalised to
  **200px** (3×200 + 2×12 gap = 624).

**Known, and shipped anyway at Taylor's call: the page is ~51 MB** — 28 embeds over 27 GIFs
in `assets/animatediff/`. Transcoding to H.264 would land it near 5 MB (the homepage figures
already do this), and that offer was declined for now. If you revisit it, the reduced-motion
script in `index.md` only targets `.project-media video` and would need to cover post videos.

Live at `/writing/2026/06/23/animatediff-on-tt-hardware-the-full-story/`; `/writing/` lists it.
Pages run 32157149988 succeeded — checked via `gh run view`, not the lying Pages API.

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
