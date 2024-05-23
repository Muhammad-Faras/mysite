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
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path("__reload__/", include("django_browser_reload.urls")), # tailwind auto reload
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

