---
layout: default
title: Photos
permalink: /photos/
---

# Photos

{% assign sorted_photos = site.data.photos.photos | sort: "year" | reverse %}
{% assign years = sorted_photos | map: "year" | uniq %}

{% if sorted_photos.size == 0 %}
<p style="color: var(--muted);">Photos coming soon.</p>
{% else %}
{% for year in years %}
<h2 class="section-heading">{{ year }}</h2>
<div class="photo-grid">
{% assign year_photos = sorted_photos | where: "year", year %}
{% for photo in year_photos %}
<div class="photo-card">
  <img src="{{ '/assets/images/' | append: photo.file | relative_url }}"
       alt="{{ photo.caption }}"
       loading="lazy">
  <p class="photo-caption">{{ photo.caption }}{% if photo.event %}<br><span class="photo-event">{{ photo.event }}</span>{% endif %}</p>
</div>
{% endfor %}
</div>
{% endfor %}
{% endif %}
