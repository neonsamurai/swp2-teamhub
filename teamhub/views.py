# coding: utf-8
"""
.. module:: views

:platform: Unix, Windows

:synopsis: Django views für teamhub Paket.

.. moduleauthor:: Veronika Gross


"""
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from teamhub.decorators import teamleiterBerechtigung, aufgabeBearbeitenBerechtigung
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from teamhub.models import Aufgabe, Projekt, AUFGABE_STATUS, TeamhubUser
import teamhub.stringConst as c
from django.utils import timezone


# Create your views here.


def makeContext(context):
    '''Fügt dem context Dictionary Standardwerte hinzu. Diese werden Seitenweit verwendet.

    :param context: Das Kontext-Dictionary, das standardisiert werden soll.

    :type context: Dictionary

    '''
    context['projektliste'] = Projekt.objects.all().order_by('name')
    context['prioritaet'] = [c.PRIORITAET_HI, c.PRIORITAET_ME, c.PRIORITAET_LO]
    context['dateNow'] = timezone.now()
    return context


@login_required
def dashboard(request):
    '''Die View der Startseite. Sie sammelt alle Aufgaben, die dem angemeldeten Benutzer zugewiesen sind.

'''

    meineAufgaben = Aufgabe.objects.filter(bearbeiter=TeamhubUser.objects.get(pk=request.user.pk)).order_by('faelligkeitsDatum')
    context = makeContext({'meineAufgaben': meineAufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    context['title'] = 'Meine Aufgaben'
    return render_to_response('base_aufgabe_liste.html', context, context_instance=RequestContext(request))


def offeneAufgabenAnzeigen(request):
    '''
    Diese View sammelt alle Aufgaben, die im Status "offen" stehen.
'''

    meineAufgaben = Aufgabe.objects.filter(status=c.AUFGABE_STATUS_OP).order_by('faelligkeitsDatum')
    context = makeContext({'meineAufgaben': meineAufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    context['title'] = 'Offene Aufgaben'
    return render_to_response('base_aufgabe_liste.html', context, context_instance=RequestContext(request))


def vonMirErstellteAufgaben(request):
    '''
    Diese View sammelt alle Aufgaben, deren Ersteller der angemeldete Benutzer ist.
    '''

    meineAufgaben = Aufgabe.objects.filter(ersteller=TeamhubUser.objects.get(pk=request.user.pk)).order_by('faelligkeitsDatum')
    context = makeContext({'meineAufgaben': meineAufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    context['title'] = 'Von mir erstellte Aufgaben'
    return render_to_response('base_aufgabe_liste.html', context, context_instance=RequestContext(request))


def logoutUser(request):
    '''Meldet den angemeldete Benutzer ab und leitet ihn auf die Loginseite weiter.
'''
    return logout_then_login(request, '/login/')


def aufgabeErstellen(request):

    '''Abhängig vom übergebenen Requesttyp erstellt diese View entweder ein neues Aufgabenobjekt,
    oder stellt ein Eingabeformular zum Erstellen eines Aufgabenobjekts bereit.
'''

    from teamhub.forms import aufgabeForm
    from teamhub.decorators import decorateSave
    template = 'base_aufgabe_bearbeiten.html'
    if request.method == 'POST':
        form = aufgabeForm(request.POST)
        if form.is_valid():
            @decorateSave
            def saveAufgabe(form_to_save, request, template):
                newAufgabe = form_to_save.save(commit=False)
                newAufgabe.ersteller = TeamhubUser.objects.get(pk=request.user.pk)
                newAufgabe.save()
                return redirect('/aufgabe/' + str(newAufgabe.pk) + '/')
            return saveAufgabe(form, request, template)
    else:
        form = aufgabeForm()
    context = makeContext({'form': form, "title": "Aufgabe Erstellen"})
    return render_to_response(template, context, context_instance=RequestContext(request))


@aufgabeBearbeitenBerechtigung
def aufgabeBearbeiten(request, aufgabeId):
    '''Abhängig vom übergebenen Requesttyp ändert diese View entweder ein Aufgabenobjekt,
    oder stellt ein Eingabeformular zum Verändern eines Aufgabenobjekts bereit.


    :param aufgabeId: Primärschlüssel des Aufgabenobjekts, welches verändert werden soll.

    :type aufgabeId: int
'''
    from teamhub.forms import aufgabeForm
    from teamhub.decorators import decorateSave

    template = 'base_aufgabe_bearbeiten.html'
    aufgabe = Aufgabe.objects.get(pk=aufgabeId)
    if request.method == 'POST':
        form = aufgabeForm(request.POST, instance=aufgabe)
        if form.is_valid():
            @decorateSave
            def saveAufgabe(form_to_save, request, template):

                Aufgabe = form_to_save.save(commit=False)
                if 'stati' in request.POST:
                    Aufgabe.status = request.POST['stati']
                Aufgabe.save()
                return redirect('/aufgabe/' + str(aufgabe.pk) + '/')
            return saveAufgabe(form, request, template)
    else:
        form = aufgabeForm(instance=aufgabe)

    context = makeContext({'form': form, "title": "Aufgabe bearbeiten", 'stati': aufgabe.getStati(), 'aktuellerstatus_lang': dict(AUFGABE_STATUS)[aufgabe.status], 'aktuellerstatus': aufgabe.status})

    return render_to_response(template, context, context_instance=RequestContext(request))


def projektListe(request):
    '''Erstellt eine Liste aller Projekte in der Datenbank.
'''
    projektliste = Projekt.objects.all()
    context = {'projektliste': projektliste}
    return render_to_response('base_projekt.html', context, context_instance=RequestContext(request))


def projektDetail(request, projektId):
    '''Erstellt die Detailansicht eines Projekts.

    :param projektId: Der Primärschlüssel des angezeigten Projekts.

    :type projektId: int
'''
    projekt = Projekt.objects.get(pk=projektId)
    aufgaben = Aufgabe.objects.filter(projekt=projekt).order_by('faelligkeitsDatum')
    context = makeContext({'projekt': projekt, 'aufgaben': aufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    return render_to_response('base_projekt_detail.html', context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def projektErstellen(request):
    '''Abhängig vom Requesttyp erstellt diese View entweder ein neues Projektobjekt oder stellt ein Formular
    bereit, mit dem ein neues Projektobjekt erstellt werden kann.
'''
    from teamhub.forms import projektFormErstellen
    from teamhub.decorators import decorateSave

    template = 'base_projekt_erstellen.html'
    if request.method == 'POST':
        form = projektFormErstellen(request.POST)
        if form.is_valid():
            @decorateSave
            def projektSave(form_to_save, request, template):
                newProject = form_to_save.save(commit=False)
                newProject.besitzer = TeamhubUser.objects.get(pk=request.user.pk)
                newProject.save()
                return redirect('/projekte/' + str(newProject.pk) + '/')
            return projektSave(form, request, template)

    else:
        form = projektFormErstellen()
    context = makeContext({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def projektBearbeiten(request, projektId):

    '''Abhängig vom übergebenen Requesttyp ändert diese View entweder ein Projektobjekt,
    oder stellt ein Eingabeformular zum Verändern eines Projektobjekts bereit.


    :param projektId: Primärschlüssel des Projektobjekts, welches verändert werden soll.

    :type projektId: int
'''
    from teamhub.forms import projektFormBearbeiten
    from teamhub.decorators import decorateSave

    template = 'base_projekt_bearbeiten.html'
    projekt = Projekt.objects.get(pk=projektId)

    if request.method == 'POST':
        form = projektFormBearbeiten(request.POST, instance=projekt)
        if form.is_valid():
            @decorateSave
            def projektSave(form_to_save, request, template):
                form_to_save.save()
                return redirect('/projekte/' + projektId + '/')
            return projektSave(form, request, template)
    else:
        form = projektFormBearbeiten(instance=projekt)

    context = makeContext({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


def aufgabeDetails(request, aufgabeId):
    '''Erzeugt die Detailansicht eines Aufgabenobjekts.

    :param aufgabeId: Der Primärschlüssel des angezeigten Aufgabenobjekts.

    :type aufgabeId: int
'''
    aufgabe = Aufgabe.objects.get(pk=aufgabeId)

    context = makeContext({'aufgabe': aufgabe, 'aktuellerstatus_lang': dict(AUFGABE_STATUS), 'benutzer': TeamhubUser.objects.get(pk=request.user.pk)})
    return render_to_response('base_aufgabe.html', context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def benutzerErstellen(request):
    '''Abhängig vom Requesttyp erstellt diese View entweder ein neues Userobjekt oder stellt ein Formular
    bereit, mit dem ein neues Userobjekt erstellt werden kann.

    .. note : Nur Benutzer mit dem 'is_staff'-Flag auf 'True' können weitere Benutzerkonten erstellen.

'''
    from teamhub.forms import userForm
    from teamhub.decorators import decorateSave

    template = 'base_benutzer_erstellen.html'
    if request.method == "POST":
        form = userForm(request.POST)
        if form.is_valid():
            @decorateSave
            def benutzerSave(form_to_save, request, template):

                user = form_to_save.save()
                user.set_password("test")
                user.save()
                return dashboard(request)
            return benutzerSave(form, request, template)
    else:
        form = userForm()

    context = makeContext({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


def userProfilBearbeiten(request):
    '''Ermöglicht einem Benutzer, seine Benutzerprofildaten zu verändern.
'''
    from teamhub.forms import profilForm
    from teamhub.decorators import decorateSave

    template = 'base_profil.html'
    user = TeamhubUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = profilForm(request.POST, instance=user)
        if form.is_valid():
            @decorateSave
            def benutzerSave(form_to_save, request, template):
                form.save()
                return redirect('/profil/')
            return benutzerSave(form, request, template)
    else:
        form = profilForm(instance=user)

    context = makeContext({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


def passwortAendern(request):
    '''
    Diese View ermöglicht das Ändern des Passorts
    '''
    from teamhub.forms import passwortAendernForm
    from teamhub.decorators import decorateSave, passwAendern

    template = 'base_passwortAendern.html'

    if request.method == 'POST':
        form = passwortAendernForm(request.POST)
        if form.is_valid():

            @decorateSave
            @passwAendern
            def benutzerSave(form, request, template):
                return redirect('/passwaendern/')
            return benutzerSave(form, request, template)
    else:
        form = passwortAendernForm()

    context = makeContext({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def passwortZuruecksetzen(request):
    '''
    Diese View ermöglicht das Zurücksetzen des Passworts eines Benutzers auf das Standardpasswort des Systems.

    .. note : Das Standardpasswort lautet "test". Es sollte vom betroffenden Benutzer möglichst
    schnell auf ein geeigneteres Passwort geändert werden

    '''
    from teamhub.decorators import decorateSave
    from teamhub.forms import passwortZuruecksetzenForm

    template = 'base_passwortZuruecksetzen.html'

    if request.method == 'POST':
        form = passwortZuruecksetzenForm(request.POST)
        if form.is_valid():
            @decorateSave
            def zuruecksetzen(form, request, template):
                print request.POST['benutzerliste']
                user = TeamhubUser.objects.get(pk=request.POST['benutzerliste'])
                user.set_password("test")
                user.save()
                return redirect('/passwzurueck/')
            return zuruecksetzen(form, request, template)
    else:
        form = passwortZuruecksetzenForm()
    context = makeContext({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


def aufgabeSuchen(request):
    '''
    Implementierung einer einfachen Suche. Es wird in Titel und Beschreibung gesucht.
'''

    from django.db.models import Q

    if 'search' in request.GET and request.GET['search']:
        anfrage = request.GET['search']
        if 'projekt' in request.GET and request.GET['projekt']:
            p_anfrage = Projekt.objects.get(name=request.GET['projekt'])
            aufgabe = Aufgabe.objects.filter(projekt=p_anfrage).filter(Q(titel__icontains=anfrage) | Q(beschreibung__icontains=anfrage))
            context = makeContext({'aufgabe': aufgabe, "anfrage": anfrage})
        else:
            aufgabe = Aufgabe.objects.filter(Q(titel__icontains=anfrage) | Q(beschreibung__icontains=anfrage))
            context = makeContext({'aufgabe': aufgabe, "anfrage": anfrage})

    else:
        anfrage = "Bitte geben Sie ein Suchbegriff ein!!!"
        context = makeContext({"anfrage": anfrage})
    return render_to_response('base_search.html', context, context_instance=RequestContext(request))
