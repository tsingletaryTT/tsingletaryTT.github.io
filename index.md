---
layout: default
---

<div class="hero">
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

<section class="section" id="work">
  <div class="section-label">Selected Work</div>
  {% for project in site.data.projects %}
  <div class="project">
    <div class="project-header">
      <span class="project-name">{{ project.name }}</span>
      <span class="project-lang">{{ project.lang }}</span>
    </div>
    <div class="project-desc">{{ project.desc }}</div>
    <a href="{{ project.url }}" class="project-link">{{ project.url | remove: "https://" }} ↗</a>
  </div>
  {% endfor %}
</section>

<section class="section">
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

<section class="section" id="writing">
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
  {% else %}
  <p class="post-placeholder">Posts will appear here.</p>
  {% endif %}
</section>
