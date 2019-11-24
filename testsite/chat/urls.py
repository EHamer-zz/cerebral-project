from django.urls import path

from . import views

urlpatterns = [
    path('view', views.view, name='view'),
    path('connect', views.connect, name='connect'),
    path('', views.index, name='index'),
]