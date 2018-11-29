from django.urls import path, include
from verControl import views


urlpatterns = [
    path('', views.index, name='index'),
    path('corrida/nueva',views.corridaNueva, name='corridaNueva'),
    path('corrida',views.corrida,name='corrida'),
    path('corrida/<int:pk>/', views.corridaDetalle, name='corridaDetalle'),
    path('grafico/<int:det>/<int:co>/',views.graficoCorr, name='grafico'),
    path('control', views.control,name='control'),
    path('control/<int:pk>/',views.controlDetalle,name='controlDetalle'),
    path('accounts/', include('django.contrib.auth.urls')),
]
