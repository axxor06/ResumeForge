from django import template

register = template.Library()

@register.filter
def first(value):
    if value:
        return value[0]
    return ''

@register.filter
def split_tech(value):
    """Split tech string by comma, slash, or pipe into a list of tags."""
    if not value:
        return []
    import re
    parts = re.split(r'[,/|]', str(value))
    return [p.strip() for p in parts if p.strip()]
