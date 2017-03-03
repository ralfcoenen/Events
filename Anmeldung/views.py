from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Anmeldung.models import Event, Teilnehmer

from .forms import TeilnehmerForm


def index(request):
    return HttpResponse("Willkommen zur Anmeldung.")

def event_list(request):
    events = Event.objects.all()
    return render(request, 'Anmeldung/event_list.html', {'events': events})

def event_teilnehmer(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'Anmeldung/event_teilnehmer.html', {'event': event})

def teilnehmer_neu(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method=="POST":
        form = TeilnehmerForm(request.POST)
        if form.is_valid():
            teilnehmer = form.save(commit=False)
            teilnehmer.event=event
            teilnehmer.save()
            return redirect('event_teilnehmer',pk=event.pk)
    else:
        form = TeilnehmerForm()
    return render(request, 'Anmeldung/teilnehmer_neu.html',{'form': form})
