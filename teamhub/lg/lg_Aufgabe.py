# coding: utf-8
from teamhub.models import Aufgabe
from django.utils import timezone

class lgAufgabe:
    def lg_aufgabe_isValid(self, aufgabe):
        if Aufgabe.objects.filter(name=aufgabe.name).count()!=0:
            return False
        if not aufgabe.faelligkeitsDatum>=timezone.now():
            return False