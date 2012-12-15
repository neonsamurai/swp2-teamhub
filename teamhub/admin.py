# coding: utf-8
"""
.. module:: admin
   :platform: Unix, Windows
   :synopsis: Customization for admin module. It adds auto population of the ForeignKey field 'ersteller' and 'besitzer' to models Aufgabe and Projekt

.. moduleauthor:: Tim


"""

from django.contrib import admin
from teamhub.models import Aufgabe, Projekt


class AufgabeAdmin(admin.ModelAdmin):
    list_display = ('titel', 'ersteller', 'erstellDatum')

    def save_model(self, request, obj, form, change):
        '''Auto populate ForeignKey field 'ersteller' on save in admin site

        :param request: The request object from which the logged in user is determined.
        :type request: HttpRequest
        :param obj: The Aufgabe object to be populated with the ForeignKey of the logged in user.
        :type obj: Aufgabe
        :param form: The Django form from which the POST request originates.
        :type form: Form or ModelForm
        :param change: ?
        :type change: ?
        '''
        obj.ersteller = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        '''Saves the formset with the modified Projekt object.

        :param request: The request object from which the logged in user is determined.
        :type request: HttpRequest
        :param form: The Django form from which the POST request originates.
        :type form: Form or ModelForm
        :param formset: The formset to be saved.
        :type formset: Formset
        :param change: ?
        :type change: ?
        '''
        if formset.model == Aufgabe:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.ersteller = request.user
                instance.save()
        else:
            formset.save()

admin.site.register(Aufgabe, AufgabeAdmin)
'''Saves the formset with the modified Projekt object.

        :param request: The request object from which the logged in user is determined.
        :type request: HttpRequest
        :param form: The Django form from which the POST request originates.
        :type form: Form or ModelForm
        :param formset: The formset to be saved.
        :type formset: Formset
        :param change: ?
        :type change: ?
        '''

class ProjektAdmin(admin.ModelAdmin):
    list_display = ('name', 'besitzer')

# Auto populate ForeignKey field besitzer on save in admin site
    def save_model(self, request, obj, form, change):
        '''Auto populate ForeignKey field 'besitzer' on save in admin site

        :param request: The request object from which the logged in user is determined.
        :type request: HttpRequest
        :param obj: The Aufgabe object to be populated with the ForeignKey of the logged in user.
        :type obj: Aufgabe
        :param form: The Django form from which the POST request originates.
        :type form: Form or ModelForm
        :param change: ?
        :type change: ?
        '''
        obj.besitzer = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        '''Saves the formset with the modified Projekt object.

        :param request: The request object from which the logged in user is determined.
        :type request: HttpRequest
        :param form: The Django form from which the POST request originates.
        :type form: Form or ModelForm
        :param formset: The formset to be saved.
        :type formset: Formset
        :param change: ?
        :type change: ?
        '''
        if formset.model == Projekt:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.besitzer = request.user
                instance.save()
        else:
            formset.save()

admin.site.register(Projekt, ProjektAdmin)