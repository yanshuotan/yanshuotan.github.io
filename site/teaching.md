---
layout: default
title: Teaching
permalink: /teaching/
---

# Teaching

{% assign institutions = site.data.teaching.teaching | map: "institution" | uniq %}
{% for inst in institutions %}
<div class="teaching-group">
<h3>{{ inst }}</h3>
<ul class="course-list">
{% for course in site.data.teaching.teaching %}
{% if course.institution == inst %}
<li class="course-item">
  <div class="course-header">
    <span class="course-name">
      {% if course.course_code %}<strong>{{ course.course_code }}</strong>: {% endif %}{{ course.title }}
    </span>
    <span class="course-meta">{{ course.level }} · {{ course.role }}</span>
  </div>
  <div class="course-meta">{{ course.semesters | join: ", " }}</div>
  {% if course.description %}
    <div class="course-desc">{{ course.description }}</div>
  {% endif %}
  {% if course.notes %}
    <div class="course-desc">{{ course.notes }}</div>
  {% endif %}
</li>
{% endif %}
{% endfor %}
</ul>
</div>
{% endfor %}
