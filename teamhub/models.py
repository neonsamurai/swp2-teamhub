# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError
import teamhub.stringConst as c

# Enums used by model classes
PRIORITAET = (
    (c.PRIORITAET_HI, "Hoch"),
    (c.PRIORITAET_ME, "Mittel"),
    (c.PRIORITAET_LO, "Niedrig"),
)

AUFGABE_STATUS = (
    (c.AUFGABE_STATUS_OP, "Offen"),
    (c.AUFGABE_STATUS_IP, "In Bearbeitung"),
    (c.AUFGABE_STATUS_PA, "Angehalten"),
    (c.AUFGABE_STATUS_CL, "Geschlossen"),
)

PROJEKT_STATUS = (
    (c.PROJEKT_STATUS_OP, "Offen"),
    (c.PROJEKT_STATUS_CL, "Geschlossen"),
)

# App model classes


class Projekt(models.Model):
    '''
    Repräsentation eines Projekts. Das Projekt dient als Container für Aufgaben.

    '''

    besitzer = models.ForeignKey(User, related_name="besitzer", help_text="Verantwortlicher für das Projekt.",blank=True, null=True)

    name = models.CharField(max_length=512, help_text="Name des Projekts.", unique=True)
    beschreibung = models.TextField(help_text="Ausführliche Beschreibung des Projekts.")
    status = models.CharField(max_length=2, default=c.PROJEKT_STATUS_OP, choices=PROJEKT_STATUS, help_text="Zustand des Projekts.")
    
    def __unicode__(self):
        return self.name


class Aufgabe(models.Model):

    '''
    Repräsentation einer Aufgabe.
    '''
    ersteller = models.ForeignKey(User, related_name="ersteller", help_text="Ersteller dieser Aufgabe.",blank=True, null=True)
    bearbeiter = models.ForeignKey(User, related_name="bearbeiter", blank=True, null=True, help_text="Bearbeiter dieser Aufgabe.")
    projekt = models.ForeignKey(Projekt, related_name="projekt", help_text="Das der Aufgabe übergeordnete Projekt.")

    status = models.CharField(max_length=2, default=c.AUFGABE_STATUS_OP, choices=AUFGABE_STATUS, help_text="Bearbeitungsstatus der Aufgabe.")
    prioritaet = models.CharField(max_length=2, default=c.PRIORITAET_ME, choices=PRIORITAET, help_text="Priorität der Aufgabe im Hinblick auf das Projekt.")
    titel = models.CharField(max_length=512, help_text="Der Titel soll eine Idee des Inhalts der Aufgabe geben.")
    beschreibung = models.TextField(blank=True, help_text="Detaillierter Beschreibung der Aufgabe. Was ist das Problem? Unter welchen Bedingungen gilt die Aufgabe als gelöst?")
    erstellDatum = models.DateTimeField(auto_now_add=True, help_text="Die Aufgabe wurde an diesem Tag erstellt.")
    aenderungsDatum = models.DateTimeField(editable=False, auto_now=True, auto_now_add=True, help_text="Zeit der letzten Änderung.")
    faelligkeitsDatum = models.DateTimeField(blank=True, help_text="Die Aufgabe muss bis zu diesem Datum erledigt sein.")
  
    def save(self):
        if Aufgabe.objects.filter(titel=self.titel,projekt=self.projekt).exclude(pk=self.pk).count()!=0:
            raise IntegrityError (c.FEHLER_AUFGABE_NAME)
        if self.faelligkeitsDatum < timezone.now():
            raise IntegrityError (c.FEHLER_AUFGABE_DATUM)
        if self.projekt.status==c.PROJEKT_STATUS_CL:
            raise IntegrityError(c.FEHLER_AUFGABE_PROJEKTSTATUS)
        super(Aufgabe, self).save()


    def __unicode__(self):
        return self.titel

