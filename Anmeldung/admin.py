from django.contrib import admin
from django.utils.html import format_html

from .models import Event, Teilnehmer, texte
from djqscsv import write_csv, render_to_csv_response

class TeilnehmerInline(admin.StackedInline):
   model = Teilnehmer
   extra = 3



class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['bezeichnung','oeffentlich','beginn','ende','registrationdeadline']}),
        #('Von Bis',             {'fields': ['beginn','ende'], 'classes': ['collapse']}),
        ('kurze Beschreibung',  {'fields': ['kurzbeschreibung'], 'classes': ['collapse']}),
        ('Beschreibung',        {'fields': ['beschreibung'], 'classes': ['collapse']}),
        ('Bild',                {'fields': ['bild_breite','bild','bild_display'], 'classes': ['collapse']}),
    ]
    readonly_fields = ['bild_display']
    inlines = [TeilnehmerInline]
    actions = ['exportliste']
    list_display = ('bezeichnung','beginn','ende','registrationdeadline')

    def exportliste(self, request, queryset):
        rs = queryset.values('bezeichnung','teilnehmer__anrede','teilnehmer__titel','teilnehmer__name','teilnehmer__vorname','teilnehmer__strasse','teilnehmer__plz','teilnehmer__ort','teilnehmer__email','teilnehmer__telefon','teilnehmer__anreisedatum','teilnehmer__abreisedatum','teilnehmer__bemerkung')
        return render_to_csv_response(rs,delimiter=';')

    def bild_display(self, obj):
        return format_html(u'<a href="{}"><img src="{}"></a>', obj.bild_thumb.url, obj.bild_thumb.url)
    bild_display.allow_tags = True

class texteAdmin(admin.ModelAdmin):
    filedsets = [
        (None,                  {'fields': ['bereich','headertext','datepublishedstart','datepublishedend',]}),
        ('Bild',                {'fields': ['bild_breite','bild','bild_display'], 'classes': ['collapse']}),
    ]
    def bild_display(self, obj):
        return format_html(u'<a href="{}"><img src="{}"></a>', obj.bild_thumb.url, obj.bild_thumb.url)
    bild_display.allow_tags = True
    readonly_fields = ['bild_display']
    list_display = ('headertext','bereich','datepublishedstart','datepublishedend')


admin.site.register(Event,EventAdmin)
admin.site.register(texte,texteAdmin)
admin.site.site_header = 'Ekayana-Institut'
