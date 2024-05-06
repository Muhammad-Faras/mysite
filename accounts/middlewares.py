from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if user is authenticated and not trying to access profile related pages
        if request.user.is_authenticated and not request.path.startswith('/accounts/profile'):
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                # Check if the user's profile is complete
                if not profile.is_complete():
                    # Redirect to the profile completion page
                    return redirect(reverse('accounts:profile'))

        return response
