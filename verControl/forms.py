from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import ModelForm
from .models import Corrida
    
class IngresoCorrida(ModelForm):
    class Meta:
        model = Corrida
        fields = ['determinacion', 'control','valor']

    