from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def role_required(*roles):
    """Allow access only to users with one of the given roles."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                login_url = reverse('school:login')
                return redirect(f'{login_url}?next={request.path}')
            try:
                role = request.user.profile.role
            except Exception:
                role = None
            if role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'អ្នកមិនមានសិទ្ធិចូលទៅកាន់ទំព័រនេះ។')
            return redirect('school:dashboard')
        return _wrapped
    return decorator


def admin_required(view_func):
    return role_required('admin')(view_func)


def admin_or_teacher(view_func):
    return role_required('admin', 'teacher')(view_func)


def all_roles(view_func):
    return role_required('admin', 'teacher', 'parent', 'student')(view_func)
