from .models import SchoolSettings


def school_settings(request):
    """Inject school settings into every template context."""
    return {'school': SchoolSettings.get()}


def ensure_user_profile(request):
    """
    Ensure every authenticated user has a UserProfile.
    Prevents RelatedObjectDoesNotExist crashes in templates.
    """
    if request.user.is_authenticated:
        try:
            _ = request.user.profile
        except Exception:
            from .models import UserProfile
            role = 'admin' if request.user.is_superuser else 'student'
            UserProfile.objects.get_or_create(
                user=request.user,
                defaults={'role': role}
            )
    return {}
