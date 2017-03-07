from django.db import models
from ckeditor.fields import RichTextField
from datetime import date
from django.utils import timezone


# Create your models here.


class Event(models.Model):
	bezeichnung = models.CharField(max_length=200)
	registrationdeadline = models.DateField(null=True)
	beginn = models.DateField(null=True)
	ende = models.DateField(null=True)
	kurzbeschreibung = RichTextField()
	beschreibung = RichTextField(blank=True, default='')
	oeffentlich = models.BooleanField(default=True)

	def __str__(self):
		return self.bezeichnung

	ordering = ['+beginn']

class Teilnehmer(models.Model):
	event = models.ForeignKey(Event,on_delete=models.CASCADE)
	anrede = models.CharField(max_length=15, default='')
	titel = models.CharField(max_length=15, blank=True, default='')
	name = models.CharField(max_length=40)
	vorname = models.CharField(max_length=40)
	strasse = models.CharField(max_length=60)
	plz = models.CharField(max_length=8)
	ort = models.CharField(max_length=40)
	land = models.CharField(max_length=40,blank=True, default='')
	email = models.EmailField(blank=True,default='')
	telefon = models.CharField(max_length=20)
	bemerkung = models.TextField(blank=True,default='')
	anreisedatum = models.DateField(null=True)
	abreisedatum = models.DateField(null=True)

	def __str__(self):
		return self.name

	ordering = ['+name']

class texte(models.Model):
	bereich = models.CharField(max_length=50)
	headertext = models.CharField(max_length=50)
	langtext = RichTextField()

	def __str__(self):
		return self.headertext
