# coding: utf-8
"""
.. module:: admin

:platform: Unix, Windows

:synopsis: Anpassungen für das Admin-Modul. Es fügt automatisches Füllen der Fremdschlüssel 'ersteller' und 'besitzer' zu den Model-Klassen 'Aufgabe' und 'Projekt' hinzu.

.. moduleauthor:: Tim Jagodzinski

"""

from django.contrib import admin
from teamhub.models import Aufgabe, Projekt


class AufgabeAdmin(admin.ModelAdmin):
    list_display = ('titel', 'ersteller', 'erstellDatum')

    def save_model(self, request, obj, form, change):
        '''Automatisches Füllen des Fremdschlüssels 'ersteller' beim Speichern in der Adminseite.

        :param obj: Das Aufgabe-Objekt, welches mit dem Fremdschlüssels des angemeldeten Users befüllt werden soll.
        :type obj: Aufgabe
        :param form: Das Django form von dem der POST request ausgeht.
        :type form: Form oder ModelForm

        '''
        obj.ersteller = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        '''Speichert das formset mit dem veränderten Aufgabe-Objekt.

        '''
        if formset.model == Aufgabe:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.ersteller = request.user
                instance.save()
        else:
            formset.save()

admin.site.register(Aufgabe, AufgabeAdmin)

class ProjektAdmin(admin.ModelAdmin):
    list_display = ('name', 'besitzer')

# Auto populate ForeignKey field besitzer on save in admin site
    def save_model(self, request, obj, form, change):
        '''Automatisches Füllen des Fremdschlüssels 'besitzer' beim Speichern in der Adminseite.

        :param obj: Das Projekt-Objekt, welches mit dem Fremdschlüssels des angemeldeten Users befüllt werden soll.
        :type obj: Aufgabe
        '''
        obj.besitzer = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        '''Speichert das formset mit dem veränderten Projekt-Objekt.

        '''
        if formset.model == Projekt:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.besitzer = request.user
                instance.save()
        else:
            formset.save()

admin.site.register(Projekt, ProjektAdmin)