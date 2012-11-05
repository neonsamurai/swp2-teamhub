# coding: utf-8
from teamhub.models import Aufgabe
from teamhub.models import Projekt
from django.utils import timezone

class lgAufgabe:
    def lg_aufgabe_isValid(self, aufgabe):
        if Aufgabe.objects.filter(titel=aufgabe.titel,projekt=aufgabe.projekt).exclude(pk=aufgabe.pk).count()!=0:
            return False
        if aufgabe.faelligkeitsDatum < timezone.now():
            return False
        if aufgabe.projekt.status=="CL":
            return False
        '''
        if (not aufgabe.prioritaet=="ME") and (aufgabe.status=="CL" or aufgabe.status=="PA"):
            return False
        '''
        aufgabe.save()
        return True