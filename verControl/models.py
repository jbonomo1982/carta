from django.db import models
from django.utils import timezone

# Create your models here.
class Lote(models.Model):
    codigo= models.CharField(max_length=100,help_text="codigo que identifica el lote, dado por el fabricante.")
    fechaVenc = models.DateField(verbose_name="Fecha Vencimiento")
    def __str__(self):
        return self.codigo


class Equipo(models.Model):
    nombre = models.CharField(max_length=100,help_text="nombre del Equipo -- Cómo lo identifica el laboratorio")
    fabricante = models.CharField(max_length=100,null=True,blank=True)
    descripcion = models.TextField(null=True, blank=True,help_text="Se puede dar el nombre del equipo, modelo, u otra particularidad del mismo")
    def __str__(self):
        return self.nombre


class Control(models.Model):
    nom = models.CharField(max_length=100,help_text="nombre del control")
    fabricante = models.CharField(max_length=100,null=True,blank=True)
    enUso = models.BooleanField(default=True, help_text="si el control es el que actualmente se usa en las corridas")
    lote = models.ForeignKey(Lote,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom + self.lote.__str__()
    



class Determinacion(models.Model):
    nombre = models.CharField(max_length=100,help_text="nombre de la determinación")
    fabricante = models.CharField(max_length=100,null=True,blank=True)
    codigo = models.CharField(max_length=100,null=True, blank=True,help_text="identificación dada por el fabricante")
    unidades = models.CharField(max_length=100,help_text="unidades con que se informa la determinación")
    equipo = models.ForeignKey(Equipo,on_delete=models.CASCADE, help_text="Equipo en que se procesa la determinación, si se procesa en diversos equipos cada equipo tiene su determinación.")

    def __str__(self):
        return self.nombre


    


class ValAcu(models.Model):
    control= models.ForeignKey(Control,on_delete=models.CASCADE)
    deter = models.ForeignKey(Determinacion,on_delete=models.CASCADE)
    media = models.FloatField()
    sd = models.FloatField()

    def acumular(self):
        """Hacer metodo para que tomando los valores de las corridas
        de esta determinacion y control cambien la media y los desvios--
        toma los valores de la corrida si esta tiene como valido=True
        """
        pass




class ValFabr(models.Model):
    control= models.ForeignKey(Control,on_delete=models.CASCADE)
    deter = models.ForeignKey(Determinacion,on_delete=models.CASCADE)
    media = models.FloatField(help_text="El valor de la media que informa el fabricante")
    sd = models.FloatField()
    

class Corrida(models.Model):
    fecha = models.DateTimeField()
    determinacion = models.ForeignKey(Determinacion, on_delete=models.CASCADE)
    control= models.ForeignKey(Control,on_delete=models.CASCADE)
    valor = models.FloatField(help_text="El valor del control en la corrida")
    valido = models.BooleanField(default=True, help_text="si el valor puede ser tomado para calcular media y sd acumulado")
    
    

