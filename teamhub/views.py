# coding: utf-8
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from teamhub.models import Aufgabe, Projekt
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
    return render_to_response('templates/base.html', context)

def logoutUser(request):
    '''
    Meldet den Anwender vom System ab und leitet auf die Login-Seite weiter.
    '''
    return logout_then_login(request, '/login/')

def projektListe(request):
    projektliste = Projekt.objects.all()
    context = {'projektliste': projektliste}
    return render_to_response('templates/base_projekt.html', context)

def projektDetail(request, projektId):
    '''
    Erstellt die Detailansicht eines Projekts.
    '''
    projekt = Projekt.objects.get(pk=projektId)
    context = {'projekt': projekt}
    return render_to_response('templates/base_projekt_detail.html', context)

def projektErstellen(request):
    from teamhub.forms import projektForm
    
    if request.method == 'POST':
        form = projektForm(request.POST)
        if form.is_valid():
            newProject = form.save()
            return redirect('/projekte/'+ str(newProject.pk) + '/')
    else:
        form = projektForm()
        
    context = {'form': form}
    return render_to_response('templates/base_projekt_bearbeiten.html', context, context_instance=RequestContext(request))

def projektBearbeiten(request, projektId):
    from teamhub.forms import projektForm
    
    projekt = Projekt.objects.get(pk=projektId)
    
    if request.method == 'POST':
        form = projektForm(request.POST, instance = projekt)
        if form.is_valid():
            form.save()
            return redirect('/projekte/'+ projektId + '/')
    else:
        form = projektForm(instance = projekt)
        
    context = {'form': form}
    return render_to_response('templates/base_projekt_bearbeiten.html', context, context_instance=RequestContext(request))
        
def aufgabeDetails(request, aufgabeId):
    '''
    Erstellt die Detailansicht für eine Aufgabe.
    '''
    aufgabe = Aufgabe.objects.get(pk=aufgabeId)
    context = {'aufgabe': aufgabe}
    return render_to_response('templates/base_aufgabe.html', context)

def userProfilBearbeiten(request):
    '''
    Erstellt die Bearbeitungsansicht für das Profil des angemeldeten Benutzers.
    '''
    from teamhub.forms import profilForm
    
    user = User.objects.get(pk=request.user.pk)
    
    if request.method == 'POST':
        form = profilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profil/')
    else:
        form = profilForm(instance=user)
        
    context = {'form': form}
    return render_to_response('templates/base_profil.html', context, context_instance=RequestContext(request))
