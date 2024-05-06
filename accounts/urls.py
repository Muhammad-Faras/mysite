from django.urls import path
from .views import profile_view, other_user_profileview, custom_login_redirect
app_name = 'accounts'
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('other_userprofile/<int:id>', other_user_profileview, name='other_userprofile'),
    path('custom-login-redirect/', custom_login_redirect, name='custom_login_redirect'),
]