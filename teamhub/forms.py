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

