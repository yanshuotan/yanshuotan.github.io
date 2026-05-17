---
layout: default
title: Students
permalink: /students/
---

# Students

{% assign current = site.data.students.students | where_exp: "s", "s.expected == true" %}
{% assign graduated = site.data.students.students | where_exp: "s", "s.expected != true" %}

<div class="group-photo-wrap">
  <img class="group-photo" src="{{ '/assets/images/students.jpeg' | relative_url }}" alt="Group photo">
  <p class="group-photo-caption">With my students, April 2026</p>
</div>

<h2 class="section-heading">Current</h2>

<ul class="student-list">
{% for s in current %}
<li class="student-item">
  <div>
    <span class="student-name">{{ s.name }}</span>
    <span class="student-degree">&nbsp;({{ s.degree }}{% if s.coadvisor %}, co-advised with {{ s.coadvisor }}{% endif %}{% if s.notes %}, <em>{{ s.notes }}</em>{% endif %})</span>
  </div>
  <span class="student-years">{{ s.year_start }}–{{ s.year_end }} (expected)</span>
</li>
{% endfor %}
</ul>

{% if graduated.size > 0 %}
<h2 class="section-heading">Graduated / Completed</h2>
<ul class="student-list">
{% for s in graduated %}
<li class="student-item">
  <div>
    <span class="student-name">{{ s.name }}</span>
    <span class="student-degree">&nbsp;({{ s.degree }}{% if s.coadvisor %}, co-advised with {{ s.coadvisor }}{% endif %}{% if s.notes %}, <em>{{ s.notes }}</em>{% endif %})</span>
  </div>
  <span class="student-years">{{ s.year_start }}–{{ s.year_end }}</span>
</li>
{% endfor %}
</ul>
{% endif %}
