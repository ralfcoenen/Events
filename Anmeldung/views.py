from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Anmeldung.models import Event, Teilnehmer, texte, UserSettings
from .forms import TeilnehmerForm
from datetime import date

import urllib.request
import json

from django.conf import settings
from django.contrib import messages

from django.core.mail import send_mail, send_mass_mail
import string

from django.template import engines, Context, Template

#------------------------------------------------------------

def testbase2(request):
    events = Event.objects.filter(registrationdeadline__gte=date.today()).order_by('beginn')
    links = texte.objects.filter(bereich__exact='LEFT',datepublishedstart__lte=date.today(),datepublishedend__gte=date.today()).order_by('-datepublishedstart')
    rechts = texte.objects.filter(bereich__exact='RIGHT',datepublishedstart__lte=date.today(),datepublishedend__gte=date.today()).order_by('-datepublishedstart')
    return render(request, 'Anmeldung/event_detail.html', {'events': events, 'links': links, 'rechts': rechts})
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
    setts = UserSettings.objects.get()

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

                """
                  Anmweldung war erfolgreich, sende nun die Emails

                """

                # Objecte in Dicts
                eventDict=event.__dict__
                settsDict=setts.__dict__
                # Dicts zusamenfassen, alles in settsDict
                settsDict.update(eventDict)
                # SettsDict um Formulareingaben ergänzen
                settsDict['anrede']=form.cleaned_data['anrede']
                settsDict['titel']=form.cleaned_data['titel']
                settsDict['vorname']=form.cleaned_data['vorname']
                settsDict['name']=form.cleaned_data['name']
                settsDict['strasse']=form.cleaned_data['strasse']
                settsDict['land']=form.cleaned_data['land']
                settsDict['plz']=form.cleaned_data['plz']
                settsDict['ort']=form.cleaned_data['ort']
                settsDict['telefon']=form.cleaned_data['telefon']
                settsDict['email']=form.cleaned_data['email']
                settsDict['bemerkung']=form.cleaned_data['bemerkung']
                # Aus Dict wird Context
                ctx = Context(settsDict)
                # Bau die Engine und gemeriere template
                engine = engines['django']
                template = engine.from_string(settsDict['email_antworttext'])
                nachricht = template.render(ctx)
                # mesage 1
                #

                betreff = 'Neue Anmeldung für ' + event.bezeichnung
                """
                nachricht = ' '.join(['Vielen Dank!\n',
                                    'Sie haben sich erfolgreich für die Veranstaltung ', '"',event.bezeichnung ,'"', ' angemeldet!\n\n',
                                    'Ihre Daten sind wie folgt erfasst worden:\n\n',
                                    form.cleaned_data['vorname'], form.cleaned_data['name'], '\n',
                                    form.cleaned_data['strasse'], '\n',
                                    form.cleaned_data['land'], form.cleaned_data['plz'], form.cleaned_data['ort'], '\n',
                                    form.cleaned_data['telefon'], '\n',
                                    form.cleaned_data['email'],'\n',
                                    form.cleaned_data['bemerkung'],
                                    setts.email_antworttext,
                                ])
                """
                von = setts.emails_to
                an = [form.cleaned_data['email']]
                message1=(betreff,nachricht,von,an)
                #
                # mesage 2
                #
                betreff = 'Neue Anmeldung für ' + event.bezeichnung
                """
                nachricht = ' '.join(['Es gibt eine neue Anmeldung: \n',
                                      '-----------------------------\n\n'
                                      'Vielen Dank!\n',
                                      'Sie haben sich erfolgreich für die Veranstaltung', '"',event.bezeichnung ,'"', 'angemeldet!\n\n',
                                      'Ihre Daten sind wie folgt erfasst worden:\n\n',
                                      form.cleaned_data['vorname'], form.cleaned_data['name'], '\n',
                                      form.cleaned_data['strasse'], '\n',
                                      form.cleaned_data['land'], form.cleaned_data['plz'], form.cleaned_data['ort'], '\n',
                                      form.cleaned_data['telefon'], '\n',
                                      form.cleaned_data['email'],'\n',
                                      form.cleaned_data['bemerkung']
                                ])
                """
                nachricht ='Es gibt eine neue Anmeldung: \n-----------------------------\n\n' + nachricht
                von = setts.emails_to
                an = [setts.emails_to]
                message2 = (betreff,nachricht,von,an)
                #
                #  Sende Alle eMails auf einmal
                #

                send_mass_mail((message1, message2),fail_silently=False)

                return redirect('teilnehmer_neu',pk=pk)
                #events = Event.objects.filter(registrationdeadline__gte=date.today()).order_by('beginn')
                #return render(request, 'Anmeldung/event_detail.html', {'events': events })

            else:
                messages.error(request, 'Falsches reCAPTCHA! Bitte nochmal versuchen!')
                return redirect('teilnehmer_neu',pk=pk)
    else:
        form = TeilnehmerForm()
    return render(request, 'Anmeldung/teilnehmer_neu.html',{'form': form, 'event': event, 'setts': setts})
