from . import views
from django.urls import path


urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>', views.project, name='project'),
    path('add-project', views.addProject, name='add-project'),
    path('edit-project/<str:pk>', views.editProject, name='edit-project'),
    path('delete-project/<str:pk>', views.deleteProject, name='delete-project')
]


