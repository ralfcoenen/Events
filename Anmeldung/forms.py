from django import forms

from .models import Teilnehmer

class TeilnehmerForm(forms.ModelForm):

    class Meta:
        model = Teilnehmer
        fields = ('name','vorname','strasse','plz','ort','email','anreisedatum','abreisedatum')
