---
layout: default
title: Joining
permalink: /joining/
---

# Joining the Group

{{ site.data.joining.intro }}

<ul class="opening-list">
{% for position in site.data.joining.positions %}
<li>
<details class="opening" id="{{ position.id }}">
  <summary class="opening-summary">
    <div class="opening-summary-left">
      <span class="opening-title">{{ position.title }}</span>
      <span class="opening-status opening-status--{{ position.status }}">{{ position.status }}</span>
    </div>
    <div class="opening-summary-text">{{ position.summary }}</div>
  </summary>
  <div class="opening-body">
    {% for para in position.description %}
    <p>{{ para }}</p>
    {% endfor %}
    {% if position.deadline %}<p class="opening-meta"><strong>Deadline:</strong> {{ position.deadline }}</p>{% endif %}
    {% if position.how_to_apply %}<p class="opening-meta"><strong>How to apply:</strong> {{ position.how_to_apply }}</p>{% endif %}
  </div>
</details>
</li>
{% endfor %}
</ul>

<script>
// Auto-expand and scroll to a position if linked via #id (e.g. /joining/#postdoc)
if (location.hash) {
  var target = document.querySelector(location.hash);
  if (target && target.tagName === "DETAILS") {
    target.open = true;
    target.scrollIntoView({ block: "start" });
  }
}
</script>
