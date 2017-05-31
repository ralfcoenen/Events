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


    readonly_fields = ('AnzahlTeilnehmer','AnzahlEssen','AnzahlWarteliste')
    fieldsets = [
            (None,    {'fields': ['bezeichnung', 'oeffentlich', 'sichtbar', 'beginn', 'ende', 'registrationdeadline','eventplaetze', 'essensplaetze']}),
            ('kurze Beschreibung',  {'fields': ['kurzbeschreibung'], 'classes': ['collapse']}),
            ('Beschreibung',        {'fields': ['beschreibung'], 'classes': ['collapse']}),
        ]
    inlines = [TeilnehmerInline]
    actions = ['exportliste']
    list_display = ('bezeichnung', 'beginn', 'ende', 'registrationdeadline', 'AnzahlTeilnehmer','AnzahlEssen','AnzahlWarteliste',)
    save_on_top = True
    save_as = True

    def AnzahlTeilnehmer(self, obj):
        return obj.teilnehmer_set.count()

    def AnzahlEssen(self, obj):
        return Event.objects.filter(id=obj.id).filter(teilnehmer__verpflegung='Ich nehme an der Verpflegung teil').count()

    def AnzahlWarteliste(self, obj):
        return Event.objects.filter(id=obj.id).filter(teilnehmer__verpflegung='Alles belegt. Ich möchte auf die Warteliste').count()

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
        writer = csv.DictWriter(response,fieldnames=fieldnames, delimiter=";", dialect="excel")
        writer.writeheader()

        for e in rs:
            # e['teilnehmer__bemerkung'] = e['teilnehmer__bemerkung'].replace('\r',' ').replace('\n','')
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
    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
            'all': ('Anmeldung/css/admin/my_own_admin.css',)
        }


    fieldsets = [
            (None,              {'fields': ['senden', 'emails_to',
                                            #'email_antworttext_teilnehmer','email_antworttext_organisation',
                                            'htmltext_teilnehmer','htmltext_organisation']})
    ]

    def has_add_permission(self, request):
        # Add Button muss weg, weil sonst versehntlich überschrieben wird
        return False


admin.site.register(Event, EventAdmin)
admin.site.register(texte, texteAdmin)
admin.site.register(UserSettings, usersettingsAdmin)
admin.site.site_header = 'Ekayana-Institut'
