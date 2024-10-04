from django import template

register = template.Library()

@register.filter
def field_hour(dictionary, key):
    return dictionary.get(key)
