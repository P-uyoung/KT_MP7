# blog/urls.py
from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login, name='index'),
    path('add', views.add, name='add'),
]