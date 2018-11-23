from django.shortcuts import render
from .models import Determinacion, Corrida
from .forms import IngresoCorrida
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone


# Create your views here.

def index(request):
    deter = Determinacion.objects.all()
    return render(request, 'verControl/index.html', {'deter':deter})


def corridaNueva(request):
        
        if request.method == "POST":
            form = IngresoCorrida(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.fecha = timezone.now()
                post.save()
                pk = str(post.pk)
                return redirect('/corrida/'+pk)
        else:
            form = IngresoCorrida()
        return render(request, 'verControl/corridaForm.html', {'form': form})

def corrida(request):
    corrida = Corrida.objects.all()
    return render(request,'verControl/corrida.html',{'corrida': corrida})

def corridaDetalle(request, pk):
    corrida = get_object_or_404(Corrida, pk=pk)
    return render(request, 'verControl/corridaDetalle.html', {'corrida': corrida})


