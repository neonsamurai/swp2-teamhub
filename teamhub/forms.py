from django.forms import ModelForm
from django.contrib.auth.models import User

'''
Django forms go here
'''

class profilForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')