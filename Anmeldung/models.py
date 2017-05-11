from django.db import models
import datetime
from django.utils.translation import ugettext as _


from Anmeldung.singleton import SingletonModel

from tinymce import HTMLField


class Event(models.Model):
    bezeichnung = models.CharField(max_length=200)
    registrationdeadline = models.DateField('Sichtbar bis einschl.',default=datetime.date.today)
    beginn = models.DateField(default=datetime.date.today)
    ende = models.DateField(default=datetime.date.today)
    kurzbeschreibung = HTMLField('Kurze Beschreibung')
    beschreibung = HTMLField('Beschreibung')
    oeffentlich = models.BooleanField('Öffentliche Veranstaltung bzw. noch Plätze frei',default=True)
    eventplaetze = models.PositiveSmallIntegerField("Plätze für Teilnehmer", default=0)
    schlafplaetze = models.PositiveSmallIntegerField("Plätze für Übernachtung",default=0)
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
    #
    ANREDEFRAU = 'Frau'
    ANREDEHERR = 'Herr'
    ANREDECHOICES = (
        (ANREDEFRAU, 'Frau'),
        (ANREDEHERR, 'Herr'),
    )
    #
    #
    SLEEPEXTERN = 'EXTERN'
    SLEEPZELT = 'ZELT'
    SLEEPWOHNWAGEN = 'WOHNWAGEN'
    SLEEPINTERN = 'IMHAUS'
    SLEEPWARTELISTE = 'WARTELISTE'
    SLEEPCHOICES = (
        (SLEEPEXTERN, 'Ich wohne ausserhalb (Hotel o.ä.)'),
        (SLEEPZELT, 'Ich schlafe im Zelt'),
        (SLEEPWOHNWAGEN, 'Ich komme mit dem Wohnwagen o.ä.'),
        (SLEEPINTERN, 'Ich brauche einen Schlafplatz im Haus'),
        (SLEEPWARTELISTE, 'Alles belegt. Ich möchte auf die Warteliste')
    )
    #
    TRANSNONE = 'NONE'
    TRANSENGLSIH = 'ENGLISH'
    TRANSFRENCH = 'FRENCH'
    TRANSCHOICES = (
        (TRANSNONE, ""),
        (TRANSENGLSIH, "I need an English translation"),
        (TRANSFRENCH, "J'ai besoin d'une traduction en français"),
    )
    TRAVELBAHN = 'BAHN'
    TRAVELBAHNPICKUP = 'BAHNPICKUP'
    TRAVELAUTO = 'AUTO'
    TRAVELBYPICKUP = 'MITFAHRER'
    TRAVELCHOICES = (
        (TRAVELBAHN, 'Ich fahre Bahn'),
        (TRAVELBAHNPICKUP, 'Ich fahre Bahn und möchte am Bahnhof abgeholt werden.'),
        (TRAVELAUTO, 'Ich komme mit dem Auto'),
        (TRAVELBYPICKUP, 'Ich bin Mitfahrer')
    )


    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    anrede = models.CharField(max_length=15, default='',choices=ANREDECHOICES)
    titel = models.CharField(max_length=15, blank=True, default='')
    name = models.CharField(max_length=40)
    vorname = models.CharField(max_length=40)
    strasse = models.CharField('Straße und Hausnummer',max_length=60)
    plz = models.CharField(max_length=8)
    ort = models.CharField(max_length=40)
    land = models.CharField(max_length=40,blank=True, default='')
    email = models.EmailField()
    telefon = models.CharField(max_length=20,blank=True)
    bemerkung = models.TextField(blank=True,default='')
    anreisedatum = models.DateField(default=datetime.date.today)
    abreisedatum = models.DateField(default=datetime.date.today)
    verkehrsmittel = models.CharField('Ich reise an mit',max_length=40,choices=TRAVELCHOICES,default=TRAVELBAHN)
    mitfahrplaetze = models.PositiveSmallIntegerField('Ich biete Mitfahrgelegenheiten für', default=0)
    businessaddress = models.BooleanField('Geschäftsadresse',default=False)
    verpflegung = models.CharField('Verpflegung', max_length=43, choices=ESSENCHOICE, default=ESSENEXTERN)
    unterbringung = models.CharField('Unterbringung', max_length=43, choices=SLEEPCHOICES, default=SLEEPEXTERN)
    uebersetzung = models.BooleanField('Ich brauche eine Übersetzung',default=False)
    uebersetzungen = models.CharField('Art der Übersetzung', max_length=40, choices=TRANSCHOICES, default=TRANSNONE)

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
    datepublishedstart = models.DateField('Veröffentlichung von',default=datetime.date.today)
    datepublishedend = models.DateField('Veröffentlichung bis',default=datetime.date.today)

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
