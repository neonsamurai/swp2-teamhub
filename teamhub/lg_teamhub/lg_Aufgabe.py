from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from teamhub.models import Aufgabe, Projekt
from teamhub.forms import aufgabeForm

class LgAufgabe:
    def lg_aufgabeErstellen(self, request):
        form = aufgabeForm(request)
        
        if not form.is_valid():
            print "form invalid"
            return False, str("erstellen")
       
        if Projekt.objects.filter(name=request.get("name")).count() != 0:
            print "duplicate name"
            return False, str("erstellen")
        
        newAufgabe = form.save()
        return True, str(newAufgabe.pk)
