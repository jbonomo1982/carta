from django.shortcuts import render, render_to_response
from .models import Determinacion, Corrida, Control, ValFabr
from .forms import IngresoCorrida
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.models import Span, Label
import numpy as np
from datetime import datetime
from django.contrib.auth.decorators import login_required
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from django.template import RequestContext


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
    query = Corrida.objects.filter(determinacion=det).filter(control=co).order_by('fecha')
    x= query.values_list('fecha', flat=True)
    x= list(x)
    y= query.values_list('valor', flat=False)
    y=list(y)
    title = 'Carta'

    for l in x:
        form = l.strftime("%x %X")
        grupo.append(form)

    for i in range(len(grupo)): #puebla la lista
        r = y[i][0]
        grupo[i] = grupo[i],r


    #Buscar la media acumulada de las corridas:
    valArray = np.array(y)
    div4 = np.mean(valArray)

    #Buscar el desvio standard:

    div5 = np.std(valArray)
    
    r =query.all().values_list('determinacion', flat=True)
    c= query.all().values_list('control', flat=True)
    res = r[0]
    con = c[0]
    det = Determinacion.objects.get(pk=res)
    cont= Control.objects.get(pk=con)

    #busca los valores de fábrica (sd y media)
    valRef = ValFabr.objects.filter(control=con).get(deter=res)
    media = valRef.media
    sd = valRef.sd

    sd1A= media+sd
    sd2A= media+sd*2
    sd1D= media -sd
    sd2D= media - sd*2
    sd3A= media + sd*3
    sd3D= media - sd*3


    #Se instancia el grafico

    plot = figure(title= title , 
        x_axis_label= 'fecha', 
        y_axis_label= 'conc.', 
        plot_width =800,
        plot_height =600,
        x_axis_type="datetime",
        )
    

    plot.line(x, y, legend= cont.nom, line_width = 2)
    plot.circle(x,y,fill_color="blue", size=10)
    plot.line(x, media, line_width=2, line_dash="dashed", line_color="green", legend="media")
    
    #Se marcan los SD
    def3d = Span(location=sd3D,
                              dimension='width', line_color='red',
                              line_dash='solid', line_width=3)


    l3d= Label(x=0, y=sd3D, x_units='screen', text='3SD', render_mode='css',
      border_line_color='black', border_line_alpha=1.0,)
    
    def3a = Span(location=sd3A,
                              dimension='width', line_color='red',
                              line_dash='solid', line_width=3)


    l3a= Label(x=0, y=sd3A,x_units='screen', text='3SD', render_mode='css',
      border_line_color='black', border_line_alpha=1.0,)

    def2d = Span(location=sd2D,
                              dimension='width', line_color='brown',
                              line_dash='dotted', line_width=2)


    l2d= Label(x=0, y=sd2D, x_units='screen', text='2SD', render_mode='css',
      border_line_color='black', border_line_alpha=1.0,)

    
    def2a = Span(location=sd2A,
                              dimension='width', line_color='brown',
                              line_dash='dotted', line_width=2)


    l2a= Label(x=0, y=sd2A, x_units='screen', text='2SD', render_mode='css',
      border_line_color='black', border_line_alpha=1.0,)

    def1a = Span(location=sd1A,
                              dimension='width', line_color='orange',
                              line_dash='dotted', line_width=2)


    l1a= Label(x=0, y=sd1A, x_units='screen', text='1SD', render_mode='css',
      border_line_color='black', border_line_alpha=1.0,)


    def1d = Span(location=sd1D,
                              dimension='width', line_color='orange',
                              line_dash='dotted', line_width=2)


    l1d= Label(x=0, y=sd1D, x_units='screen', text='1SD', render_mode='css',
      border_line_color='black', border_line_alpha=1.0,)

    
    plot.add_layout(def3d)
    plot.add_layout(l3d)
    plot.add_layout(def3a)
    plot.add_layout(l3a)
    plot.add_layout(def2d)
    plot.add_layout(l2d)
    plot.add_layout(def2a)
    plot.add_layout(l2a)
    plot.add_layout(def1a)
    plot.add_layout(l1a)
    plot.add_layout(def1d)
    plot.add_layout(l1d)
    
    
    #Store components 
    script, div = components(plot)


    div2 = grupo
    div3 = det.nombre


    return render(request,'verControl/graficoT.html',{'script':script,'div':div, 'div2':div2,
     'div3':div3,'div4':div4, 'div5':div5})



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

