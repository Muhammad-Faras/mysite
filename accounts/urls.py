from django.urls import path
from .views import follow_view,unfollow_view,profile_view,about_view,create_profile_view,custom_login_redirect, CustomPasswordChangeView


app_name = 'accounts'
urlpatterns = [
    path('profile/<int:id>', profile_view, name='profile'),
    path('profile/<int:user_id>/about/', about_view, name='profile_about'),
    path('create_profile/', create_profile_view, name='create_profile'),
    path('custom-login-redirect/', custom_login_redirect, name='custom_login_redirect'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('follow-user/<int:id>', follow_view, name='follow'),
    path('unfollow-user/<int:id>', unfollow_view, name='unfollow'),
]