# coding: utf-8
from django.forms import ModelForm, CharField
from django.contrib.auth.models import User
from teamhub.models import Projekt, Aufgabe
from django.utils import timezone



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
        fields=('username','is_staff')