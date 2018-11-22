from django.shortcuts import render
from .models import Determinacion

# Create your views here.

def index(request):
    deter = Determinacion.objects.all()
    return render(request, 'verControl/index.html', {'deter':deter})
