# coding: utf-8
from django.forms import ModelForm, CharField
from django.contrib.auth.models import User
from teamhub.models import Projekt, Aufgabe
from django.utils import timezone
from django.core.exceptions import ValidationError


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
        
    def clean(self):
        
        cleaned_data= super(aufgabeForm, self).clean()
        aufgabentitel=cleaned_data.get("titel")   
        projekt=cleaned_data.get("projekt")
        f_datum=cleaned_data.get("faelligkeitsDatum")
        
        
        if aufgabentitel and projekt:
            if Aufgabe.objects.filter(titel=aufgabentitel, projekt=projekt).exclude(pk=self.instance.pk).count() != 0:
                msg = "Es existiert schon eine Aufgabe mit dem Namen!"
                self._errors["titel"] = self.error_class([msg])
                del cleaned_data["titel"]
                
        if f_datum:
            if f_datum < timezone.now():
                msg= "Fälligkeitsdatum darf nicht in der Vergangenheit liegen!"
                self._errors["faelligkeitsDatum"] = self.error_class([msg])
                del cleaned_data["faelligkeitsDatum"]
         
        if projekt:
            if projekt.status=="CL":
                 raise ValidationError("Das Projektstatus darf nicht geschlossen sein!")
               
        return cleaned_data
        

'''
class aufgabeErstellenForm(aufgabeForm):
    class Meta:
        model = Aufgabe
        exclude = ('ersteller', 'status',)
       '''

                
class userForm(ModelForm):
    class Meta:
        model = User
        fields=('username','is_staff')