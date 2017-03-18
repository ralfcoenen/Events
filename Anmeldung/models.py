from django.db import models
from ckeditor.fields import RichTextField
from datetime import date


from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from imagekit.utils import get_field_info
from Anmeldung.singleton import SingletonModel

from tinymce import HTMLField

# Create your models here.

class Event(models.Model):
    bezeichnung = models.CharField(max_length=200)
    registrationdeadline = models.DateField('Sichtbar bis einschl.',null=True)
    beginn = models.DateField(null=True)
    ende = models.DateField(null=True)
    kurzbeschreibung = HTMLField('Kurze Beschreibung')
    beschreibung = HTMLField('Beschreibung')
    oeffentlich = models.BooleanField('Öffentliche Veranstaltung bzw. noch Plätze frei',default=True)

    class Meta:
        verbose_name = 'Veranstaltung'
        verbose_name_plural = 'Veranstaltungen'


    def __str__(self):
        return self.bezeichnung

    ordering = ['+beginn']

class Teilnehmer(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    anrede = models.CharField(max_length=15, default='')
    titel = models.CharField(max_length=15, blank=True, default='')
    name = models.CharField(max_length=40)
    vorname = models.CharField(max_length=40)
    strasse = models.CharField('Straße und Hausnummer',max_length=60)
    plz = models.CharField(max_length=8)
    ort = models.CharField(max_length=40)
    land = models.CharField(max_length=40,blank=True, default='')
    email = models.EmailField(blank=True,default='')
    telefon = models.CharField(max_length=20,blank=True)
    bemerkung = models.TextField(blank=True,default='')
    anreisedatum = models.DateField(null=True,blank=True)
    abreisedatum = models.DateField(null=True, blank=True)

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
    datepublishedstart = models.DateField('Veröffentlichung von',default=date.today)
    datepublishedend = models.DateField('Veröffentlichung bis',default=date.today)

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
