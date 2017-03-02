from django.http import HttpResponse
from django.shortcuts import render
from Anmeldung.models import Event, Teilnehmer


def index(request):
    return HttpResponse("Willkommen zur Anmeldung.")

def event_list(request):
    events = Event.objects.all()
    return render(request, 'Anmeldung/event_list.html', {'events': events})
