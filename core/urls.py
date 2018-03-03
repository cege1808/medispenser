from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from .views import login_view, logout_view, edit_profile, create_user, med_info, schedule_view


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', create_user, name = 'register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', edit_profile, name='profile/edit'),
    path('profile/medication', med_info, name='profile/medication'),
    path('profile/schedule', schedule_view, name='profile/schedule')
]