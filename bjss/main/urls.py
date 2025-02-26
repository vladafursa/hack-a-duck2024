from django.urls import path, include
from . import views
from .views import register, login, option_view
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('option/', option_view, name='option'),  # Map the option view
]

