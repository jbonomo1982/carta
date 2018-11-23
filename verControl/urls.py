from django.urls import path
from verControl import views


urlpatterns = [
    path('', views.index, name='index'),
    path('corrida/nueva',views.corridaNueva, name='corridaNueva'),
    path('corrida',views.corrida,name='corrida'),
    path('corrida/<int:pk>/', views.corridaDetalle, name='corridaDetalle'),
]
