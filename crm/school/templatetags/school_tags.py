from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Usage: {{ mydict|get_item:key }}"""
    return dictionary.get(key, '')


@register.filter
def safe_url(image_field):
    """
    Safely return the URL of an image field.
    Returns empty string if the field is empty or the URL cannot be generated.
    Usage: {{ obj.photo|safe_url }}
    """
    if not image_field:
        return ''
    try:
        name = getattr(image_field, 'name', None)
        if not name:
            return ''
        return image_field.url
    except Exception:
        return ''


@register.simple_tag(takes_context=True)
def user_role(context):
    """Return the role display of the logged-in user safely."""
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return ''
    try:
        return request.user.profile.get_role_display()
    except Exception:
        return ''


@register.simple_tag(takes_context=True)
def user_role_badge(context):
    """Return a Bootstrap badge for the user's role."""
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return ''
    try:
        role = request.user.profile.role
    except Exception:
        role = ''
    colors = {
        'admin':   'danger',
        'teacher': 'primary',
        'parent':  'success',
        'student': 'secondary',
    }
    color = colors.get(role, 'secondary')
    label = role.capitalize() if role else 'User'
    return format_html('<span class="badge bg-{}">{}</span>', color, label)
