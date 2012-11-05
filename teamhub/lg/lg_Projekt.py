# coding: utf-8
from teamhub.models import Projekt

class lgProjekt:
    def lg_projekt_isValid(self, projekt):
        if Projekt.objects.filter(name=projekt.name).exclude(pk=projekt.pk).count()!=0:
            return False
        projekt.save()
        return True