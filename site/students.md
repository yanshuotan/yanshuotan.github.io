---
layout: default
title: Students
permalink: /students/
---

# Students

{% assign current = site.data.students.students | where_exp: "s", "s.expected == true" %}
{% assign graduated = site.data.students.students | where_exp: "s", "s.expected != true" %}

<h2 class="section-heading">Current</h2>

<ul class="student-list">
{% for s in current %}
<li class="student-item">
  <div>
    <span class="student-name">{{ s.name }}</span>
    <span class="student-degree">&nbsp;({{ s.degree }}{% if s.coadvisor %}, co-advised with {{ s.coadvisor }}{% endif %})</span>
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
    <span class="student-degree">&nbsp;({{ s.degree }}{% if s.coadvisor %}, co-advised with {{ s.coadvisor }}{% endif %})</span>
  </div>
  <span class="student-years">{{ s.year_start }}–{{ s.year_end }}</span>
</li>
{% endfor %}
</ul>
{% endif %}

{% if site.data.students.mentoring %}
<h2 class="section-heading">Other Mentoring</h2>
<ul class="student-list">
{% for m in site.data.students.mentoring %}
<li class="student-item">
  <div>
    <span class="student-name">{{ m.title }}</span>
    <span class="student-degree">&nbsp;— {{ m.organization }}</span>
  </div>
  <span class="student-years">{{ m.year_start }}{% if m.year_end %}–{{ m.year_end }}{% endif %}</span>
</li>
{% endfor %}
</ul>
{% endif %}
