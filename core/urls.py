from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.create_user, name = 'register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='profile/edit'),
    path('profile/medication/add', views.medication_add, name='profile/medication/add'),
    path('profile/schedule', views.schedule_view, name='profile/schedule'),
    path('profile/medication', views.medication_information, name='profile/medication'),
    path('demo/', views.demo, name='demo'),
]