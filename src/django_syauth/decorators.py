from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

def syauth_login_required(view_func):
    """
    Decorator for views that checks that the user is logged in,
    redirecting to the Syauth login page if necessary.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('django_syauth:login')
    return _wrapped_view
