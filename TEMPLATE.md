# {{ name }}

**{{ title }}**

{{ tagline }}

{{ mission_statement }}

**Credentials:** {{ credentials | join(' · ') }}

🔭 **Currently exploring:** {{ currently_exploring | join(' · ') }}

---

## 🔬 Open Source & Frameworks

| Project | What It Solves | ⭐ |
|---------|---------------|----|
{% for repo in featured_repos -%}
| [{{ repo.display_name or repo.name }}](https://github.com/apundhir/{{ repo.name }}) | {{ repo.tagline }} | {{ repo.stars or '' }} |
{% endfor %}

---

## 📊 Impact

{% for item in impact -%}
- **{{ item.metric }}** — {{ item.description }}
{% endfor %}

---

## ✏️ Latest Writing

<!-- BLOG_POSTS_START -->
{% for post in blog_posts -%}
- [{{ post.title }}]({{ post.url }}) {% if post.source %}· *{{ post.source }}*{% endif %}
{% endfor %}
<!-- BLOG_POSTS_END -->

{% if publications %}
### Featured Publications

{% for pub in publications -%}
{% if pub.featured -%}
- **{{ pub.title }}** — *{{ pub.publication }}*{% if pub.date %} ({{ pub.date_formatted }}){% endif %}{% if pub.url %} [Read →]({{ pub.url }}){% endif %}
{% if pub.quote %}  > "{{ pub.quote }}"
{% endif -%}
{% endif -%}
{% endfor -%}
{% endif %}

---

## 🤝 Advisory & Speaking

{{ aiexponent_tagline }}

**For Organizations & Leaders:** {{ speaking.for_organizations | join(' · ') }}

**For Individuals & Founders:** {{ speaking.for_founders | join(' · ') }}

**Topics:** {{ speaking.topics | join(' · ') }}

{% if speaking.upcoming_events %}
### Upcoming

{% for event in speaking.upcoming_events -%}
- **{{ event.name }}** ({{ event.date }}) — *{{ event.topic }}*
{% endfor %}
{% endif %}

---

## 🤝 Connect

{{ connect_text }}

[LinkedIn]({{ links.linkedin }}) · [AiExponent]({{ links.website }}) · [Forbes Tech Council]({{ links.forbes }}) · [Senior Executive]({{ links.senior_executive }}) · [X/Twitter]({{ links.twitter }})

---

> {{ signature_quote }}

{% if settings.show_last_updated %}
<sub>🔄 Profile auto-updated on {{ last_updated }} · Powered by [GitHub Actions](https://github.com/apundhir/apundhir/actions)</sub>
{% endif %}
