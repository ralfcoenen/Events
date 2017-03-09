from django.db import models
from ckeditor.fields import RichTextField
from datetime import date
from django.utils import timezone

from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from imagekit.utils import get_field_info

# Create your models here.

# Generiert Bild_thumb nach User-Angabe der Bild_breite 
class BildThumbnail(ImageSpec):
    format = 'JPEG'
    options = {'quality': 60}

    @property
    def processors(self):
        model, field_name = get_field_info(self.source)
        return [ResizeToFit(model.bild_breite)]

register.generator('anmeldung:event:bild_thumbnail', BildThumbnail)


class Event(models.Model):
    bezeichnung = models.CharField(max_length=200)
    registrationdeadline = models.DateField('Sichtbar bis einschl.',null=True)
    beginn = models.DateField(null=True)
    ende = models.DateField(null=True)
    kurzbeschreibung = RichTextField()
    beschreibung = RichTextField(blank=True, default='')
    oeffentlich = models.BooleanField('Öffentliche Veranstaltung bzw. noch Plätze frei',default=True)
    bild_breite = models.IntegerField('Bild Breite (px)',default=350,null=True,blank=True)
    bild_hoehe = models.IntegerField('Bild Höhe (px)',default=150,null=True,blank=True)
    bild = models.ImageField(null=True,blank=True)
    bild_thumb = ImageSpecField(source='bild',id='anmeldung:event:bild_thumbnail')

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
    BEREICHCHOICES = (
    (LEFTCONTENT, 'linke Spalte'),
    (RIGHTCONTENT, 'rechte Spalte'),
    )
    bereich = models.CharField(max_length=5,choices=BEREICHCHOICES,default=LEFTCONTENT)
    headertext = models.CharField('Überschrift',max_length=50)
    langtext = RichTextField()
    datepublishedstart = models.DateField('Veröffentlichung von',default=date.today)
    datepublishedend = models.DateField('Veröffentlichung bis',default=date.today)

    def __str__(self):
        return self.headertext

    class Meta:
        verbose_name ='Texte'
        verbose_name_plural = 'Texte'
