from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Usage: {{ mydict|get_item:key }}"""
    return dictionary.get(key, '')


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
    from django.utils.html import format_html
    return format_html('<span class="badge bg-{}">{}</span>', color, label)
