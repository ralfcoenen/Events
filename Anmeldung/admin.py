from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
#from modeltranslation.admin import TranslationStackedInline
#from django.utils.html import format_html
import csv
from django.http import HttpResponse

from .models import Event, Teilnehmer, texte, UserSettings
#from djqscsv import render_to_csv_response


from filebrowser.sites import site

site.directory = "uploads/"


class TeilnehmerInline(admin.StackedInline):
    model = Teilnehmer
    extra = 0
    fieldsets = [
                    (None,                      {'fields': ['name', 'vorname']}),
                    ('Adress-Daten Privat',     {'fields': ['strasse', 'plz', 'ort'], 'classes': ['collapse']}),
                    ('Adress-Daten Business',   {'fields': ['businessaddress','bustrasse', 'buplz', 'buort'], 'classes': ['collapse']}),
                    ('sonstiges',               {'fields': ['email','telefon', 'anreisedatum','abreisedatum','uebersetzungen','verkehrsmittel','unterbringung','wohnenimhaus','verpflegung','bemerkung'], 'classes': ['collapse']})
              ]
    ordering = ['name']
    save_on_top = True
    save_as = True


class EventAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    fieldsets = [
        (None,                  {'fields': ['bezeichnung', 'oeffentlich', 'sichtbar', 'beginn', 'ende', 'registrationdeadline','eventplaetze', 'essensplaetze']}),
        ('kurze Beschreibung',  {'fields': ['kurzbeschreibung'], 'classes': ['collapse']}),
        ('Beschreibung',        {'fields': ['beschreibung'], 'classes': ['collapse']}),
    ]
    inlines = [TeilnehmerInline]
    actions = ['exportliste']
    list_display = ('bezeichnung', 'beginn', 'ende', 'registrationdeadline')
    save_on_top = True
    save_as = True


    def exportliste(self, request, queryset):

        rs = queryset.values('bezeichnung', 'teilnehmer__anrede', 'teilnehmer__titel',
                             'teilnehmer__name', 'teilnehmer__vorname',
                             'teilnehmer__strasse', 'teilnehmer__plz', 'teilnehmer__ort',
                             'teilnehmer__businessaddress','teilnehmer__bustrasse', 'teilnehmer__buplz', 'teilnehmer__buort',
                             'teilnehmer__email', 'teilnehmer__telefon', 'teilnehmer__anreisedatum',
                             'teilnehmer__abreisedatum', 'teilnehmer__uebersetzungen','teilnehmer__verpflegung',
                             'teilnehmer__unterbringung','teilnehmer__wohnenimhaus','teilnehmer__bemerkung')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        fieldnames = [ 'bezeichnung', 'teilnehmer__anrede', 'teilnehmer__titel',
                             'teilnehmer__name', 'teilnehmer__vorname',
                             'teilnehmer__strasse', 'teilnehmer__plz', 'teilnehmer__ort',
                             'teilnehmer__businessaddress','teilnehmer__bustrasse', 'teilnehmer__buplz', 'teilnehmer__buort',
                             'teilnehmer__email', 'teilnehmer__telefon', 'teilnehmer__anreisedatum',
                             'teilnehmer__abreisedatum', 'teilnehmer__uebersetzungen','teilnehmer__verpflegung',
                             'teilnehmer__unterbringung','teilnehmer__wohnenimhaus','teilnehmer__bemerkung'
                     ]

        writer = csv.DictWriter(response,fieldnames=fieldnames, delimiter=';', dialect='excel')
        writer.writeheader()

        for e in rs:
            writer.writerow(e)

        return response



class texteAdmin(TranslationAdmin):

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    fieldsets = [
        (None,                  {'fields': ['bereich', 'hoehe', 'headertext', 'datepublishedstart',
                                            'datepublishedend']}),
        ('Text',                {'fields': ['langtext'], 'classes': ['collapse']}),
    ]

    list_display = ('headertext', 'bereich', 'hoehe', 'datepublishedstart', 'datepublishedend')
    save_on_top = True
    save_as = True


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
