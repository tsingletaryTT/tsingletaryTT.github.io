---
layout: default
---

<div class="hero prose">
  <div class="hero-handle">@tsingletaryTT</div>
  <div class="hero-name">Taylor<br>Singletary</div>
  <div class="hero-role">
    Developer Relations at <strong>Tenstorrent</strong><br>
    Building tools, community, and on-ramps for the future of AI hardware.
  </div>
  <div class="hero-links">
    <a href="https://github.com/tsingletaryTT" class="primary">GitHub ↗</a>
    <a href="https://tenstorrent.com">Tenstorrent ↗</a>
    <a href="https://github.com/tsingletaryTT/tt-awesome">tt-awesome ↗</a>
  </div>
</div>

{%- comment -%}
  Category order is editorial, not alphabetical: flagship technical bring-up work
  leads, then the more playful/showcase demos, then the education and tooling that
  support them. Each project.yml entry carries exactly one `category` key from this
  list, so a filter pill only needs to show/hide whole category-blocks — no
  per-card filtering required.
{%- endcomment -%}
{% assign category_keys = "education,bringup,applied,demos,tools" | split: "," %}
{% assign category_labels = "Interactive developer education,Model development & bringup,Applied AI Applications,Demos & games,Developer tools" | split: "," %}

<section class="section" id="work">
  <div class="section-label">Selected Work</div>
  <div class="work-toolbar" role="group" aria-label="Filter by category">
    <button type="button" class="filter-pill active" data-filter="all">All</button>
    {% for key in category_keys %}
    <button type="button" class="filter-pill" data-filter="{{ key }}">{{ category_labels[forloop.index0] }}</button>
    {% endfor %}
  </div>
  {% for key in category_keys %}
  {% assign items = site.data.projects | where: "category", key %}
  {% if items.size > 0 %}
  <div class="category-block" data-category="{{ key }}">
    <div class="category-label">{{ category_labels[forloop.index0] }}</div>
    <div class="project-grid">
      {% for project in items %}
      <div class="project">
        <div class="project-header">
          <span class="project-name">{{ project.name }}</span>
          <span class="project-lang">{{ project.lang }}</span>
        </div>
        <div class="project-desc">{{ project.desc }}</div>
        {% if project.media %}
        <figure class="project-media project-media--{{ project.media_kind }}">
          {%- comment -%}
            media_alt lands inside an HTML attribute, so it MUST be escaped. An unescaped double
            quote in a figure's alt text closes the attribute early, kramdown then fails to parse
            the tag and ships it to the page as escaped text — a visible "&lt;img src=..." string
            where the figure should be. media_note and desc are element text and need no filter.
          {%- endcomment -%}
          {% if project.media_kind == 'clip' %}
          <video src="{{ project.media | relative_url }}"
                 poster="{{ project.poster | relative_url }}"
                 autoplay loop muted playsinline preload="metadata"
                 aria-label="{{ project.media_alt | escape }}"></video>
          {% else %}
          <img src="{{ project.media | relative_url }}" alt="{{ project.media_alt | escape }}"
               loading="lazy" decoding="async">
          {% endif %}
          {% if project.media_note %}<figcaption>{{ project.media_note }}</figcaption>{% endif %}
        </figure>
        {% endif %}
        <a href="{{ project.url }}" class="project-link">{{ project.url | remove: "https://" }} ↗</a>
        {% if project.site %}<a href="{{ project.site }}" class="project-link">Live site ↗</a>{% endif %}
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}
  {% endfor %}
</section>

{% comment %}
  Hidden while _data/contributions.yml is empty — a section label with an empty grid under it
  reads as a bug. Add an entry to that file and this comes back on its own.
{% endcomment %}
{% if site.data.contributions and site.data.contributions.size > 0 %}
<section class="section prose">
  <div class="section-label">Contributing To</div>
  <div class="contrib-grid">
    {% for item in site.data.contributions %}
    <a href="https://github.com/{{ item.repo }}" class="contrib-item">
      <div class="contrib-org">{{ item.repo | split: "/" | first }}/</div>
      <div class="contrib-name">{{ item.repo | split: "/" | last }}</div>
    </a>
    {% endfor %}
  </div>
</section>
{% endif %}

<section class="section prose" id="writing">
  <div class="section-label">Writing</div>
  {% assign recent_posts = site.posts | limit: 3 %}
  {% if recent_posts.size > 0 %}
  <ul class="post-list">
    {% for post in recent_posts %}
    <li class="post-item">
      <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      <a href="{{ post.url | relative_url }}" class="post-title-link">{{ post.title }}</a>
    </li>
    {% endfor %}
  </ul>
  <a href="{{ '/writing' | relative_url }}" class="view-all">View all writing ↗</a>
  <a href="{{ '/feed.xml' | relative_url }}" class="view-all" type="application/atom+xml">RSS ↗</a>
  {% else %}
  <p class="post-placeholder">Posts will appear here.</p>
  {% endif %}
</section>

<script>
  (function () {
    if (!window.matchMedia || !matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    document.querySelectorAll('.project-media video').forEach(function (v) {
      v.autoplay = false;
      v.loop = false;
      v.controls = true;
      v.pause();
    });
  })();
</script>

<script>
  (function () {
    var pills = document.querySelectorAll('.filter-pill');
    var blocks = document.querySelectorAll('.category-block');
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var filter = pill.dataset.filter;
        pills.forEach(function (p) { p.classList.toggle('active', p === pill); });
        blocks.forEach(function (block) {
          block.hidden = filter !== 'all' && block.dataset.category !== filter;
        });
      });
    });
  })();
</script>
