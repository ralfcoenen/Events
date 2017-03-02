from django.db import models

# Create your models here.
class Event(models.Model):
	bezeichnung = models.CharField(max_length=200)
	beginn = models.DateField(null=True)
	ende = models.DateField(null=True)

	def __str__(self):
		return self.bezeichnung

class Teilnehmer(models.Model):
	event = models.ForeignKey(Event,on_delete=models.PROTECT)
	name = models.CharField(max_length=40)
	vorname = models.CharField(max_length=40)
	strasse = models.CharField(max_length=60)
	plz = models.CharField(max_length=8)
	ort = models.CharField(max_length=40)
	email = models.EmailField(null=True)

	def __str__(self):
		return self.name
