from django.contrib import admin
from .models import Control,Corrida, Determinacion,Equipo,ValAcu,ValFabr, Lote

# Register your models here.

admin.site.register(Control)
admin.site.register(Corrida)
admin.site.register(Determinacion)
admin.site.register(Equipo)
admin.site.register(ValAcu)
admin.site.register(ValFabr)
admin.site.register(Lote)