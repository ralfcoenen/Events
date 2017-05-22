from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _


from Anmeldung.singleton import SingletonModel

from tinymce import HTMLField


class Event(models.Model):
    bezeichnung = models.CharField(max_length=200)
    registrationdeadline = models.DateField('Sichtbar bis einschl.',default=datetime.date.today)
    beginn = models.DateField(default=datetime.date.today)
    ende = models.DateField(default=datetime.date.today)
    kurzbeschreibung = HTMLField('Kurze Beschreibung', blank=True)
    beschreibung = HTMLField('Beschreibung', blank=True)
    oeffentlich = models.BooleanField('Öffentliche Veranstaltung bzw. noch Plätze frei',default=True)
    sichtbar = models.BooleanField('wird angezeigt',default=True)
    eventplaetze = models.PositiveSmallIntegerField("Plätze für Teilnehmer", default=0)
    essensplaetze = models.PositiveSmallIntegerField("Plätze für Teilnehmer an der Verpflegung", default=0)

    class Meta:
        verbose_name = 'Veranstaltung'
        verbose_name_plural = 'Veranstaltungen'

    def __str__(self):
        return self.bezeichnung

    ordering = ['+beginn']

class Teilnehmer(models.Model):
    #
    #  Choices einrichten
    #
    ESSENEXTERN = 'Ich verpflege mich selbst'
    ESSENINTERN = 'Ich nehme an der Verpflegung teil'
    ESSENWARTELISTE = 'Alles belegt. Ich möchte auf die Warteliste'
    #Translators: Auswahl im Anmeldeformular
    ESSENCHOICE = (
        (ESSENEXTERN, _('Ich verpflege mich selbst')),
        (ESSENINTERN, _('Ich nehme an der Verpflegung teil')),
        (ESSENWARTELISTE, _('Alles belegt. Ich möchte auf die Warteliste')),
    )
    #
    SLEEPNONE = ''
    SLEEPEXTERN = 'Extern'
    SLEEPZELT = 'Zelt'
    SLEEPWOHNWAGEN = 'Wohnwagen u.ä.'

    SLEEPCHOICES = (
        (SLEEPNONE, ''),
        (SLEEPEXTERN, 'Ich wohne im Hotel o.ä.'),
        (SLEEPZELT, 'Ich schlafe im Zelt'),
        (SLEEPWOHNWAGEN, 'Ich komme mit dem Wohnwagen o.ä.'),
    )
    #
    ANREDEFRAU = 'Frau'
    ANREDEHERR = 'Herr'
    ANREDECHOICES = (
        (ANREDEFRAU, _('Frau')),
        (ANREDEHERR, _('Herr')),
    )
    #
    #

    TRANSNONE = 'Keine'
    TRANSENGLISH = 'Englisch'
    TRANSFRENCH = 'Französisch'
    TRANSCHOICES = (
        (TRANSNONE, _("Keine")),
        (TRANSENGLISH, _("Ich brauche eine englische Übersetzung")),
        (TRANSFRENCH, _("Ich brauche eine französische Übersetzung")),
    )
    TRAVELBAHN = 'Bahn'
    TRAVELBAHNPICKUP = 'Bahn mit Abholung'
    TRAVELAUTO = 'Auto'
    TRAVELBYPICKUP = 'Mitfahrer'
    TRAVELCHOICES = (
        (TRAVELBAHN, _('Ich fahre Bahn')),
        (TRAVELBAHNPICKUP, _('Ich fahre Bahn und möchte am Bahnhof abgeholt werden.')),
        (TRAVELAUTO, _('Ich komme mit dem Auto')),
        (TRAVELBYPICKUP, _('Ich bin Mitfahrer'))
    )


    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    anrede = models.CharField(_('Anrede'),max_length=15, default='',choices=ANREDECHOICES)
    titel = models.CharField(_('Titel'),max_length=15, blank=True, default='')
    name = models.CharField(_('Familienname'),max_length=40)
    vorname = models.CharField(_('Vorname'),max_length=40)
    strasse = models.CharField(_('Straße und Hausnummer'),max_length=60)
    plz = models.CharField(_('Postleitzahl'),max_length=8)
    ort = models.CharField(_('Ort'),max_length=40)
    land = models.CharField(_('Land'),max_length=40,blank=True, default='')
    email = models.EmailField()
    telefon = models.CharField(_('Telefon'),max_length=20,blank=True)
    bemerkung = models.TextField(_('Bemerkung'),blank=True,default='')
    anreisedatum = models.DateField(_('Anreisedatum'),default=datetime.date.today)
    abreisedatum = models.DateField(_('Abreisedatum'),default=datetime.date.today)
    verkehrsmittel = models.CharField(_('Ich reise an mit'),max_length=40,choices=TRAVELCHOICES,default=TRAVELBAHN)
    businessaddress = models.BooleanField(_('Rechnungsadresse'),default=False)
    bustrasse = models.CharField(_('Rechnung Straße und Hausnummer'), max_length=60, blank=True, default='')
    buplz = models.CharField(_('Rechnung Postleitzahl'), max_length=8, blank=True, default='')
    buort = models.CharField(_('Rechnung Ort'), max_length=40, blank=True, default='')
    buland = models.CharField(_('Rechnung Land'), max_length=40, blank=True, default='')
    verpflegung = models.CharField(_('Verpflegung'), max_length=43, choices=ESSENCHOICE, default=ESSENEXTERN)
    wohnenimhaus = models.BooleanField(_('Ich möchte im Haus wohnen'), default=False)
    unterbringung = models.CharField(_('Unterbringung'),max_length=20,choices=SLEEPCHOICES,default=SLEEPNONE, blank=True)
    uebersetzungen = models.CharField(_('Art der Übersetzung'), max_length=40, choices=TRANSCHOICES, default=TRANSNONE)

    def __str__(self):
        return self.name

    ordering = ['+name']

    class Meta:
        verbose_name ='Teilnehmer'
        verbose_name_plural = 'Teilnehmer'

class texte(models.Model):
    LEFTCONTENT = 'LEFT'
    RIGHTCONTENT = 'RIGHT'
    COLCHOICES = (
    (LEFTCONTENT, 'linke Spalte'),
    (RIGHTCONTENT, 'rechte Spalte'),
    )
    TOPCONTENT = "TOP"
    BOTTOMCONTENT ="BOTTOM"
    ROWCHOICES = (
        (TOPCONTENT, 'Über den Terminen'),
        (BOTTOMCONTENT,'Unter den Terminen'),
    )
    bereich = models.CharField(max_length=5,choices=COLCHOICES,default=LEFTCONTENT)
    hoehe = models.CharField(max_length=6, choices=ROWCHOICES, default=BOTTOMCONTENT)
    headertext = models.CharField('Überschrift',max_length=50)
    langtext = HTMLField('Text')
    datepublishedstart = models.DateField(_('Veröffentlichung am'),default=datetime.date.today)
    datepublishedend = models.DateField(_('Veröffentlichung bis'),default=datetime.date.today)

    class Meta:
        ordering = ['datepublishedstart']

        verbose_name = 'Texte'
        verbose_name_plural = 'Texte'


    def __str__(self):
        return self.headertext


class UserSettings(SingletonModel):
    senden = models.BooleanField('E-Mails senden',default=True)
    emails_to = models.CharField(max_length=60,blank=True,null=True)
    email_antworttext_teilnehmer = models.TextField('Text für aut. eMail-Antwort an Teilnehmer',blank=True, default='')
    email_antworttext_organisation = models.TextField('Text für aut. eMail an Organisation bei neuer Anmeldung',blank=True, default='')

    def __str__(self):
        return 'Einstellung'

    class Meta:
        verbose_name = 'System-Einstellung'
        verbose_name_plural = 'System-Einstellungen'
