from django.urls import path
from django.views.generic.base import TemplateView
from . import views
# from .views import login_view, logout_view, edit_profile, create_user

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.create_user, name = 'register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='profile/edit'),
    path('profile/medication', views.med_info, name='profile/medication'),
    path('profile/schedule', views.schedule_view, name='profile/schedule'),
    path('demo/', views.demo, name='demo'),
]