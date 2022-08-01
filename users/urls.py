from . import views
from django.urls import path

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('register', views.registerUser, name='register'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('account', views.account, name='account'),
    path('edit-profile', views.editProfile, name='edit-profile'),
    path('add-skill', views.addSkill, name='add-skill'),
    path('edit-skill/<str:pk>', views.editSkill, name='edit-skill'),
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete-skill')
]

