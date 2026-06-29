from .models import SchoolSettings


def school_settings(request):
    """Inject school settings into every template context."""
    return {'school': SchoolSettings.get()}
