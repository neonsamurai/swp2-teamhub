# coding: utf-8

"""
.. module:: forms
:platform: Unix, Windows
:synopsis: Custom Django forms for teamhub package.

.. moduleauthor:: Dennis, Ruslan, Tim, Veronika


"""

from django.contrib.auth.models import User
from django.forms import ModelForm, RegexField

from teamhub.models import Projekt, Aufgabe
from django.utils import timezone
from django import forms

'''
Django forms go here
'''
class profilForm(ModelForm):
    username = RegexField(label="Benutzername", max_length=30,
                                    regex=r'^[\w.@+-]+$',
                                    help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                    error_messages={
                                        'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    class Meta:
        model = User
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
    username = RegexField(label="Benutzername", max_length=30,
                                    regex=r'^[\w.@+-]+$',
                                    help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                    error_messages={
                                        'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    class Meta:
        model = User
        fields = ('username', 'email','is_staff')
        
class passwortAendernForm(forms.Form):
    passwAlt = forms.CharField(label= "Altes Passwort", max_length=128, min_length=4)
    passwNeu1 = forms.CharField(label= "Neues Passwort", max_length=128, min_length=4)
    passwNeu2 = forms.CharField(label= "Neues Passwort widerholen", max_length=128, min_length=4)

