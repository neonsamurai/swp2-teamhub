# coding: utf-8

"""
.. module:: forms
:platform: Unix, Windows
:synopsis: Custom Django forms for teamhub package.

.. moduleauthor:: Dennis, Ruslan, Tim, Veronika


"""
from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput

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


class passwortAendernForm(forms.Form):
    passwAlt = forms.CharField(widget=PasswordInput, label="Altes Passwort", max_length=128, min_length=4)
    passwNeu1 = forms.CharField(widget=PasswordInput, label="Neues Passwort", max_length=128, min_length=4)
    passwNeu2 = forms.CharField(widget=PasswordInput, label="Neues Passwort widerholen", max_length=128, min_length=4)

