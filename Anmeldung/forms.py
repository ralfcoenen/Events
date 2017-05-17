from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Teilnehmer, Event

class TeilnehmerForm(forms.ModelForm):

    class Meta:
        model = Teilnehmer

        # fields = '__all__'
        # exclude = ['event']
        fields = ('anrede','titel','vorname','name','strasse',
              'plz','ort','land','businessaddress','bustrasse','buplz','buort','buland','telefon','email', 'uebersetzungen', 'verkehrsmittel', 'verpflegung',
              'bemerkung')

        help_texts = {
            'businessaddress': (_('Bitte geben Sie dazu im folgenden Ihre Geschäftsadresse ein')),
            'uebersetzungen' : (_('Bitte bringen Sie ein FM-Radio als Empfänger für die Übersetzung mit. Android und IOS bieten entsprechende Apps an.')),
        }


    def __init__(self, *args, **kwargs):
        super(TeilnehmerForm, self).__init__(*args, **kwargs)
        #
        # Hier gehört eine Datenbankabfrage hin um die restlichen Schlaf- und
        # Essensplätze abzufragen
        # ----------------------------------------------------------
        #

        # Hier werden die Auswahlen in dem Formen manipuliert
        # falls alle Plätze belegt sind.
        #
        if len(kwargs) > 0:
            pk=kwargs['initial']['pk']
            v = Teilnehmer.objects.filter(event__id=pk, verpflegung = 'Ich nehme an der Verpflegung teil').count()

            Felder=Event.objects.values_list('essensplaetze').filter(id=pk)

            if Felder[0][0] <= v:
                new_choices = list(self.fields['verpflegung'].choices)
                # Lösche Tuple
                new_choices.remove(('Ich nehme an der Verpflegung teil',_('Ich nehme an der Verpflegung teil')))
                self.fields['verpflegung'].choices = new_choices
                self.fields['verpflegung'].widget.choices = new_choices
            else:
                #
                # WARTELISTE Raus

                new_choices = list(self.fields['verpflegung'].choices)
                # Lösche Tuple
                new_choices.remove(('Alles belegt. Ich möchte auf die Warteliste',_('Alles belegt. Ich möchte auf die Warteliste')))
                self.fields['verpflegung'].choices = new_choices
                self.fields['verpflegung'].widget.choices = new_choices





