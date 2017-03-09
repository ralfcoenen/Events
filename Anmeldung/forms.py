from django import forms

from .models import Teilnehmer

class TeilnehmerForm(forms.ModelForm):

    class Meta:
        model = Teilnehmer
        fields = ('anrede','titel','name','vorname','strasse','plz','ort','land','telefon','email','bemerkung')
