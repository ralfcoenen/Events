from django.contrib import admin

from .models import Event, Teilnehmer, texte
from djqscsv import write_csv, render_to_csv_response

class TeilnehmerInline(admin.StackedInline):
   model = Teilnehmer
   extra = 3



class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['bezeichnung','oeffentlich','beginn','ende','registrationdeadline']}),
        #('Von Bis',             {'fields': ['beginn','ende'], 'classes': ['collapse']}),
        ('kurze Beschreibung',  {'fields': ['kurzbeschreibung']}),
        ('Beschreibung',         {'fields': ['beschreibung']}),
    ]
    inlines = [TeilnehmerInline]
    actions = ['exportliste']
    list_display = ('bezeichnung','beginn','ende','registrationdeadline')

    def exportliste(self, request, queryset):
        rs = queryset.values('bezeichnung','teilnehmer__anrede','teilnehmer__titel','teilnehmer__name','teilnehmer__vorname','teilnehmer__strasse','teilnehmer__plz','teilnehmer__ort','teilnehmer__email','teilnehmer__telefon','teilnehmer__anreisedatum','teilnehmer__abreisedatum','teilnehmer__bemerkung')
        return render_to_csv_response(rs,delimiter=';')

class texteAdmin(admin.ModelAdmin):
    list_display = ('bereich','headertext','datepublishedstart','datepublishedend')

admin.site.register(Event,EventAdmin)
admin.site.register(texte,texteAdmin)
admin.site.site_header = 'Ekayana-Institut'
