# coding: utf-8

"""
.. module:: forms

:platform: Unix, Windows

:synopsis: Custom Django forms für teamhub Paket.

.. moduleauthor:: Tim Jagodzinski


"""
from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput

from teamhub.models import Projekt, Aufgabe, TeamhubUser


class profilForm(ModelForm):
    '''
    Eingabeformular zum Ändern des Benutzerprofils.
    '''
    class Meta:
        model = TeamhubUser
        fields = ('username', 'first_name', 'last_name', 'email')


class projektFormBearbeiten(ModelForm):
    '''
    Eingabeformular zum Bearbeiten eines Projekt-Objekts.
    '''
    class Meta:
        model = Projekt
        exclude = ('besitzer')


class projektFormErstellen(ModelForm):
    '''
    Eingabeformular zum Erstellen eines Projekt-Objekts.
    '''
    class Meta:
        model = Projekt
        exclude = ('status', 'besitzer')


class aufgabeForm(ModelForm):
    '''
    Eingabeformular zum Erstellen/Bearbeiten eines Aufgabe-Objekts.
    '''
    class Meta:
        model = Aufgabe
        exclude = ('ersteller', 'status',)


class userForm(ModelForm):
    '''
    Eingabeformular zum Erstellen/Ändern eines TeamhubUser-Objekts.
    '''
    class Meta:
        model = TeamhubUser
        fields = ('username', 'email', 'is_staff')


class passwortAendernForm(forms.Form):
    '''
    Eingabeformular zum Ändern des Passworts.
    '''
    passwAlt = forms.CharField(widget=PasswordInput, label="Altes Passwort", max_length=128, min_length=4)
    passwNeu1 = forms.CharField(widget=PasswordInput, label="Neues Passwort", max_length=128, min_length=4)
    passwNeu2 = forms.CharField(widget=PasswordInput, label="Neues Passwort widerholen", max_length=128, min_length=4)


class passwortZuruecksetzenForm(forms.Form):
    benutzerliste = forms.ModelChoiceField(queryset=TeamhubUser.objects.all())
