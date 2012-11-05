from django.forms import ModelForm
from django.contrib.auth.models import User
from teamhub.models import Projekt, Aufgabe

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
 
class aufgabeForm(ModelForm):
    class Meta:
        model = Aufgabe
        #auto_id=True
        '''
        def __unicode__(self):
            return self.as_divs()
          '''     