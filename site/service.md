---
layout: default
title: Service
permalink: /service/
---

# Academic Service

<h2 class="section-heading">Reviewing — Journals</h2>

<table class="service-table">
<thead><tr><th>Venue</th><th>Years</th></tr></thead>
<tbody>
{% assign journals = site.data.service.reviewing | where: "type", "journal" %}
{% for r in journals %}
<tr>
  <td>{{ r.venue }}</td>
  <td>{{ r.years | sort | join: ", " }}</td>
</tr>
{% endfor %}
</tbody>
</table>

<h2 class="section-heading">Reviewing — Conferences</h2>

<table class="service-table">
<thead><tr><th>Venue</th><th>Years</th></tr></thead>
<tbody>
{% assign confs = site.data.service.reviewing | where: "type", "conference" %}
{% for r in confs %}
<tr>
  <td>{{ r.venue }}</td>
  <td>{{ r.years | sort | join: ", " }}</td>
</tr>
{% endfor %}
</tbody>
</table>

<h2 class="section-heading">Other Service</h2>

<table class="service-table">
<thead><tr><th>Role</th><th>Organization</th><th>Years</th></tr></thead>
<tbody>
{% for s in site.data.service.other_service %}
<tr>
  <td>{{ s.title }}</td>
  <td>{{ s.organization }}</td>
  <td>{{ s.year_start }}{% if s.year_end %}–{{ s.year_end }}{% endif %}</td>
</tr>
{% endfor %}
</tbody>
</table>
