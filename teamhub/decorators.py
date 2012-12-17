# coding: utf-8
<<<<<<< HEAD
from teamhub.models import Aufgabe, Projekt
from django.db.utils import IntegrityError
=======
from teamhub.models import Aufgabe
>>>>>>> master
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.context_processors import csrf
import teamhub.stringConst as c

def makeContext(context):
    context['projektliste'] = Projekt.objects.all().order_by('name')
    context['prioritaet']=[c.PRIORITAET_HI,c.PRIORITAET_ME,c.PRIORITAET_LO]
    return context


def decorateSave(func):
    def wrapper(form, request):
        try:
            return func(form, request)
        except IntegrityError, e:
            msg= str(e)
            context={}
            context.update(csrf(request))
            
            if msg==c.FEHLER_AUFGABE_NAME:
                form._errors["titel"] = form.error_class([msg])
                del form.cleaned_data["titel"]
                context['form']=form                
            if msg==c.FEHLER_AUFGABE_DATUM:
                
                form._errors["faelligkeitsDatum"] = form.error_class([msg])
                del form.cleaned_data["faelligkeitsDatum"]
                context['form']=form
            if msg==c.FEHLER_AUFGABE_PROJEKTSTATUS or msg==c.FEHLER_AUFGABE_STATUS:
                form._errors['__all__'] = form.error_class([msg])
                context['form']=form
            context = makeContext(context)    
            return render_to_response('base_aufgabe_bearbeiten.html',context)
            
        except Exception, e:
            msg= str(e)
            context={}
            context.update(csrf(request))
            form._errors['__all__'] = form.error_class([msg])
            context['form']=form
            context = makeContext(context)    
            return render_to_response('base_aufgabe_bearbeiten.html',context)
            
    return wrapper

def teamleiterBerechtigung(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request)
        return redirect("/")
    return wrapper

def aufgabeBearbeitenBerechtigung(func):
    def wrapper(request, *args, **kwargs):
        aufgabe=Aufgabe.objects.get(pk=kwargs['aufgabeId'])
        if request.user==aufgabe.bearbeiter or request.user==aufgabe.ersteller:
            return func(request, aufgabe.pk)
        return redirect("/")
    return wrapper
    
            