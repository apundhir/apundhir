[![{{ banner.alt }}]({{ banner.path }})]({{ links.askajay }})

# {{ name }}

**{{ title }}**

*{{ tagline }}*

{{ intro | trim }}

**Credentials:** {{ credentials | join(' · ') }}

[![AskAjay.ai](https://img.shields.io/badge/AskAjay.ai-Visit-0E3A5C?style=flat)]({{ links.askajay }}) [![The Brief](https://img.shields.io/badge/The_Brief-Subscribe-0E3A5C?style=flat)]({{ links.brief }}) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)]({{ links.linkedin }}) [![X](https://img.shields.io/badge/X-Follow-000000?style=flat&logo=x&logoColor=white)]({{ links.x }})

---

## What I'm working on

{% for item in working_on %}
- {{ item }}
{% endfor %}

| {{ numbers | map(attribute='value') | join(' | ') }} |
|{{ ':---:|' * (numbers | length) }}
| {{ numbers | map(attribute='label') | join(' | ') }} |

---

## Latest writing

<!-- LATEST_WRITING_START -->
{% for post in latest_writing %}
- [{{ post.title }}]({{ post.url }})
{% endfor %}
<!-- LATEST_WRITING_END -->

More at [askajay.ai/thinking]({{ links.askajay }}/thinking). Every other Tuesday I send [The Brief]({{ links.brief }}): one argument, one correction of the week's coverage, one move for Monday.

### Published elsewhere

{% for pub in publications %}
- [{{ pub.title }}]({{ pub.url }}) · *{{ pub.publication }}*{{ ', ' ~ pub.date_formatted if pub.date_formatted }}
{% endfor %}

My [Forbes Technology Council profile]({{ links.forbes }}) has the full list of columns.

---

## Frameworks

{{ frameworks | join(' · ') }}

Free to use, with worksheets, at [askajay.ai/tools]({{ frameworks_url }}).

---

## Open source

| Project | What it does |
|---------|--------------|
{% for p in open_source %}
| [{{ p.name }}](https://github.com/{{ p.repo }}) | {{ p.what }} |
{% endfor %}

The first five are built and maintained by [AiExponent]({{ links.aiexponent }}), the product arm of AI Exponent LLC.

---

## Work with me

{% for s in services %}
- [{{ s.name }}]({{ s.url }}) for {{ s.for }}
{% endfor %}

The quickest way to reach me is [askajay.ai/connect]({{ links.connect }}).
