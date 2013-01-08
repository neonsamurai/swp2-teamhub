# coding: utf-8
"""
.. module:: forms
:platform: Unix, Windows
:synopsis: Custom Django forms for teamhub package.

.. moduleauthor:: Dennis, Ruslan, Tim, Veronika


"""
from django.forms import ModelForm
from teamhub.models import Projekt, Aufgabe, TeamhubUser


'''
Django forms go here
'''


class profilForm(ModelForm):
    class Meta:
        model = TeamhubUser
        fields = ('username', 'first_name', 'last_name', 'email')


class projektFormBearbeiten(ModelForm):
    class Meta:
        model = Projekt
        exclude = ('besitzer')


class projektFormErstellen(ModelForm):
    class Meta:
        model = Projekt
        exclude = ('status', 'besitzer')


class aufgabeForm(ModelForm):
    class Meta:
        model = Aufgabe
        exclude = ('ersteller', 'status',)


class userForm(ModelForm):
    class Meta:
        model = TeamhubUser
        fields = ('username', 'email', 'is_staff')
