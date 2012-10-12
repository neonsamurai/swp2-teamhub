from django.forms import ModelForm
from django.contrib.auth.models import User
from teamhub.models import Projekt

'''
Django forms go here
'''

class profilForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
class projektForm(ModelForm):
    class Meta:
        model = Projekt
        