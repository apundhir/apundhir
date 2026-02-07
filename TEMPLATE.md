![{{ name }} — {{ title }}](assets/github-banner.jpg)

# {{ name }}

**{{ title }}**

{{ tagline }}

{{ mission_statement }}

**Credentials:** {{ credentials | join(' · ') }}

🔭 **Currently exploring:** {{ currently_exploring | join(' · ') }}

---

## 🔬 Open Source & Frameworks

| Project | What It Solves |
|---------|---------------|
{% for repo in featured_repos -%}
| [{{ repo.display_name or repo.name }}](https://github.com/apundhir/{{ repo.name }}) | {{ repo.tagline }} |
{% endfor %}

---

## 📊 Impact

| 70% | Multi-million $ | Full-lifecycle |
|:---:|:---:|:---:|
| Reduction in enterprise model time-to-deployment | Annualized value through AI-driven optimization | Responsible AI governance operationalized |

---

## ✏️ Latest Writing

<!-- BLOG_POSTS_START -->
{% for post in blog_posts -%}
- [{{ post.title }}]({{ post.url }})
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

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)]({{ links.linkedin }}) [![AiExponent](https://img.shields.io/badge/AiExponent-Visit-0D7377?style=flat)]({{ links.website }}) [![Forbes](https://img.shields.io/badge/Forbes_Tech_Council-Profile-1a1a1a?style=flat)]({{ links.forbes }}) [![Senior Executive](https://img.shields.io/badge/Senior_Executive-Profile-2c3e50?style=flat)]({{ links.senior_executive }}) [![X](https://img.shields.io/badge/X-Follow-000000?style=flat&logo=x&logoColor=white)]({{ links.twitter }})

---

> {{ signature_quote }}

{% if settings.show_last_updated %}
<sub>🔄 Profile auto-updated on {{ last_updated }} · Powered by [GitHub Actions](https://github.com/apundhir/apundhir/actions)</sub>
{% endif %}
