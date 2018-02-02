from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from .views import UserFormView,login_view, logout_view


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', UserFormView.as_view(), name = 'register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]