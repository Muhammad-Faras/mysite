from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.startswith('/accounts/profile'):
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                if not profile.is_complete():
                    return redirect(reverse('accounts:profile'))

        return response
