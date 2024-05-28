from django.urls import path
from .views import home_view, terms_of_service_view,privacy_policy_view
app_name = 'home'
urlpatterns = [
    path('', home_view,name='home'),
    path('pyacademia/terms-of-service/', terms_of_service_view,name='terms-of-service'),
    path('pyacademia/privacy-policy/', privacy_policy_view,name='privacy_policy'),
]