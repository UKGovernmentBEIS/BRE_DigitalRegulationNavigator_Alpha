from functools import wraps

from django.shortcuts import redirect

FINDER_DATA_KEY = "finder_data"


def finder_data_required(_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if FINDER_DATA_KEY not in request.session:
                return redirect("finder:index")
            return func(request, request.session[FINDER_DATA_KEY], *args, **kwargs)

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)
