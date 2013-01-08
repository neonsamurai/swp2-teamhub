# coding: utf-8
"""
.. module:: views
:platform: Unix, Windows
:synopsis: Django views for teamhub package.

.. moduleauthor:: Dennis, Ruslan, Tim, Veronika


"""
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from teamhub.decorators import teamleiterBerechtigung, aufgabeBearbeitenBerechtigung
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from teamhub.models import Aufgabe, Projekt, AUFGABE_STATUS, TeamhubUser
import teamhub.stringConst as c


# Create your views here.


def makeContext(context):
    '''Adds default keys to the context dictionary. These are used site wide.

:param context: The view context dictionary to be appended.
:type context: Dictionary
'''
    context['projektliste'] = Projekt.objects.all().order_by('name')
    context['prioritaet'] = [c.PRIORITAET_HI, c.PRIORITAET_ME, c.PRIORITAET_LO]
    return context


@login_required
def dashboard(request):
    '''The landing page view. It gets all tasks which are assigned to the logged in user.

'''

    meineAufgaben = Aufgabe.objects.filter(bearbeiter=TeamhubUser.objects.get(pk=request.user.pk)).order_by('faelligkeitsDatum')
    meineAufgaben = statusAufgaben(meineAufgaben)
    context = makeContext({'meineAufgaben': meineAufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    context['title'] = 'Meine Aufgaben'
    return render_to_response('base.html', context, context_instance=RequestContext(request))


def offeneAufgabenAnzeigen(request):

    meineAufgaben = Aufgabe.objects.filter(status=c.AUFGABE_STATUS_OP).order_by('faelligkeitsDatum')
    context = makeContext({'meineAufgaben': meineAufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    context['title'] = 'Offene Aufgaben'
    return render_to_response('base.html', context, context_instance=RequestContext(request))


def vonMirErstellteAufgaben(request):

    meineAufgaben = Aufgabe.objects.filter(ersteller=TeamhubUser.objects.get(pk=request.user.pk)).order_by('faelligkeitsDatum')
    context = makeContext({'meineAufgaben': meineAufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    context['title'] = 'Von mir erstellte Aufgaben'
    return render_to_response('base.html', context, context_instance=RequestContext(request))


def statusAufgaben(meineAufgaben):
    for aufgabe in meineAufgaben:
        aufgabe.status = dict(AUFGABE_STATUS)[aufgabe.status]

    return meineAufgaben


def aufgabe(request):

    '''The view creates the input form for creating new tasks.

'''

    return render_to_response('base_aufgabe_erstellen.html', context_instance=RequestContext(request))


def logoutUser(request):
    '''Logs the current user out of the system and redirects to the login screen.
'''
    return logout_then_login(request, '/login/')


def aufgabeErstellen(request):

    '''Depending on the request type this view creates a new Aufgabe objects or provides an input form
to create a new Aufgabe object.
'''

    from teamhub.forms import aufgabeForm
    from teamhub.decorators import decorateSave

    if request.method == 'POST':
        form = aufgabeForm(request.POST)
        if form.is_valid():
            @decorateSave
            def saveAufgabe(form_to_save, request):
                newAufgabe = form_to_save.save(commit=False)
                newAufgabe.ersteller = TeamhubUser.objects.get(pk=request.user.pk)
                newAufgabe.save()
                return redirect('/aufgabe/' + str(newAufgabe.pk) + '/')
            return saveAufgabe(form, request)
    else:
        form = aufgabeForm()
    context = makeContext({'form': form, "title": "Aufgabe Erstellen"})
    return render_to_response('base_aufgabe_bearbeiten.html', context, context_instance=RequestContext(request))


@aufgabeBearbeitenBerechtigung
def aufgabeBearbeiten(request, aufgabeId):
    '''Depending on the request type this view changes a Aufgabe object or provides an input form
to modify data of a Aufgabe object.

:param aufgabeId: The foreign key of the Aufgabe object to be modified.
:type aufgabeId: int
'''
    from teamhub.forms import aufgabeForm
    from teamhub.decorators import decorateSave

    aufgabe = Aufgabe.objects.get(pk=aufgabeId)
    if request.method == 'POST':
        form = aufgabeForm(request.POST, instance=aufgabe)
        if form.is_valid():
            @decorateSave
            def saveAufgabe(form_to_save, request):

                Aufgabe = form_to_save.save(commit=False)
                if 'stati' in request.POST:
                    Aufgabe.status = request.POST['stati']
                Aufgabe.save()
                return redirect('/aufgabe/' + str(aufgabe.pk) + '/')
            return saveAufgabe(form, request)
    else:
        form = aufgabeForm(instance=aufgabe)

    context = makeContext({'form': form, "title": "Aufgabe bearbeiten", 'stati': aufgabe.getStati(), 'aktuellerstatus_lang': dict(AUFGABE_STATUS)[aufgabe.status], 'aktuellerstatus': aufgabe.status})

    return render_to_response('base_aufgabe_bearbeiten.html', context, context_instance=RequestContext(request))


def aufgabeAnnehmen(request, aufgabeId):
    from teamhub.decorators import decorateSave

    aufgabe = Aufgabe.objects.get(pk=aufgabeId)

    @decorateSave
    def saveAufgabe(request, aufgabeId):
        aufgabe.bearbeiter = TeamhubUser.objects.get(pk=request.user.pk)
        aufgabe.save()
        return redirect('/aufgabe/' + str(aufgabe.pk) + '/')
    return saveAufgabe(request, aufgabeId)


def projektListe(request):
    '''Gives a list of all projects in the system.
'''
    projektliste = Projekt.objects.all()
    context = {'projektliste': projektliste}
    return render_to_response('base_projekt.html', context, context_instance=RequestContext(request))


def projektDetail(request, projektId):
    '''Gives the detail view of a project.

:param projektId: The primary key of the project to be displayed.
:type projektId: int
'''
    projekt = Projekt.objects.get(pk=projektId)
    aufgaben = Aufgabe.objects.filter(projekt=projekt).order_by('faelligkeitsDatum')
    context = makeContext({'projekt': projekt, 'aufgaben': aufgaben, 'aktuellerstatus_lang': dict(AUFGABE_STATUS)})
    return render_to_response('base_projekt_detail.html', context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def projektErstellen(request):
    '''Depending on the request type this view creates a new Projekt object or provides an input form
to create a new Projekt object.
'''
    from teamhub.forms import projektFormErstellen
    from teamhub.decorators import decorateSave

    if request.method == 'POST':
        form = projektFormErstellen(request.POST)
        if form.is_valid():
            @decorateSave
            def projektSave(form_to_save, request):
                newProject = form_to_save.save(commit=False)
                newProject.besitzer = TeamhubUser.objects.get(pk=request.user.pk)
                newProject.save()
                return redirect('/projekte/' + str(newProject.pk) + '/')
            return projektSave(form, request)

    else:
        form = projektFormErstellen()
    context = makeContext({'form': form})
    return render_to_response('base_projekt_erstellen.html', context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def projektBearbeiten(request, projektId):

    '''Depending on the request type this view changes a Projekt object or provides an input form
to modify data of a Projekt object.

:param projektId: The primary key of the Projekt object to be modified.
:type projektId: int
'''
    from teamhub.forms import projektFormBearbeiten
    from teamhub.decorators import decorateSave

    projekt = Projekt.objects.get(pk=projektId)

    if request.method == 'POST':
        form = projektFormBearbeiten(request.POST, instance=projekt)
        if form.is_valid():
            @decorateSave
            def projektSave(form_to_save, request):
                form_to_save.save()
                return redirect('/projekte/' + projektId + '/')
            return projektSave(form, request)
    else:
        form = projektFormBearbeiten(instance=projekt)

    context = makeContext({'form': form})
    return render_to_response('base_projekt_bearbeiten.html', context, context_instance=RequestContext(request))


def aufgabeDetails(request, aufgabeId):
    '''Gives the detail view of a given Aufgabe object.

:param aufgabeId: The foreign key of the Aufgabe to be displayed.
:type aufgabeId: int
'''
    aufgabe = Aufgabe.objects.get(pk=aufgabeId)
    aufgabe.status = dict(AUFGABE_STATUS)[aufgabe.status]
    context = makeContext({'aufgabe': aufgabe, 'benutzer': TeamhubUser.objects.get(pk=request.user.pk)})
    return render_to_response('base_aufgabe.html', context, context_instance=RequestContext(request))


@teamleiterBerechtigung
def benutzerErstellen(request):
    '''Depending on the request type this view either creates a new user in the system,
or displays an input form to create a new user.

.. note : Only users with the is_staff flag set to True can create new users.
'''
    from teamhub.forms import userForm
    from teamhub.decorators import decorateSave

    if request.method == "POST":
        form = userForm(request.POST)
        if form.is_valid():
            @decorateSave
            def benutzerSave(form_to_save, request):

                user = form_to_save.save()
                user.set_password("test")
                user.save()
                return dashboard(request)
            return benutzerSave(form, request)
    else:
        form = userForm()

    context = makeContext({'form': form})
    return render_to_response('base_benutzer_erstellen.html', context, context_instance=RequestContext(request))


def userProfilBearbeiten(request):
    '''Allows a user to modify her profile data.
'''
    from teamhub.forms import profilForm
    from teamhub.decorators import decorateSave

    user = TeamhubUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = profilForm(request.POST, instance=user)
        if form.is_valid():
            @decorateSave
            def benutzerSave(form_to_save, request):
                form.save()
                return redirect('/profil/')
            return benutzerSave(form, request)
    else:
        form = profilForm(instance=user)

    context = makeContext({'form': form})
    return render_to_response('base_profil.html', context, context_instance=RequestContext(request))


def passwortAendern(request):
    from teamhub.forms import passwortAendernForm
    from teamhub.decorators import decorateSave, passwAendern

    if request.method == 'POST':
        form = passwortAendernForm(request.POST)
        if form.is_valid():

            @decorateSave
            @passwAendern
            def benutzerSave(form, request):
                return redirect('/passwaendern/')
            return benutzerSave(form, request)
    else:
        form = passwortAendernForm()

    context = makeContext({'form': form})
    return render_to_response('base_passwortAendern.html', context, context_instance=RequestContext(request))


def search(request):
    '''Implementierung einer einfachen suche. Es wird in Titel und Beschreibung gesucht.'''
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
