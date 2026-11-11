from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs): 

        if not request.user.is_authenticated:
            return redirect("login")
        
        if not request.user.groups.filter(name="Admin").exists():
            return redirect("home")

        return view_func(request, *args, **kwargs) # The user passed all security checks, so now execute the original view.
    return wrapper