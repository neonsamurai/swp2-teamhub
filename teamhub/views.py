# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from teamhub.models import Aufgabe
# Create your views here.

@login_required
def dashboard(request):
    '''
    Erstellt die Dashboardansicht mit den dafür nötigen Daten:
        * Meine zugewiesenen Tickets
        * Meine zugewiesenen Projekte
    '''
    meineAufgaben = Aufgabe.objects.filter(bearbeiter=request.user).order_by('faelligkeitsDatum')
    context = {'meineAufgaben': meineAufgaben}
    return render_to_response('../templates/base.html', context)

def aufgabeDetails(request, aufgabeId):
    '''
    Erstellt die Detailansicht für eine Aufgabe.
    '''
    aufgabe = Aufgabe.objects.get(pk=aufgabeId)
    context = {'aufgabe': aufgabe}
    return render_to_response('../templates/base_aufgabe.html', context)