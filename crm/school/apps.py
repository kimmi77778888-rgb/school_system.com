from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school'
    
    def ready(self):
        """Import signals when app is ready"""
        import school.signals  # noqa
