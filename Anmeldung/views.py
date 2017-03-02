from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Willkommen zur Anmeldung.")

def event_list(request):
    return render(request, 'Anmeldung/event_list.html', {})
