# coding: utf-8

from teamhub.models import Aufgabe, Projekt
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
import teamhub.stringConst as c



from teamhub.models import TeamhubUser


def makeContext(context):
    context['projektliste'] = Projekt.objects.all().order_by('name')
    context['prioritaet'] = [c.PRIORITAET_HI, c.PRIORITAET_ME, c.PRIORITAET_LO]
    return context


def decorateSave(func):
    def wrapper(form, request):
        try:
            return func(form, request)
        except IntegrityError, e:

            msg = str(e)
            context = {}
            context.update(csrf(request))

            if msg == c.FEHLER_AUFGABE_NAME:
                form._errors["titel"] = form.error_class([msg])
                del form.cleaned_data["titel"]
                context['form'] = form
            if msg == c.FEHLER_AUFGABE_DATUM:
                form._errors["faelligkeitsDatum"] = form.error_class([msg])
                del form.cleaned_data["faelligkeitsDatum"]
                context['form'] = form
            if msg == c.FEHLER_AUFGABE_PROJEKTSTATUS or msg == c.FEHLER_AUFGABE_STATUS:
                form._errors['__all__'] = form.error_class([msg])
                context['form'] = form
            if msg == c.FEHLER_TEAMHUBUSER_USERNAME_INVALID:
                form._errors["username"] = form.error_class([msg])
                del form.cleaned_data["username"]
                context['form'] = form
                context = makeContext(context)
                return render_to_response('base_profil.html', context, context_instance=RequestContext(request))
            context = makeContext(context)
            return render_to_response('base_aufgabe_bearbeiten.html', context, context_instance=RequestContext(request))

        except Exception, e:
            msg = str(e)
            context = {}
            context.update(csrf(request))
            form._errors['__all__'] = form.error_class([msg])
            context['form'] = form
            context = makeContext(context)
            return render_to_response('base_aufgabe_bearbeiten.html', context, context_instance=RequestContext(request))

    return wrapper


def teamleiterBerechtigung(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        return redirect("/")
    return wrapper


def aufgabeBearbeitenBerechtigung(func):
    def wrapper(request, *args, **kwargs):
        aufgabe = Aufgabe.objects.get(pk=kwargs['aufgabeId'])
        if TeamhubUser.objects.get(pk=request.user.pk) == aufgabe.bearbeiter or TeamhubUser.objects.get(pk=request.user.pk) == aufgabe.ersteller:
            return func(request, aufgabe.pk)
        return redirect("/")
    return wrapper


def passwAendern(func):
    def wrapper(form, request):
        user = User.objects.get(pk=request.user.pk)
        passwAlt = form.cleaned_data['passwAlt']
        passwNeu1 = form.cleaned_data['passwNeu1']
        passwNeu2 = form.cleaned_data['passwNeu2']
        if not user.check_password(passwAlt):
            raise Exception(c.FEHLER_PASSWD_ALT)
        if not passwNeu1 == passwNeu2:
            raise Exception(c.FEHLER_PASSWD_NEU)
        user.set_password(passwNeu2)
        user.save()

        context = {}
        context.update(csrf(request))
        context['form'] = form
        context['erfolg'] = c.PASSWD_GEAENDERT
        context = makeContext(context)
        return render_to_response('base_passwortAendern.html', context, context_instance=RequestContext(request))

    return wrapper

