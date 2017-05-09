from django.db import models
import datetime


from Anmeldung.singleton import SingletonModel

from tinymce import HTMLField

# Create your models here.

class Event(models.Model):
    bezeichnung = models.CharField(max_length=200)
    registrationdeadline = models.DateField('Sichtbar bis einschl.',default=datetime.date.today)
    beginn = models.DateField(default=datetime.date.today)
    ende = models.DateField(default=datetime.date.today)
    kurzbeschreibung = HTMLField('Kurze Beschreibung')
    beschreibung = HTMLField('Beschreibung')
    oeffentlich = models.BooleanField('Öffentliche Veranstaltung bzw. noch Plätze frei',default=True)
    schlafplaetze = models.PositiveSmallIntegerField(default=0)
    essensplaetze = models.PositiveSmallIntegerField(default=0)

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
    ESSENCHOICE = (
        (ESSENEXTERN, 'Ich verpflege mich selbst'),
        (ESSENINTERN, 'Ich nehme an der Verpflegung teil'),
        (ESSENWARTELISTE, 'Alles belegt. Ich möchte auf die Warteliste'),
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
    businessaddress = models.BooleanField('Geschäftsadresse',default=False)
    verpflegung = models.CharField('Verpflegung', max_length=43, choices=ESSENCHOICE, default=ESSENEXTERN)
    unterbringung = models.CharField('Unterbringung', max_length=43, choices=SLEEPCHOICES, default=SLEEPEXTERN)

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
