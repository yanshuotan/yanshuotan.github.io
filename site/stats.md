---
layout: default
title: Stats
permalink: /stats/
---

# Stats

<div class="stats-grid">
  <div class="stat-card">
    <span class="stat-number">{{ site.data.stats.publications.journal }}</span>
    <span class="stat-label">Journal papers</span>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ site.data.stats.publications.conference }}</span>
    <span class="stat-label">Conference papers</span>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ site.data.stats.publications.preprint }}</span>
    <span class="stat-label">Preprints</span>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ site.data.stats.reviewing.total }}</span>
    <span class="stat-label">Papers reviewed</span>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ site.data.stats.talks.total_instances }}</span>
    <span class="stat-label">Invited talks</span>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ site.data.stats.talks.num_locations }}</span>
    <span class="stat-label">Cities visited</span>
  </div>
</div>

---

## Collaborators

Number of joint papers with each co-author, sorted by count.

<table class="stats-table">
  <thead>
    <tr><th>Name</th><th>Papers</th></tr>
  </thead>
  <tbody>
  {% for c in site.data.stats.collaborators %}
    <tr>
      <td>{{ c.name }}</td>
      <td>{{ c.papers }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>

---

## Reviewing

{{ site.data.stats.reviewing.total }} papers reviewed in total:
{{ site.data.stats.reviewing.journal }} for journals and
{{ site.data.stats.reviewing.conference }} for conferences.

<table class="stats-table">
  <thead>
    <tr><th>Venue</th><th>Type</th><th>Years</th></tr>
  </thead>
  <tbody>
  {% for r in site.data.service.reviewing %}
    <tr>
      <td>{% if r.venue_short %}{{ r.venue_short }}{% else %}{{ r.venue }}{% endif %}</td>
      <td>{{ r.type | capitalize }}</td>
      <td>{{ r.years | join: ", " }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>
