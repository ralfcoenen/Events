from django.shortcuts import render, get_object_or_404, redirect
from Anmeldung.models import Event, texte, UserSettings
from .forms import TeilnehmerForm
from datetime import date

import urllib.request

from django.conf import settings
from django.contrib import messages

from django.core.mail import send_mail, send_mass_mail
import json
import string

from django.template import engines, Context, Template


# ------------------------------------------------------------


def uebersicht(request):
    events = Event.objects.filter(registrationdeadline__gte=date.today()).order_by('beginn')
    links = texte.objects.filter(bereich__exact='LEFT',
                                 datepublishedstart__lte=date.today(),
                                 datepublishedend__gte=date.today()).order_by('-datepublishedstart')
    rechts = texte.objects.filter(bereich__exact='RIGHT',
                                  datepublishedstart__lte=date.today(),
                                  datepublishedend__gte=date.today()).order_by('-datepublishedstart')
    oben = texte.objects.filter(bereich__exact='LEFT',
                                hoehe__exact='TOP',
                                datepublishedstart__lte=date.today(),
                                datepublishedend__gte=date.today()).order_by('-datepublishedstart')
    unten = texte.objects.filter(bereich__exact='LEFT',
                                 hoehe__exact='BOTTOM',
                                 datepublishedstart__lte=date.today(),
                                 datepublishedend__gte=date.today()).order_by('-datepublishedstart')
    return render(request, 'Anmeldung/event_detail.html',
                  {'events': events, 'links': links, 'rechts': rechts, 'oben': oben, 'unten': unten})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'Anmeldung/event_detail.html', {'event': event})


def teilnehmer_neu(request, pk):
    # Bootstrap benutzt 'danger'
    MESSAGE_TAGS = {messages.error: 'danger'}

    event = get_object_or_404(Event, pk=pk)
    setts = UserSettings.objects.get()

    if request.method == "POST":
        form = TeilnehmerForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            #End reCAPTCHA validation

            if result['success']:
                teilnehmer = form.save(commit=False)
                teilnehmer.event = event
                teilnehmer.save()
                messages.success(request, 'Neue Anmeldung erfolgreich durchgeführt!')

                if setts.senden:
                    """
                      Anmweldung war erfolgreich, sende nun die Emails
                    """
                    # Objecte in Dicts
                    eventDict = event.__dict__
                    settsDict = setts.__dict__
                    # Dicts zusamenfassen, alles in settsDict
                    settsDict.update(eventDict)
                    # SettsDict um Formulareingaben ergänzen
                    settsDict['anrede'] = form.cleaned_data['anrede']
                    settsDict['titel'] = form.cleaned_data['titel']
                    settsDict['vorname'] = form.cleaned_data['vorname']
                    settsDict['name'] = form.cleaned_data['name']
                    settsDict['businessaddress'] = form.cleaned_data['businessaddress']
                    settsDict['strasse'] = form.cleaned_data['strasse']
                    settsDict['land'] = form.cleaned_data['land']
                    settsDict['plz'] = form.cleaned_data['plz']
                    settsDict['ort'] = form.cleaned_data['ort']
                    settsDict['bustrasse'] = form.cleaned_data['bustrasse']
                    settsDict['buland'] = form.cleaned_data['buland']
                    settsDict['buplz'] = form.cleaned_data['buplz']
                    settsDict['buort'] = form.cleaned_data['buort']
                    settsDict['telefon'] = form.cleaned_data['telefon']
                    settsDict['email'] = form.cleaned_data['email']
                    settsDict['bemerkung'] = form.cleaned_data['bemerkung']
                    settsDict['verpflegung'] = form.cleaned_data['verpflegung']
                    settsDict['uebersetzungen'] = form.cleaned_data['uebersetzungen']
                    settsDict['unterbringung'] = form.cleaned_data['unterbringung']
                    settsDict['wohnenimhaus'] = form.cleaned_data['wohnenimhaus']
                    settsDict['anreisedatum'] = form.cleaned_data['anreisedatum']
                    settsDict['abreisedatum'] = form.cleaned_data['abreisedatum']
                    # Aus Dict wird Context
                    ctx = Context(settsDict)

                    # Bau die Engine und generiere templates
                    # engine = engines['django']
                    # template = engine.from_string(settsDict['email_antworttext_teilnehmer'])
                    # nachricht = template.render(ctx)
                    nachricht = 'Bitte Schalten Sie in die HTML-Ansicht für diese eMail'
                    nachricht_html=engines['django'].from_string(settsDict['htmltext_teilnehmer']).render(ctx)

                    nachricht2 = 'Bitte Schalten Sie in die HTML-Ansicht für diese eMail'
                    nachricht2_html = engines['django'].from_string(settsDict['htmltext_organisation']).render(ctx)

                    #
                    # mesage 1
                    #
                    betreff = 'Ihre Anmeldung für ' + event.bezeichnung
                    von = setts.emails_to
                    an = [form.cleaned_data['email']]
                    # message1 = (betreff, nachricht, von, an)
                    send_mail(betreff, nachricht, von, an, html_message=nachricht_html, fail_silently=False)
                    #
                    # mesage 2
                    #
                    betreff = 'Neue Anmeldung für ' + event.bezeichnung
                    von = setts.emails_to
                    an = [setts.emails_to]
                    # message2 = (betreff, nachricht, von, an)
                    send_mail(betreff, nachricht2, von, an, html_message=nachricht2_html, fail_silently=False)
                    #
                    #  Sende Alle eMails auf einmal
                    #
                    # send_mass_mail((message1, message2), fail_silently=False)



                return redirect('teilnehmer_neu', pk=pk)

            else:
                messages.error(request, 'Falsches reCAPTCHA! Bitte nochmal versuchen!')
                return redirect('teilnehmer_neu', pk=pk)
    else:
        form = TeilnehmerForm(initial = {'pk': pk})

    return render(request, 'Anmeldung/teilnehmer_neu.html', {'form': form, 'event': event, 'setts': setts})
