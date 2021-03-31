from functools import wraps

from django.shortcuts import get_object_or_404, redirect


def no_tracker_required(_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, "tracker"):
                return redirect("tracker:detail")
            return func(request, *args, **kwargs)

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)


def tracker_required(_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.user, "tracker"):
                return redirect("tracker:create")
            return func(request, request.user.tracker, *args, **kwargs)

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)


def category_required(_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, tracker, category_slug, *args, **kwargs):
            category = get_object_or_404(tracker.get_categories(), slug=category_slug)
            return func(request, tracker, category, *args, **kwargs)

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)
