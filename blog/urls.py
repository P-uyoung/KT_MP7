from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name="list"),
    path('create/', views.create, name="create"),
    path('create/form/', views.create_form, name="create_form"),
    path('<id>/', views.detail, name="detail"),
]
