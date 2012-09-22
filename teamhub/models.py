# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

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

# Create your models here.
class Aufgabe(models.Model):
    '''
    Repräsentation einer Aufgabe.
    '''
    ersteller = models.ForeignKey(User, related_name="ersteller", editable=False, help_text="Ersteller dieser Aufgabe.")
    bearbeiter = models.ForeignKey(User, related_name="bearbeiter", blank=True, null=True, help_text="Bearbeiter dieser Aufgabe.")
    
    status = models.CharField(max_length=2, default="OP",choices=AUFGABE_STATUS, help_text="Bearbeitungsstatus der Aufgabe.")
    prioritaet = models.CharField(max_length=2, default="ME", choices=PRIORITAET, help_text="Priorität der Aufgabe im Hinblick auf das Projekt.")
    titel = models.CharField(max_length=512, help_text="Der Titel soll eine Idee des Inhalts der Aufgabe geben.")
    beschreibung = models.TextField(blank=True, help_text="Detaillierter Beschreibung der Aufgabe. Was ist das Problem? Unter welchen Bedingungen gilt die Aufgabe als gelöst?")
    erstellDatum = models.DateTimeField(auto_now_add=True, help_text="Die Aufgabe wurde an diesem Tag erstellt.")
    aenderungsDatum = models.DateTimeField(editable=False,auto_now=True, auto_now_add=True, help_text="Zeit der letzten Änderung.")
    faelligkeitsDatum = models.DateTimeField(blank=True, help_text="Die Aufgabe muss bis zu diesem Datum erledigt sein.")
