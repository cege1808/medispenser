from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.create_user, name = 'register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='profile/edit'),
    path('profile/medication', views.show_medication, name='profile/medication'),
    path('profile/medication/new', views.new_medication, name='profile/medication/new'),
    path('profile/medication/edit', views.edit_medication, name='profile/medication/edit'),
    path('profile/medication/delete', views.delete_medication, name='profile/medication/delete'),
    path('profile/schedule', views.show_schedule, name='profile/schedule'),
    path('profile/schedule/new', views.new_schedule, name='profile/schedule/new'),
    path('profile/schedule/edit', views.edit_schedule, name='profile/schedule/edit'),
    path('profile/schedule/delete', views.delete_schedule, name='profile/schedule/delete'),
    path('profile/log', views.show_log, name='profile/log'),
    path('profile/log_add_row', views.log_add_row, name='profile/log_add_row'),
    path('demo/', views.demo, name='demo'),
]