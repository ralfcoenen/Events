from django.contrib import admin

from .models import Event, Teilnehmer
from djqscsv import write_csv, render_to_csv_response

class TeilnehmerInline(admin.TabularInline):
   model = Teilnehmer
   extra = 3


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['bezeichnung']}),
        ('Von Bis',             {'fields': ['beginn','ende'], 'classes': ['collapse']}),
        ('kurze Beschreibung',  {'fields': ['kurzbeschreibung'], 'classes': ['collapse']}),

        ('Beschreibung',         {'fields': ['beschreibung'], 'classes': ['collapse']}),
        ('Deadline für Anmeldungen', {'fields': ['registrationdeadline'], 'classes': ['collapse']}),

    ]
    inlines = [TeilnehmerInline]
    actions = ['exportliste']
    list_display = ('bezeichnung','beginn','ende','registrationdeadline')

    def exportliste(self, request, queryset):
        rs = queryset.values('bezeichnung','teilnehmer__name','teilnehmer__vorname','teilnehmer__strasse','teilnehmer__plz','teilnehmer__ort','teilnehmer__email','teilnehmer__anreisedatum','teilnehmer__abreisedatum')
        return render_to_csv_response(rs,delimiter=';')


admin.site.register(Event,EventAdmin)
#admin.site.register(Teilnehmer)
