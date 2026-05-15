---
layout: default
title: Publications
permalink: /publications/
---

# Publications

<p class="pub-footnote">
  <sup>*</sup> Equal contribution or alphabetical ordering &nbsp;|&nbsp;
  <sup>†</sup> Student or postdoc supervised &nbsp;|&nbsp;
  <sup>‡</sup> Corresponding author
</p>

{% assign arxiv_base = "https://arxiv.org/abs/" %}

<h2 class="section-heading">Journal Publications</h2>
<div class="pub-section">
<ul class="pub-list">
{% for pub in site.data.journal_pubs.publications %}
<li class="pub-item">
  <span class="pub-num">{{ pub.number }}</span>
  <div class="pub-body">
    <div class="pub-title">
      {% if pub.link %}<a href="{{ pub.link }}">{{ pub.title }}</a>{% else %}{{ pub.title }}{% endif %}
      {% if pub.awards %}{% for award in pub.awards %}<span class="pub-awards">{{ award }}</span>{% endfor %}{% endif %}
    </div>
    <div class="pub-authors">{{ pub.author_html }}</div>
    <div class="pub-venue">{{ pub.venue_html }}</div>
    {% if pub.arxiv %}
    <div class="pub-links">
      <a class="pub-link-badge" href="{{ arxiv_base }}{{ pub.arxiv }}">arXiv</a>
    </div>
    {% endif %}
    {% if pub.notes and pub.notes != "Author list alphabetical" %}
      <div class="pub-note">{{ pub.notes }}</div>
    {% endif %}
  </div>
</li>
{% endfor %}
</ul>
</div>

<h2 class="section-heading">Conference Publications</h2>
<div class="pub-section">
<ul class="pub-list">
{% for pub in site.data.conf_pubs.publications %}
<li class="pub-item">
  <span class="pub-num">{{ pub.number }}</span>
  <div class="pub-body">
    <div class="pub-title">
      {% if pub.link %}<a href="{{ pub.link }}">{{ pub.title }}</a>{% else %}{{ pub.title }}{% endif %}
      {% if pub.awards %}{% for award in pub.awards %}<span class="pub-awards">{{ award }}</span>{% endfor %}{% endif %}
    </div>
    <div class="pub-authors">{{ pub.author_html }}</div>
    <div class="pub-venue">{{ pub.venue_html }}</div>
    {% if pub.arxiv %}
    <div class="pub-links">
      <a class="pub-link-badge" href="{{ arxiv_base }}{{ pub.arxiv }}">arXiv</a>
    </div>
    {% endif %}
  </div>
</li>
{% endfor %}
</ul>
</div>

<h2 class="section-heading">Preprints</h2>
<div class="pub-section">
<ul class="pub-list">
{% for pub in site.data.preprints.publications %}
<li class="pub-item">
  <span class="pub-num">{{ pub.number }}</span>
  <div class="pub-body">
    <div class="pub-title">
      {% if pub.link %}<a href="{{ pub.link }}">{{ pub.title }}</a>{% else %}{{ pub.title }}{% endif %}
    </div>
    <div class="pub-authors">{{ pub.author_html }}</div>
    <div class="pub-venue">{{ pub.venue_html }}</div>
  </div>
</li>
{% endfor %}
</ul>
</div>
