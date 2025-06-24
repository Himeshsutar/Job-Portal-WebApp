from django.shortcuts import redirect
from .models import UserProfile

def employer_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role == 'Employer':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # or show a "Permission denied" message
    return wrapper_func

def jobseeker_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role == 'Job Seeker':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func
