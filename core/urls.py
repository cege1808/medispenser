from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.create_user, name = 'register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='profile/edit'),
    path('profile/schedule', views.schedule_view, name='profile/schedule'),
    path('profile/medication', views.medication, name='profile/medication'),
    path('profile/medication/new', views.new_medication, name='profile/medication/new'),
    path('profile/medication/edit', views.edit_medication, name='profile/medication/edit'),
    path('profile/medication/delete', views.delete_medication, name='profile/medication/delete'),
    path('demo/', views.demo, name='demo'),
]