from django.urls import path
from .views import project_view, create_project_view,project_detail_view, project_update_view, project_delete_view


app_name = 'projects'
urlpatterns = [
    path('', project_view, name='projects'),
    path('create/', create_project_view, name='create_project'),
    path('detail/<int:id>', project_detail_view, name='project_detail'),
    path('update/<int:id>', project_update_view, name='project_update'),
    path('delete/<int:id>', project_delete_view, name='project_delete'),
]