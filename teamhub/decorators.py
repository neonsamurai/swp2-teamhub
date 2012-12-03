# coding: utf-8
from django.db.utils import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from teamhub.views import makeContext
import teamhub.stringConst as c


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
            if msg==c.FEHLER_AUFGABE_PROJEKTSTATUS:
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