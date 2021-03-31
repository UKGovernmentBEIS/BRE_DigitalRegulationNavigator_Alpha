from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def remove_filter(context, name, value):
    data = context["request"].GET.copy()
    values = data.getlist(name)

    values.remove(str(value))
    data.setlist(name, values)

    return data.urlencode()
