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


def notifications_context(request):
    """
    Add notification data to every template context.
    Shows unread count and recent notifications in topbar.
    """
    if request.user.is_authenticated:
        try:
            from .models import Notification, NotificationRead
            from django.db.models import Q, Exists, OuterRef
            
            # Safely get user role
            try:
                user_role = request.user.profile.role
            except Exception:
                return {'unread_count': 0, 'recent_notifications': []}
            
            # Safely get student if applicable
            student_obj = None
            try:
                if user_role in ['student', 'parent'] and hasattr(request.user.profile, 'student'):
                    student_obj = request.user.profile.student
            except Exception:
                pass
            
            # Get classroom for student
            classroom_obj = None
            try:
                if user_role == 'student' and student_obj:
                    classroom_obj = student_obj.classroom
            except Exception:
                pass
            
            # Get notifications for this user based on role and audience
            notifications = Notification.objects.filter(
                Q(audience='everyone') | 
                Q(audience=user_role) |
                Q(classroom=classroom_obj) |
                Q(student=student_obj)
            ).filter(is_active=True).order_by('-created_at')
            
            # Annotate with read status
            notifications = notifications.annotate(
                is_read=Exists(
                    NotificationRead.objects.filter(
                        notification=OuterRef('pk'),
                        user=request.user
                    )
                )
            )
            
            # Count unread
            unread_count = notifications.filter(is_read=False).count()
            
            # Get recent 5 notifications
            recent_notifications = list(notifications[:5])
            
            return {
                'unread_count': unread_count,
                'recent_notifications': recent_notifications,
            }
        except Exception as e:
            # If anything fails, return empty notifications rather than crashing
            return {'unread_count': 0, 'recent_notifications': []}
    
    return {
        'unread_count': 0,
        'recent_notifications': [],
    }
