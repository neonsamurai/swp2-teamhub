# coding: utf-8
from teamhub.forms import projektForm
from teamhub.models import Projekt
from django.contrib.auth.models import User

class lgProjekt:
    def lg_projektErstellen(self, request):
        form = projektForm(request)
        
        if not form.is_valid():
           return False, str("erstellen")
       
        if Projekt.objects.filter(name=request.get("name")).count() != 0:
            return False, str("erstellen")
        
        newProjekt = form.save()
        return True, str(newProjekt.pk)
    
    def lg_projektBearbeiten(self, request, projekt):
        form = projektForm(request, instance=projekt)
        
        if not form.is_valid():
            return str(projekt.pk)
       
        if (Projekt.objects.get(pk=projekt.pk).name != projekt.name) and Projekt.objects.filter(name=request.get("name")).count() != 0:
            return str(projekt.pk)
        
        newProjekt = form.save()
        return str(newProjekt.pk)

    
