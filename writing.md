---
layout: default
title: Writing
permalink: /writing/
---

<div class="page-header">
  <div class="section-label">Writing</div>
</div>

<section class="section" style="border-top: none; padding-top: 24px;">
  {% if site.data.writing %}{% assign external_posts = site.data.writing | sort: "date" | reverse %}{% else %}{% assign external_posts = "" | split: "" %}{% endif %}
  {% if site.posts.size > 0 or external_posts.size > 0 %}
  <ul class="post-list">
    {% for post in site.posts %}
    <li class="post-item">
      <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      <a href="{{ post.url | relative_url }}" class="post-title-link">{{ post.title }}</a>
    </li>
    {% endfor %}
    {% for post in external_posts %}
    <li class="post-item">
      <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      <a href="{{ post.url }}" class="post-title-link">{{ post.title }} <span class="post-host">{{ post.url | remove: "https://" | split: "/" | first }} ↗</span></a>
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p class="post-placeholder">No posts yet.</p>
  {% endif %}
  <a href="{{ '/feed.xml' | relative_url }}" class="view-all" type="application/atom+xml">Subscribe · RSS ↗</a>
</section>
