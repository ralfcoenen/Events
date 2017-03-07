from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Anmeldung.models import Event, Teilnehmer
from .forms import TeilnehmerForm
from datetime import date

import urllib.request
import json

from django.conf import settings
from django.contrib import messages


def testbase2(request):
    events = Event.objects.filter(registrationdeadline__gte=date.today()).order_by('beginn')
    return render(request, 'Anmeldung/event_detail.html', {'events': events })
"""
def event_list(request):
    events = Event.objects.filter(registrationdeadline__gte=date.today())
    return render(request, 'Anmeldung/event_list.html', {'events': events})
"""
def event_detail( request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'Anmeldung/event_detail.html', {'event': event})

def teilnehmer_neu(request,pk):
    # Bootstrap benutzt 'danger'
    MESSAGE_TAGS = {
        messages.error: 'danger'
    }
    event = get_object_or_404(Event,pk=pk)
    if request.method=="POST":
        form = TeilnehmerForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                teilnehmer = form.save(commit=False)
                teilnehmer.event=event
                teilnehmer.save()
                messages.success(request, 'Neue Anmeldung erfolgreich durchgeführt!')
                return redirect('teilnehmer_neu',pk=pk)
                #events = Event.objects.filter(registrationdeadline__gte=date.today()).order_by('beginn')
                #return render(request, 'Anmeldung/event_detail.html', {'events': events })

            else:
                messages.error(request, 'Falsches reCAPTCHA! Bitte nochmal versuchen!')
                return redirect('teilnehmer_neu',pk=pk)
    else:
        form = TeilnehmerForm()
    return render(request, 'Anmeldung/teilnehmer_neu.html',{'form': form, 'event': event})
