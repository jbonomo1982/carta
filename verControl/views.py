from django.shortcuts import render, render_to_response
from .models import Determinacion, Corrida, Control, ValFabr
from .forms import IngresoCorrida
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.models import Span
import numpy as np
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    deter = Determinacion.objects.all()
    return render(request, 'verControl/index.html', {'deter':deter})

@login_required
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

def graficoCorr(request, det, co):
    #busca por determinación, control
    grupo=[] #toma los datos del control a graficar para ponerlo en una tabla
    #Se ordenan por fecha de largada
    query = Corrida.objects.filter(determinacion=det).filter(control=co)
    x= query.values_list('fecha', flat=True)
    x= list(x)
    y= query.values_list('valor', flat=False)
    y=list(y)
    title = 'Carta'

    for l in x:
        form = l.strftime("%d, %B, %Y")
        grupo.append(form)

    for i in range(len(grupo)): #puebla la lista
        grupo[i] = grupo[i],y[i]
    
    r =query.all().values_list('determinacion', flat=True)
    c= query.all().values_list('control', flat=True)
    res = r[0]
    con = c[0]
    det = Determinacion.objects.get(pk=res)
    cont= Control.objects.get(pk=con)

    #buscar los valores de fábrica (sd y media)
    valRef = ValFabr.objects.filter(control=con).get(deter=res)
    media = valRef.media
    sd = valRef.sd

    sd1A= media+sd
    sd2A= media+sd*2
    sd1D= media -sd
    sd2D= media - sd*2




    plot = figure(title= title , 
        x_axis_label= 'fecha', 
        y_axis_label= 'conc.', 
        plot_width =600,
        plot_height =400,
        x_axis_type="datetime",
        )
    
    #mejorar el grafico

    plot.line(x, y, legend= cont.nom, line_width = 2)
    plot.circle(x,y,fill_color="blue", size=10)
    plot.line(x, media, line_width=2, line_dash="dashed", line_color="green", legend="media")
    #Store components 
    script, div = components(plot)

    div2 = grupo
    div3 = det.nombre

    #Feed them to the Django template.
    return render_to_response( 'verControl/graficoT.html',
            {'script' : script , 'div' : div, 'div2': div2, 'div3': div3} )



def control(request):
    controles=Control.objects.all()
    return render(request,'verControl/control.html',{'controles': controles})

def controlDetalle(request, pk):
    det=[]
    control = get_object_or_404(Control, pk=pk)
    corr = Corrida.objects.filter(control=pk).values_list('determinacion', flat=True)
    corr=list(corr)
    for c in corr:
        de= Determinacion.objects.get(pk=c)
        det.append(de)
    det=set(det)
    
    return render(request, 'verControl/controlDetalle.html', {'control': control, 'deter':det})

