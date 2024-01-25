from django import template

register = template.Library()


@register.filter(name="in_group")
def in_group(user, group_name):
    return bool(bool(user.groups.filter(name=group_name)) or user.is_superuser)
