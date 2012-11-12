# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError

# Enums used by model classes
PRIORITAET = (
                ("HI", "Hoch"),
                ("ME", "Mittel"),
                ("LO", "Niedrig"),
              )

AUFGABE_STATUS = (
                    ("OP", "Offen"),
                    ("IP", "In Bearbeitung"),
                    ("PA", "Angehalten"),
                    ("CL", "Geschlossen"),
                  )

PROJEKT_STATUS = (
                    ("OP", "Offen"),
                    ("CL", "Geschlossen"),
                  )

# App model classes
class Projekt(models.Model):
    '''
    Repräsentation eines Projekts. Das Projekt dient als Container für Aufgaben.
    '''
    besitzer = models.ForeignKey(User, related_name="besitzer", help_text="Verantwortlicher für das Projekt.")
    
    name = models.CharField(max_length=512, help_text="Name des Projekts.")
    beschreibung = models.TextField(help_text="Ausführliche Beschreibung des Projekts.")
    status = models.CharField(max_length=2, default="OP", choices=PROJEKT_STATUS, help_text="Zustand des Projekts.")
    
    def save (self):
        if Projekt.objects.filter(name=self.name).exclude(pk=self.pk).count()!=0:
            raise IntegrityError ('Es existiert schon ein Projekt mit dem Namen: '+self.name+'!')
        
        super(Projekt, self).save()
        
        
    def __unicode__(self):
        return self.name
    
class Aufgabe(models.Model):
    
    '''
    Repräsentation einer Aufgabe.
    '''
    ersteller = models.ForeignKey(User, related_name="ersteller", help_text="Ersteller dieser Aufgabe.")
    bearbeiter = models.ForeignKey(User, related_name="bearbeiter", blank=True, null=True, help_text="Bearbeiter dieser Aufgabe.")
    projekt = models.ForeignKey(Projekt, related_name="projekt", help_text="Das der Aufgabe übergeordnete Projekt.")
    
    status = models.CharField(max_length=2, default="OP", choices=AUFGABE_STATUS, help_text="Bearbeitungsstatus der Aufgabe.")
    prioritaet = models.CharField(max_length=2, default="ME", choices=PRIORITAET, help_text="Priorität der Aufgabe im Hinblick auf das Projekt.")
    titel = models.CharField(max_length=512, help_text="Der Titel soll eine Idee des Inhalts der Aufgabe geben.")
    beschreibung = models.TextField(blank=True, help_text="Detaillierter Beschreibung der Aufgabe. Was ist das Problem? Unter welchen Bedingungen gilt die Aufgabe als gelöst?")
    erstellDatum = models.DateTimeField(auto_now_add=True, help_text="Die Aufgabe wurde an diesem Tag erstellt.")
    aenderungsDatum = models.DateTimeField(editable=False, auto_now=True, auto_now_add=True, help_text="Zeit der letzten Änderung.")
    faelligkeitsDatum = models.DateTimeField(blank=True, help_text="Die Aufgabe muss bis zu diesem Datum erledigt sein.")
    
    def save(self):
        if Aufgabe.objects.filter(titel=self.titel,projekt=self.projekt).exclude(pk=self.pk).count()!=0:
            raise IntegrityError ('Es existiert schon eine Aufgabe mit dem Namen: '+self.titel+'!')
        if self.faelligkeitsDatum < timezone.now():
            raise IntegrityError ('Fälligkeitsdatum liegt in Vergangenheit!')
        if self.projekt.status=="CL":
            return False
        super(Aufgabe, self).save()
        return True
    
    def __unicode__(self):
        return self.titel
    
class CustomUser(User):
    
   def user_have_permissions(self, user):
       return user.is_staff
   
   def user_erstellen(self, user):
       if User.objects.filter(username=user.username).count()!=0:
           return False
       user.save()
       user.set_password("test")
       user.save()
       return True 
    
