from django.urls import path
from . import views
from .views import UserFormView,login_view


urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('signup/', views.signup, name = 'signup'),
    path('register/', UserFormView.as_view(), name = 'register'),
    path('login/', login_view, name='login'),
]