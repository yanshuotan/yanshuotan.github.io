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
  </div>
  <ul class="talk-venues">
    {% for inst in talk.instances %}
    <li>{{ inst.venue }}, {{ inst.location }}, {{ inst.date_display }}{% if inst.recording %} <a class="pub-link-badge" href="{{ inst.recording }}">Video</a>{% endif %}</li>
    {% endfor %}
  </ul>
</li>
{% endfor %}
</ul>

{% if site.data.posters.posters.size > 0 %}
<h2 class="section-heading">Poster Presentations</h2>

<ul class="talk-list">
{% for poster in site.data.posters.posters %}
<li class="talk-item">
  <div class="talk-header">
    <span class="talk-title">{{ poster.title }}</span>
  </div>
  <ul class="talk-venues">
    {% for inst in poster.instances %}
    <li>{{ inst.venue }}, {{ inst.location }}, {{ inst.date_display }}</li>
    {% endfor %}
  </ul>
</li>
{% endfor %}
</ul>
{% endif %}
