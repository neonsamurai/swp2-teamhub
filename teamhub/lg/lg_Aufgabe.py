# coding: utf-8
from teamhub.models import Aufgabe
from django.utils import timezone

class lgAufgabe:
    def lg_aufgabe_isValid(self, aufgabe):
        if Aufgabe.objects.filter(titel=aufgabe.titel).count()!=0:
            return False
        if aufgabe.faelligkeitsDatum < timezone.now():
            return False
        aufgabe.save()
        return True