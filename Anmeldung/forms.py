from django import forms

from .models import Teilnehmer, Event

class TeilnehmerForm(forms.ModelForm):

    class Meta:
        model = Teilnehmer

        fields = ('anrede','titel','name','vorname','businessaddress','strasse',
                  'plz','ort','land','telefon','email','verpflegung','unterbringung',
                  'bemerkung')

        help_texts = {
            'businessaddress': ('Bitte geben Sie dazu im folgenden Ihre Geschäftsadresse ein'),
            'unterbringung': ('Unsere Schlafplätze im Haus sind noch sehr knapp. Falls Sie dennoch im Haus übernachten möchten, wählen Sie bitte die Warteliste und geben Sie Ihre Gründe dazu als Bemerkung ein.'),
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
            s = Teilnehmer.objects.filter(event__id=pk, unterbringung = 'IMHAUS').count()
            v = Teilnehmer.objects.filter(event__id=pk, verpflegung = 'INTERN').count()

            Felder=Event.objects.values_list('essensplaetze','schlafplaetze').filter(id=pk)

            if Felder[0][0] <= v:
                new_choices = list(self.fields['verpflegung'].choices)
                new_choices.remove(('Ich nehme an der Verpflegung teil','Ich nehme an der Verpflegung teil'))
                self.fields['verpflegung'].choices = new_choices
                self.fields['verpflegung'].widget.choices = new_choices
            else:
                #
                # WARTELISTE Raus

                new_choices = list(self.fields['verpflegung'].choices)
                new_choices.remove(('Alles belegt. Ich möchte auf die Warteliste', 'Alles belegt. Ich möchte auf die Warteliste'))
                self.fields['verpflegung'].choices = new_choices
                self.fields['verpflegung'].widget.choices = new_choices



            if Felder[0][1] <= s:
                new_choices = list(self.fields['unterbringung'].choices)
                new_choices.remove(('IMHAUS','Ich brauche einen Schlafplatz im Haus'))
                self.fields['unterbringung'].choices = new_choices
                self.fields['unterbringung'].widget.choices = new_choices
            else:
                #
                # WARTELISTE Raus

                new_choices = list(self.fields['unterbringung'].choices)
                new_choices.remove(('WARTELISTE', 'Alles belegt. Ich möchte auf die Warteliste'))
                self.fields['unterbringung'].choices = new_choices
                self.fields['unterbringung'].widget.choices = new_choices




