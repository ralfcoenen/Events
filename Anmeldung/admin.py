import csv
from django.contrib import admin
from django.http import HttpResponse
from filebrowser.sites import site
from modeltranslation.admin import TranslationAdmin

from .models import Event, Teilnehmer, texte, UserSettings
from django.db.models import Q

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.shapes import *
import io
from datetime import timedelta, date
from time import strftime

# from djqscsv import render_to_csv_response
#
#  Nur für Test-Zwecke
#

site.directory = "uploads/"


class TeilnehmerInline(admin.StackedInline):
    model = Teilnehmer
    extra = 0
    fieldsets = [
        (None, {'fields': ['anrede','name', 'vorname']}),
        ('Adress-Daten Privat', {'fields': ['strasse', 'plz', 'ort'], 'classes': ['collapse']}),
        ('Adress-Daten Business',
         {'fields': ['businessaddress', 'bustrasse', 'buplz', 'buort'], 'classes': ['collapse']}),
        ('sonstiges', {
            'fields': ['email', 'telefon', 'anreisedatum', 'abreisedatum', 'uebersetzungen', 'verkehrsmittel',
                       'unterbringung', 'wohnenimhaus', 'verpflegung', 'bemerkung'], 'classes': ['collapse']})
    ]
    ordering = ['name']
    save_on_top = True
    save_as = True


class EventAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    readonly_fields = ('AnzahlTeilnehmer', 'AnzahlEssen', 'AnzahlWarteliste',)
    fieldsets = [
        (None, {'fields': ['bezeichnung', 'oeffentlich', 'sichtbar', 'beginn', 'ende', 'registrationdeadline',
                           'eventplaetze', 'essensplaetze']}),
        ('kurze Beschreibung', {'fields': ['kurzbeschreibung'], 'classes': ['collapse']}),
        ('Beschreibung', {'fields': ['beschreibung'], 'classes': ['collapse']}),
    ]
    inlines = [TeilnehmerInline]
    actions = ['exportliste', 'gesamtbericht']
    list_display = (
        'bezeichnung', 'beginn', 'ende', 'registrationdeadline', 'AnzahlTeilnehmer', 'AnzahlEssen', 'AnzahlWarteliste',)
    save_on_top = True
    save_as = True

    #
    # ReportLab
    #
    PAGE_HEIGHT = A4[1]
    PAGE_WIDTH = A4[0]
    styles = getSampleStyleSheet()

    def AnzahlTeilnehmer(self, obj):
        return obj.teilnehmer_set.count()

    def AnzahlEssen(self, obj):
        return Event.objects.filter(id=obj.id).filter(
            teilnehmer__verpflegung='Ich nehme an der Verpflegung teil').count()

    def AnzahlWarteliste(self, obj):
        return Event.objects.filter(id=obj.id).filter(
            teilnehmer__verpflegung='Alles belegt. Ich möchte auf die Warteliste').count()

    def exportliste(self, request, queryset):
        rs = queryset.values('bezeichnung', 'teilnehmer__anrede', 'teilnehmer__titel',
                             'teilnehmer__name', 'teilnehmer__vorname',
                             'teilnehmer__strasse', 'teilnehmer__plz', 'teilnehmer__ort',
                             'teilnehmer__businessaddress', 'teilnehmer__bustrasse', 'teilnehmer__buplz',
                             'teilnehmer__buort',
                             'teilnehmer__email', 'teilnehmer__telefon', 'teilnehmer__anreisedatum',
                             'teilnehmer__abreisedatum', 'teilnehmer__uebersetzungen', 'teilnehmer__verpflegung',
                             'teilnehmer__verkehrsmittel',
                             'teilnehmer__unterbringung', 'teilnehmer__wohnenimhaus', 'teilnehmer__bemerkung')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        fieldnames = ['bezeichnung', 'teilnehmer__anrede', 'teilnehmer__titel',
                      'teilnehmer__name', 'teilnehmer__vorname',
                      'teilnehmer__strasse', 'teilnehmer__plz', 'teilnehmer__ort',
                      'teilnehmer__businessaddress', 'teilnehmer__bustrasse', 'teilnehmer__buplz', 'teilnehmer__buort',
                      'teilnehmer__email', 'teilnehmer__telefon', 'teilnehmer__anreisedatum',
                      'teilnehmer__abreisedatum', 'teilnehmer__uebersetzungen', 'teilnehmer__verpflegung',
                      'teilnehmer__verkehrsmittel',
                      'teilnehmer__unterbringung', 'teilnehmer__wohnenimhaus', 'teilnehmer__bemerkung'
                      ]

        writer = csv.DictWriter(response, fieldnames=fieldnames, delimiter=";", dialect="excel")
        writer.writeheader()

        for e in rs:
            # e['teilnehmer__bemerkung'] = e['teilnehmer__bemerkung'].replace('\r',' ').replace('\n','')
            writer.writerow(e)

        return response

    def berichtsteil(self, e, menu_pdf, elements, data, styles, ueberschrift):
        elements.append(Spacer(10, 5 * mm))
        elements.append(Paragraph(ueberschrift+' (Anzahl=' + str(len(data)-1) + '):', styles['Heading3']))
        t = Table(data,style=[('LINEBELOW', (0,0),(data[0].__len__()-1,0),1,colors.black)],)
        elements.append(t)
        elements.append(Spacer(10, 10 * mm))

        return 1

    def mytemplate(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(10 * mm, 15 * mm, "Seite %d  - %s" % (doc.page, "Stand: " + date.today().strftime("%d.%m.%Y")))
        canvas.restoreState()

    def gesamtbericht(self, request, queryset):
        # response erstellen
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'attachment; filename=Gesamtbericht'
        buff = io.BytesIO()
        menu_pdf = SimpleDocTemplate(buff, rightMargin=20*mm, leftMargin=30*mm, topMargin=20*mm, bottomMargin=30*mm,)

        elements = []
        styles = getSampleStyleSheet()

        # Hier kommt der Content


        # Für jedes ausgewählte Event
        for e in queryset:

            alle_teilnehmer = e.teilnehmer_set.values('name', 'vorname', 'email', 'anreisedatum', 'abreisedatum')
            if len(alle_teilnehmer) > 0:
                #
                # Teilnehmerliste
                #
                data = []
                for t in alle_teilnehmer:
                    data.append([t['name'] + ', ' + t['vorname'], t['email'], t['anreisedatum'].strftime("%d.%m.%Y"), t['abreisedatum'].strftime("%d.%m.%Y")])
                if len(data) > 0:
                    elements.append(Paragraph(e.bezeichnung , styles['Heading1']))
                    elements.append(Paragraph("Stand: " + date.today().strftime("%d.%m.%Y"), styles['Heading3']))
                    d = Drawing(100, 1)
                    d.add(Line(0, 0, menu_pdf.width, 0))
                    elements.append(d)
                    # header
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles,'Teilnehmerliste')
                #
                # Essensplätze
                #
                essensplaetze = Teilnehmer.objects.filter(event=e.pk).filter(verpflegung = 'Ich nehme an der Verpflegung teil').values('name', 'vorname', 'email', 'anreisedatum', 'abreisedatum')
                data = []
                for t in essensplaetze:
                    data.append([t['name'] + ', ' + t['vorname'], t['email'], t['anreisedatum'].strftime("%d.%m.%Y"), t['abreisedatum'].strftime("%d.%m.%Y")])
                if len(data) > 0:
                    # header
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles,'Teilnahme an der Verpflegung')
                    # Küchenplan
                    plan = {}
                    for t in range((e.ende - e.beginn).days + 1):
                        plan[e.beginn + timedelta(t)] = 0
                    for t, v in plan.items():
                        for w in essensplaetze:
                            if w['anreisedatum'] <= t <= w['abreisedatum']:
                                plan[t] = plan[t] + 1
                    data = []
                    for k, v in sorted(plan.items()):
                        data.append([k.strftime("%d.%m.%Y     =  "), v])
                    elements.append(Spacer(10, 5 * mm))
                    elements.append(Paragraph('Personen in der Verpflegung:', styles['Heading3']))
                    t = Table(data)
                    elements.append(t)
                    elements.append(Spacer(10, 10 * mm))
                #
                #  parkplätze
                #
                parkplaetze = Teilnehmer.objects.filter(event=e.pk).filter(verkehrsmittel='Auto').values(
                    'name', 'vorname', 'email', 'anreisedatum', 'abreisedatum')
                data = []
                for t in parkplaetze:
                    data.append([t['name'] + ', ' + t['vorname'], t['email'], t['anreisedatum'].strftime("%d.%m.%Y"), t['abreisedatum'].strftime("%d.%m.%Y")])
                if len(data) > 0:
                    # header
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles,'Es kommen mit dem Auto')
                #
                # Abholung am Bahnhof
                #
                z2 = Teilnehmer.objects.filter(event=e.pk).filter(
                    Q(verkehrsmittel="Bahn mit Abholung"))
                data = []
                for t in z2:
                    data.append([t.name + ', ' + t.vorname, t.email, t.anreisedatum.strftime("%d.%m.%Y"),
                                 t.abreisedatum.strftime("%d.%m.%Y"), t.unterbringung])
                if len(data) > 0:
                    # header
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum','Unterbringung'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles, 'Am Bahnhof abzuholen')
                #
                # Zeltplätze
                #

                # Mit Q-Objetcs lassen sich ODER Abfragen realisiern, wogegen sonst Filter-Chaining als UND abgebildet wird
                z2 = Teilnehmer.objects.filter(event=e.pk).filter(Q(unterbringung="Zelt") | Q(unterbringung="Wohnwagen u.ä."))
                data = []
                for t in z2:
                    data.append([t.name + ', ' + t.vorname, t.email, t.anreisedatum.strftime("%d.%m.%Y"),
                                 t.abreisedatum.strftime("%d.%m.%Y"), t.unterbringung])
                if len(data) > 0:
                    # header
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum', 'Unterbringung'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles, 'Übernachtung im Zelt oder Wohnwagen')
                #
                # Hotels
                #
                z2 = Teilnehmer.objects.filter(event=e.pk).filter(
                    Q(unterbringung="Extern"))
                data = []
                for t in z2:
                    data.append([t.name + ', ' + t.vorname, t.email, t.anreisedatum.strftime("%d.%m.%Y"),
                                 t.abreisedatum.strftime("%d.%m.%Y")])
                if len(data) > 0:
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles, 'Übernachtung Extern')
                #
                # Übersetzungen
                #
                z2 = Teilnehmer.objects.filter(event=e.pk).filter(
                    Q(uebersetzungen="Englisch") | Q(uebersetzungen="Französisch"))
                data = []
                for t in z2:
                    data.append([t.name + ', ' + t.vorname, t.email, t.anreisedatum.strftime("%d.%m.%Y"),
                                 t.abreisedatum.strftime("%d.%m.%Y"), t.uebersetzungen])
                if len(data) > 0:
                    # header
                    data.insert(0, ['Name, Vorname', 'eMail', 'Anreisedatum', 'Abreisedatum', 'Übersetzung'])
                    self.berichtsteil(e, menu_pdf, elements, data, styles, 'Gewünschte Übersetzungen')


                # fertig mit dem Event
                elements.append(PageBreak())

        menu_pdf.build(elements, onFirstPage=self.mytemplate, onLaterPages=self.mytemplate)
        response.write(buff.getvalue())
        buff.close()
        return response


class TeilnehmerAdmin(admin.ModelAdmin):
    actions = ['Rechnung']
    fieldsets = [
        (None, {'fields': ['name', 'vorname']}),
        ('Adress-Daten Privat', {'fields': ['strasse', 'plz', 'ort', 'land'], 'classes': ['collapse']}),
        ('Adress-Daten Business',
         {'fields': ['businessaddress', 'bustrasse', 'buplz', 'buort'], 'classes': ['collapse']}),
        ('sonstiges', {
            'fields': ['email', 'telefon', 'anreisedatum', 'abreisedatum', 'uebersetzungen', 'verkehrsmittel',
                       'unterbringung', 'wohnenimhaus', 'verpflegung', 'bemerkung'], 'classes': ['collapse']})
    ]
    ordering = ['name']
    list_display = ('name', 'vorname', 'email', 'Eventbezeichnung')
    list_filter = ('event__bezeichnung',)
    search_fields = ('name', 'email')
    save_on_top = True
    save_as = True

    def Eventbezeichnung(self, obj):
        return obj.event.bezeichnung

    def Rechnung(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'attachment; filename="rechnung.pdf"'

        # Create the PDF object, using the response object as its "file."
        offset = 100
        p = canvas.Canvas(response)
        for i in queryset:
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(100, offset, i.name)

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            offset += 100

        p.save()
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
        (None, {'fields': ['bereich', 'hoehe', 'headertext', 'datepublishedstart',
                           'datepublishedend']}),
        ('Text', {'fields': ['langtext'], 'classes': ['collapse']}),
    ]

    list_display = ('headertext', 'bereich', 'hoehe', 'datepublishedstart', 'datepublishedend')
    save_on_top = True
    save_as = True


class usersettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['senden', 'emails_to',
                           # 'email_antworttext_teilnehmer','email_antworttext_organisation',
                           'htmltext_teilnehmer', 'htmltext_organisation']})
    ]

    save_on_top = True

    def has_add_permission(self, request):
        # Add Button muss weg, weil sonst versehentlich überschrieben wird
        return False


admin.site.register(Event, EventAdmin)
admin.site.register(texte, texteAdmin)
admin.site.register(UserSettings, usersettingsAdmin)
admin.site.register(Teilnehmer, TeilnehmerAdmin)
admin.site.site_header = 'Ekayana-Institut'
