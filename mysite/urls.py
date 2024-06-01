"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('chat/', include('chat.urls')),
    path('feed/', include('feed.urls')),
    path('network/', include('network.urls')),
    path('posts/', include('posts.urls')),
    path('blogs/', include('articles.urls')),
    path('resources/', include('resources.urls')),
    path('projects/', include('projects.urls')),
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')), # app 
    path("__reload__/", include("django_browser_reload.urls")), # tailwind auto reload
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

