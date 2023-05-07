# blog/urls.py
from django.urls import path
from . import views

app_name = 'signlanguage'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
]