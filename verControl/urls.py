from django.urls import path
from verControl import views

urlpatterns = [
    path('', views.index, name='index'),
]
