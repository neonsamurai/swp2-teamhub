from django.forms import ModelForm, CharField
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
        
class projektFormErstellen(ModelForm):
    class Meta:
        model = Projekt
        exclude=('status',)
        

class aufgabeForm(ModelForm):
    class Meta:
        model = Aufgabe
        #auto_id=True
        '''
        def __unicode__(self):
            return self.as_divs()
          '''     
        
class userForm(ModelForm):
    class Meta:
        model=User
        fields=('username','is_staff')