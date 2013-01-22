# coding: utf-8
"""
.. module:: models

:platform: Unix, Windows

:synopsis: Custom Django models für teamhub Paket.

.. moduleauthor:: Tim Jagodzinski


"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError
import teamhub.stringConst as c
import re

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


class TeamhubUser(User):
    '''
    Repräsentation eines Benutzers. Die Proxyklasse wird für erweiternde Funktionen verwendet,
    die über die von Django bereitgestellten hinausgehen.
    '''
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        '''Überprüft den Benutzernamen auf nicht erlaubte Zeichen. Nur Benutzernamen, welche dem
        regulären Ausdruck r'^[\w.@+-]+$' folgen sind erlaubt.

        :throws IntegrityError: Falls das Feld unsername nicht erlaubte Zeichen enthält.

        '''
        pattern = re.compile(r'^[\w.@+-]+$')

        if not re.match(pattern, self.username):
            raise IntegrityError(c.FEHLER_TEAMHUBUSER_USERNAME_INVALID)
        super(TeamhubUser, self).save(*args, **kwargs)


class Projekt(models.Model):
    '''
    Repräsentation eines Projekts. Projekte werden zur Organisation von Aufgaben benutzt.
        .. py:attribute:: besitzer

        Fremdschlüssel, der auf ein TeamhubUser-Objekt verweist. Kann nicht mehr geändert werden.

        .. py:attribute:: name

        String, Name bzw. Titel des Projekts. Ist veränderbar.

        .. py:attribute:: beschreibung

        String, Ausführliche Beschreibung des Projekts. Ist veränderbar.

        .. py:attribute:: status

        String, Bearbeitungsstatus des Projekts. Kann nur die Werte "Offen" oder "Geschlossen" sein.

'''

    besitzer = models.ForeignKey(TeamhubUser, related_name="besitzer", help_text="Verantwortlicher für das Projekt.", blank=True, null=True)

    name = models.CharField(max_length=512, help_text="Name des Projekts.", unique=True)
    beschreibung = models.TextField(help_text="Ausführliche Beschreibung des Projekts.")
    status = models.CharField(max_length=2, default=c.PROJEKT_STATUS_OP, choices=PROJEKT_STATUS, help_text="Zustand des Projekts.")

    def __unicode__(self):
        return self.name


class Aufgabe(models.Model):

    '''Repräsentation einer Aufgabe.

        .. py:attribute:: ersteller

        Fremdschlüssel, verweist auf ein TeamhubUser-Objekt, ist unveränderbar.

        .. py:attribute:: bearbeiter

        Fremdschlüssel, verweist auf ein TeamhubUser-Objekt, ist veränderlich.

        .. py:attribute:: projekt

        Fremdschlüssel, verweist auf ein Projekt-Objekt, ist veränderlich.

        .. py:attribute:: status

        String, Bearbeitungsstatus der Aufgabe, kann je nach Zustand folgende Werte annehmen: "Offen", "In Bearbeitung", "Angehalten", "Geschlossen". Veränderlich.

        .. py:attribute:: prioritaet

        String, Bearbeitungspriorität der Aufgabe, kann die Werte "Niedrig", "Mittel", "Hoch" annehmen. Veränderlich.

        .. py:attribute:: titel

        String, Titel bzw. Kurzbeschreibung der Aufgabe, ist veränderlich.

        .. py:attribute:: beschreibung

        String, ausführliche Beschreibung der Aufgabe, ist veränderlich.

        .. py:attribute:: erstellDatum

        Datum, Zeitpunkt der Erstellung der Aufgabe, ist unveränderlich.

        .. py:attribute:: aenderungsDatum

        Datum, Zeitpunkt der letzten Änderung an der Aufgabe, wird automatisch vom System gesetzt.

        .. py:attribute:: faelligkeitsDatum

        Datum, Zeitpunkt zu dem die Aufgabe erfüllt sein soll, ist veränderlich.

'''
    ersteller = models.ForeignKey(TeamhubUser, related_name="ersteller", help_text="Ersteller dieser Aufgabe.", blank=True, null=True)
    bearbeiter = models.ForeignKey(TeamhubUser, related_name="bearbeiter", blank=True, null=True, help_text="Bearbeiter dieser Aufgabe.")
    projekt = models.ForeignKey(Projekt, related_name="projekt", help_text="Das der Aufgabe übergeordnete Projekt.")

    status = models.CharField(max_length=2, default=c.AUFGABE_STATUS_OP, choices=AUFGABE_STATUS, help_text="Bearbeitungsstatus der Aufgabe.")
    prioritaet = models.CharField(max_length=2, default=c.PRIORITAET_ME, choices=PRIORITAET, help_text="Priorität der Aufgabe im Hinblick auf das Projekt.")
    titel = models.CharField(max_length=512, help_text="Der Titel soll eine Idee des Inhalts der Aufgabe geben.")
    beschreibung = models.TextField(blank=True, help_text="Detaillierter Beschreibung der Aufgabe. Was ist das Problem? Unter welchen Bedingungen gilt die Aufgabe als gelöst?")
    erstellDatum = models.DateTimeField(auto_now_add=True, help_text="Die Aufgabe wurde an diesem Tag erstellt.")
    aenderungsDatum = models.DateTimeField(editable=False, auto_now=True, auto_now_add=True, help_text="Zeit der letzten Änderung.")
    faelligkeitsDatum = models.DateTimeField(blank=True, help_text="Die Aufgabe muss bis zu diesem Datum erledigt sein.")

    def save(self):
        '''
        Speichert das Objekt ab. Zuvor wird eine Reihe von Validierungen durchgeführt.

        Validierungen:

        * Name innerhalb des Projekts nicht eindeutig.
        * Fälligkeitsdatum liegt in der Vergangenheit.
        * Projekt ist bereits geschlossen.

        .. throws: IntegrityError Falls eine der Validierungen fehlschlägt.

        '''

        if Aufgabe.objects.filter(titel=self.titel, projekt=self.projekt).exclude(pk=self.pk).count() != 0:
            raise IntegrityError(c.FEHLER_AUFGABE_NAME)
        if self.faelligkeitsDatum < timezone.now():
            raise IntegrityError(c.FEHLER_AUFGABE_DATUM)
        if self.projekt.status == c.PROJEKT_STATUS_CL:
            raise IntegrityError(c.FEHLER_AUFGABE_PROJEKTSTATUS)
        if self.bearbeiter and self.status == c.AUFGABE_STATUS_OP:
            self.status = c.AUFGABE_STATUS_IP
        if not self.bearbeiter and self.status == c.AUFGABE_STATUS_IP:
            self.status = c.AUFGABE_STATUS_OP

        super(Aufgabe, self).save()

    def getStati(self):
        '''
        Erzeugt ein Dictionary mit erlaubten Status-Schlüsseln für die Anzeige in Formularen.

        Erlaubte Wege:

        .. image:: /img/status.png

        '''
        if self.status == c.AUFGABE_STATUS_OP:
            return dict(AUFGABE_STATUS[3:])
        if self.status == c.AUFGABE_STATUS_IP:
            return dict(AUFGABE_STATUS[2:])
        if self.status == c.AUFGABE_STATUS_PA:
            return dict(AUFGABE_STATUS[1:2])
        if self.status == c.AUFGABE_STATUS_CL:
            return dict(AUFGABE_STATUS[1:2])
        return{}

    def __unicode__(self):
        return self.titel
