from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from website.image_manifest import MANIFEST

register = template.Library()
ALIASES = {'project-01.jpg': 'ground-01', 'home-project-01.jpg': 'ground-01',
           'project-02.jpg': 'ground-02', 'home-project-02.jpg': 'ground-02', 'hero.jpg': 'hero'}

@register.filter
def media_url(filename):
    item = MANIFEST.get(ALIASES.get(filename, filename))
    return static(item['variants'][-1]['file']) if item else static('images/' + filename)

@register.simple_tag
def image_attributes(filename):
    item = MANIFEST.get(ALIASES.get(filename, filename))
    if not item:
        return ''
    srcset = ', '.join(f"{static(v['file'])} {v['width']}w" for v in item['variants'])
    return format_html('width="{}" height="{}" srcset="{}" sizes="(max-width: 600px) 100vw, (max-width: 1100px) 70vw, 960px" decoding="async"', item['width'], item['height'], srcset)
