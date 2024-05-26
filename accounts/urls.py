from django.urls import path
from .views import main_skill_view,sub_skill_view,follow_view,unfollow_view,profile_view,create_profile_view, other_user_profileview, custom_login_redirect, CustomPasswordChangeView


app_name = 'accounts'
urlpatterns = [
    path('profile/<int:id>', profile_view, name='profile'),
    path('create_profile/', create_profile_view, name='create_profile'),
    path('other_userprofile/<int:id>', other_user_profileview, name='other_userprofile'),
    path('custom-login-redirect/', custom_login_redirect, name='custom_login_redirect'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('follow-user/<int:id>', follow_view, name='follow'),
    path('unfollow-user/<int:id>', unfollow_view, name='unfollow'),
    path('main-skill/', main_skill_view, name='main_skill'),
    path('sub-skill/', sub_skill_view, name='sub_skill'),
]