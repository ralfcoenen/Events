from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from Anmeldung.models import Event, Teilnehmer


def index(request):
    return HttpResponse("Willkommen zur Anmeldung.")

def event_list(request):
    events = Event.objects.all()
    return render(request, 'Anmeldung/event_list.html', {'events': events})

def event_teilnehmer(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'Anmeldung/event_teilnehmer.html', {'event': event})
