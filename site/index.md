---
layout: default
title: Home
permalink: /
---

<div class="profile">
  <img class="profile-photo" src="{{ '/assets/images/profile/profile.jpg' | relative_url }}" alt="{{ site.data.profile.name }}">
  <div class="profile-info">
    <h1>{{ site.data.profile.name }}</h1>
    <p class="affiliation">{{ site.data.profile.department }}<br>{{ site.data.profile.institution }}</p>
    <div class="profile-links">
      {% for link in site.data.profile.cv_links %}
        <a href="{{ link.url }}">{{ link.text }}</a>
      {% endfor %}
      <a href="{{ site.cv_url | relative_url }}">CV</a>
    </div>
  </div>
</div>

## About

{{ site.data.profile.bio }}

<h2 class="section-heading">News</h2>

<ul class="news-list">
{% for item in site.data.news.news limit:8 %}
<li class="news-item">
  <span class="news-date">{{ item.date_display }}</span>
  <span class="news-badge news-badge--{{ item.category }}">{{ item.category }}</span>
  <span class="news-text">
    {% if item.url and item.title %}
      <a href="{{ item.url }}">{{ item.title }}</a> — {{ item.text }}
    {% elsif item.url %}
      <a href="{{ item.url }}">{{ item.text }}</a>
    {% else %}
      {{ item.text }}
    {% endif %}
  </span>
</li>
{% endfor %}
</ul>

<h2 class="section-heading">Selected Publications</h2>

<ul class="pub-list">
{% assign selected = site.data.journal_pubs.publications | concat: site.data.conf_pubs.publications | sort: "year" | reverse %}
{% for pub in selected limit:5 %}
<li class="pub-item">
  <span class="pub-num">{{ pub.number }}</span>
  <div class="pub-body">
    <div class="pub-title">
      {% if pub.link %}<a href="{{ pub.link }}">{{ pub.title }}</a>{% else %}{{ pub.title }}{% endif %}
      {% if pub.awards %}{% for award in pub.awards %}<span class="pub-awards">{{ award }}</span>{% endfor %}{% endif %}
    </div>
    <div class="pub-authors">{{ pub.author_html }}</div>
    <div class="pub-venue">{{ pub.venue_html }}</div>
  </div>
</li>
{% endfor %}
</ul>

<p><a href="{{ '/publications/' | relative_url }}">→ Full publication list</a></p>
