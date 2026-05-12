---
layout: default
title: Talks
permalink: /talks/
---

# Invited Talks

<ul class="talk-list">
{% for talk in site.data.talks.talks %}
<li class="talk-item">
  <div class="talk-header">
    <span class="talk-title">{{ talk.title }}</span>
    <span class="talk-year">{{ talk.year_display }}</span>
  </div>
  <ul class="talk-venues">
    {% for inst in talk.instances %}
    <li>{{ inst.venue }}, {{ inst.location }}</li>
    {% endfor %}
  </ul>
</li>
{% endfor %}
</ul>
