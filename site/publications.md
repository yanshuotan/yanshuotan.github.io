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

<div class="topic-filters">
  <span class="topic-filter-label">Filter by topic:</span>
  <button class="topic-btn active" data-topic="all">All</button>
  <button class="topic-btn" data-topic="trees">Trees</button>
  <button class="topic-btn" data-topic="ensembles">Ensembles</button>
  <button class="topic-btn" data-topic="Bayesian">Bayesian</button>
  <button class="topic-btn" data-topic="BART">BART</button>
  <button class="topic-btn" data-topic="prior-data fitted networks">Prior-data fitted networks</button>
  <button class="topic-btn" data-topic="interpretability">Interpretability</button>
  <button class="topic-btn" data-topic="theory">Theory</button>
</div>

{% assign arxiv_base = "https://arxiv.org/abs/" %}

<h2 class="section-heading">Journal Publications</h2>
<div class="pub-section">
<ul class="pub-list">
{% for pub in site.data.journal_pubs.publications %}
<li class="pub-item" data-topics="{{ pub.topics | join: '|' }}">
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
<li class="pub-item" data-topics="{{ pub.topics | join: '|' }}">
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
<li class="pub-item" data-topics="{{ pub.topics | join: '|' }}">
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

<script>
(function () {
  var buttons = document.querySelectorAll('.topic-btn');
  var items   = document.querySelectorAll('.pub-item');

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var topic = btn.getAttribute('data-topic');

      // Update active button
      buttons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');

      // Show/hide items
      items.forEach(function (item) {
        if (topic === 'all') {
          item.style.display = '';
        } else {
          var topics = item.getAttribute('data-topics').split('|');
          item.style.display = topics.indexOf(topic) !== -1 ? '' : 'none';
        }
      });

      // Hide section headings with no visible items
      document.querySelectorAll('.pub-section').forEach(function (section) {
        var heading = section.previousElementSibling;
        var visible = section.querySelectorAll('.pub-item:not([style*="none"])').length;
        if (heading) heading.style.display = visible ? '' : 'none';
        section.style.display = visible ? '' : 'none';
      });
    });
  });
})();
</script>
