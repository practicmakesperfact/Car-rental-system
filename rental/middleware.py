# rental/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class EnsureProfileCompleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'customprofile'):
                profile = request.user.customprofile
                if not profile.is_complete():
                    if request.path not in [reverse('complete_profile'), reverse('logout')]:
                        return redirect('complete_profile')
        return self.get_response(request)
