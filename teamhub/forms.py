# coding: utf-8
"""
.. module:: forms
:platform: Unix, Windows
:synopsis: Custom Django forms for teamhub package.

.. moduleauthor:: Dennis, Ruslan, Tim, Veronika


"""
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from teamhub.models import Projekt, Aufgabe


'''
Django forms go here
'''


class profilForm(ModelForm):
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
    class Meta:
        model = User
        fields = ('username', 'is_staff')