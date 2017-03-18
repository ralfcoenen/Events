from django.contrib import admin
from django.utils.html import format_html

from .models import Event, Teilnehmer, texte, UserSettings
from djqscsv import render_to_csv_response


from filebrowser.sites import site

site.directory = "uploads/"


class TeilnehmerInline(admin.StackedInline):
    model = Teilnehmer
    extra = 3
    fieldsets = [
                (None,             {'fields': ['name', 'vorname']}),
                ('Adress-Daten',   {'fields': ['strasse', 'plz', 'ort', 'email',
                                               'telefon', 'bemerkung'], 'classes': ['collapse']})
              ]
    ordering = ['name']


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['bezeichnung', 'oeffentlich', 'beginn', 'ende', 'registrationdeadline']}),
        ('kurze Beschreibung',  {'fields': ['kurzbeschreibung'], 'classes': ['collapse']}),
        ('Beschreibung',        {'fields': ['beschreibung'], 'classes': ['collapse']}),
    ]
    inlines = [TeilnehmerInline]
    actions = ['exportliste']
    list_display = ('bezeichnung', 'beginn', 'ende', 'registrationdeadline')

    def exportliste(self, request, queryset):
        rs = queryset.values('bezeichnung', 'teilnehmer__anrede', 'teilnehmer__titel',
                             'teilnehmer__name', 'teilnehmer__vorname', 'teilnehmer__strasse',
                             'teilnehmer__plz', 'teilnehmer__ort',
                             'teilnehmer__email', 'teilnehmer__telefon', 'teilnehmer__anreisedatum',
                             'teilnehmer__abreisedatum', 'teilnehmer__bemerkung')
        return render_to_csv_response(rs, delimiter=';')


class texteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['bereich', 'hoehe', 'headertext', 'datepublishedstart',
                                            'datepublishedend']}),
        ('Text',                {'fields': ['langtext'], 'classes': ['collapse']}),
    ]

    list_display = ('headertext', 'bereich', 'hoehe', 'datepublishedstart', 'datepublishedend')


class usersettingsAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,              {'fields': ['senden', 'emails_to', 'email_antworttext_teilnehmer',
                                            'email_antworttext_organisation']})
    ]

    #   def has_add_permission(self, request):
    #       # Add Button muss weg, weil sonst versehntlich überschrieben wird
    #       return False


admin.site.register(Event, EventAdmin)
admin.site.register(texte, texteAdmin)
admin.site.register(UserSettings, usersettingsAdmin)
admin.site.site_header = 'Ekayana-Institut'
