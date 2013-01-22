# coding: utf-8
"""
.. module:: tests

:platform: Unix, Windows

:synopsis: Unit tests für teamhub Paket.

.. moduleauthor:: Dennis Lipps


"""
import datetime
import unittest
from django.test import TestCase
from django.test.client import Client
from teamhub.models import Projekt, Aufgabe, AUFGABE_STATUS, TeamhubUser
import teamhub.stringConst as c
from django.utils import timezone
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class TestCase(TestCase):

    def setUp(self):
        '''Sets the basic test environment. This function is called before every unit test.
'''
        self.client = Client()
        self.faelligkeitsDatumRichtig = '2015-12-12 12:00'
        self.faelligkeitsDatumRichtig2 = '2014-12-12 12:00'
        self.faelligkeitsDatumFalsch = '2010-12-12 12:00'

    def testModel(self):

        #Hier wird das Model getestet

        #-------------------TeamhubUser------------------------------------------->

        # Prüfen ob die TeamhubUsertabelle in der Datenbank leer ist:
        self.assertEqual(TeamhubUser.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')

        # TeamhubUser mit Teamleiterrechten erstellen
        testUser=TeamhubUser(username='user', email='user@user.com', is_staff=True)
        testUser.set_password('user')
        testUser.save()

        # Testen ob ein neuer Benutzer erstellt wurde
        testUser=TeamhubUser.objects.get(pk=1)
        self.assertEqual(testUser.username, 'user', '---Benutzername ist nicht korrekt!---')
        self.assertEqual(testUser.email, 'user@user.com', '---Email ist nicht korrekt!---')
        self.assertEqual(testUser.is_staff, True, '---Berechtigung ist nicht korrekt!---')
        self.assertEqual(testUser.check_password('user'), True, '---Passwort ist nicht korrekt!---')

        # Name des Benutzer ändern und Änderung prüfen
        testUser.username='benutzer'
        testUser.save()
        self.assertEqual(testUser.username, 'benutzer', '---Benutzername ist nicht korrekt!---')

        # Email des Benutzer ändern und Änderung prüfen
        testUser.email='benutzer@user.de'
        testUser.save()
        self.assertEqual(testUser.email, 'benutzer@user.de', '---Email ist nicht korrekt!---')

        # Berechtigung des Benutzer ändern und Änderung prüfen
        testUser.is_staff=False
        testUser.save()
        self.assertEqual(testUser.is_staff, False, '---Berechtigung ist nicht korrekt!---')

        # Passwort des Benutzer ändern und Änderung prüfen
        testUser.set_password('benutzer')
        testUser.save()
        self.assertEqual(testUser.check_password('benutzer'), True, '---Berechtigung ist nicht korrekt!---')

        # Testen ob ein Benutzer mit dem gleichen Namen erstellt werden kann
        doppelterNameUser=TeamhubUser(username='benutzer', email='user@user.com', is_staff=True)
        self.assertRaisesRegexp(IntegrityError, 'column username is not unique', doppelterNameUser.save)
        self.assertEqual(TeamhubUser.objects.get(username='benutzer'), testUser, '---Benutzer mit gleichen Namen wurde erstellt!---')

        #Testen ob für Benutzername nur Buchstaben, Zahlen, sowie die Zeichen @-+_ erlaubt sind
        #testUser.username='benutzer leerzeichen'
        #self.assertRaisesRegexp(IntegrityError, c.FEHLER_TEAMHUBUSER_USERNAME_INVALID, testUser.save)

        #<--------------------------------------------------------------------

        #-------------------Projekt------------------------------------------->

        #Vorbereitung
        andereruser=TeamhubUser(username='user1', email='user@user.com', is_staff=True)
        andereruser.save()

        # Prüfen ob die Projekttabelle in der Datenbank leer ist:
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')

        #Ein gültiges Projekt wird erstellt
        testProjekt = Projekt(besitzer=testUser, name='testProjekt', beschreibung='Test,test,test!!!', status=c.PROJEKT_STATUS_OP)
        testProjekt.save()

        #Testen ob ein Projekt erstellt wurde
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')

        #Testen ob alle Daten korrekt gespeichert wurden
        testprojekt = Projekt.objects.get(pk=1)
        self.assertEqual(testprojekt.besitzer, testUser, '---Projektbesitzer ist nicht korrekt!---')
        self.assertEqual(testprojekt.name, 'testProjekt', '---Projektname ist nicht korrekt!---')
        self.assertEqual(testprojekt.beschreibung, 'Test,test,test!!!', '---Projektbeschreibung ist nicht korrekt!---')
        self.assertEqual(testprojekt.status, c.PROJEKT_STATUS_OP, '---Projektstatus ist nicht korrekt!---')

        # Name des Projekts ändern und Änderung prüfen
        testprojekt.name='andesresTestProjekt'
        testprojekt.save()
        self.assertEqual(testprojekt.name, 'andesresTestProjekt', '---Projektname ist nicht korrekt!---')

        # Beschreibung des Projekts ändern und Änderung prüfen
        testprojekt.beschreibung='andesre Beschreibung'
        testprojekt.save()
        self.assertEqual(testprojekt.beschreibung, 'andesre Beschreibung', '---Projektbeschreibung ist nicht korrekt!---')

        # Status des Projekts ändern und Änderung prüfen
        testprojekt.status=c.PROJEKT_STATUS_CL
        testprojekt.save()
        self.assertEqual(testprojekt.status, c.PROJEKT_STATUS_CL, '---Projektstatus ist nicht korrekt!---')

        # Besitzer des Projekts ändern und Änderung prüfen (Nur auf der Modelebene möglich, im laufenden Betrieb hat der Benutzer kein Zugriff auf diese Möglichkeit)
        testprojekt.besitzer=andereruser
        testprojekt.save()
        self.assertEqual(testprojekt.besitzer, andereruser, '---Projektbesitzer ist nicht korrekt!---')

        # Prüfen ob Projektname doppelt sein kann (darf nicht vorkommen)
        doppelterNameProjekt = Projekt(besitzer=testUser, name='andesresTestProjekt', beschreibung='Test,test,test!!!', status=c.PROJEKT_STATUS_OP)
        self.assertRaisesRegexp(IntegrityError, 'column name is not unique', doppelterNameProjekt.save)
        self.assertEqual(Projekt.objects.get(name='andesresTestProjekt'), testprojekt, '---Projekt mit gleichen Namen wurde erstellt!---')

        #<--------------------------------------------------------------------


        #-------------------Aufgabe------------------------------------------->

        #Vorbereitung
        testprojekt.status=c.PROJEKT_STATUS_OP
        testprojekt.save()
        anderesProjekt = Projekt(besitzer=testUser, name='anderesProjekt', beschreibung='Test,test,test!!!', status=c.PROJEKT_STATUS_OP)
        anderesProjekt.save()
        fDatum = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=1), timezone.get_default_timezone()) #Ein Datum-Objekt erstellen(Morgen)
        fDatum1 = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=2), timezone.get_default_timezone()) #Ein Datum-Objekt erstellen(Übermorgen)

        # Prüfen ob die Aufgabentabelle in der Datenbank leer ist
        self.assertEqual(Aufgabe.objects.all().count(), 0, '---Aufgabentabelle ist nicht leer!---')

        #Eine gültige Aufgabe wird erstellt
        testaufgabe = Aufgabe(ersteller=testUser, bearbeiter=testUser, projekt=testprojekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum)
        testaufgabe.save()

        #Testen ob alle Daten korrekt gespeichert wurden
        testaufgabe = Aufgabe.objects.get(pk=1)
        self.assertEqual(testaufgabe.titel, 'Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(testaufgabe.bearbeiter, testUser, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.ersteller, testUser, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.prioritaet, c.PRIORITAET_ME, '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(testaufgabe.projekt, testprojekt, '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.beschreibung, 'Beschreibung der Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual(testaufgabe.faelligkeitsDatum , fDatum, '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.status, c.AUFGABE_STATUS_IP, '---Aufgabenstatus ist nicht korrekt!---')

        # Titel der Aufgabe ändern und Änderung prüfen
        testaufgabe.titel='anderer Titel'
        testaufgabe.save()
        self.assertEqual(testaufgabe.titel, 'anderer Titel', '---Aufgabentitel ist nicht korrekt!---')

        # Beschreibung der Aufgabe ändern und Änderung prüfen
        testaufgabe.beschreibung='andere Beschreibung'
        testaufgabe.save()
        self.assertEqual(testaufgabe.beschreibung, 'andere Beschreibung', '---Aufgabenbeschreibung ist nicht korrekt!---')

        # Priorität der Aufgabe ändern und Änderung prüfen
        testaufgabe.prioritaet=c.PRIORITAET_HI
        testaufgabe.save()
        self.assertEqual(testaufgabe.prioritaet, c.PRIORITAET_HI, '---Aufgabenpriorität ist nicht korrekt!---')
        testaufgabe.prioritaet=c.PRIORITAET_LO
        testaufgabe.save()
        self.assertEqual(testaufgabe.prioritaet, c.PRIORITAET_LO, '---Aufgabenpriorität ist nicht korrekt!---')

        # Bearbeiter der Aufgabe ändern und Änderung prüfen
        testaufgabe.bearbeiter=andereruser
        testaufgabe.save()
        self.assertEqual(testaufgabe.bearbeiter, andereruser, '---Bearbeiter der Aufgabe ist nicht korrekt!---')

        # Fälligkeitsdatum der Aufgabe ändern und Änderung prüfen
        testaufgabe.faelligkeitsDatum=fDatum1
        testaufgabe.save()
        self.assertEqual(testaufgabe.faelligkeitsDatum , fDatum1, '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')

        # Ersteller der Aufgabe ändern und Änderung prüfen (Nur auf der Modelebene möglich, im laufenden Betrieb hat der Benutzer kein Zugriff auf diese Möglichkeit)
        testaufgabe.ersteller=andereruser
        testaufgabe.save()
        self.assertEqual(testaufgabe.ersteller, andereruser, '---Ersteller der Aufgabe ist nicht korrekt!---')

        # Projekt der Aufgabe ändern und Änderung prüfen
        testaufgabe.projekt=anderesProjekt
        testaufgabe.save()
        self.assertEqual(testaufgabe.projekt, anderesProjekt, '---Projekt der Aufgabe ist nicht korrekt!---')

        #Übergänge zwischen verschiedenen Status testen
        self.assertEqual(testaufgabe.status, c.AUFGABE_STATUS_IP, '---Falscher Status---')
        self.assertEqual(testaufgabe.getStati(), dict(AUFGABE_STATUS[2:]), '---Die möglichen Zustände sind nicht korrekt!---')
        testaufgabe.bearbeiter = None
        testaufgabe.save()
        self.assertEqual(testaufgabe.status, c.AUFGABE_STATUS_OP, '---Falscher Status---')
        self.assertEqual(testaufgabe.getStati(), dict(AUFGABE_STATUS[3:]), '---Die möglichen Zustände sind nicht korrekt!---')
        testaufgabe.bearbeiter = testUser
        testaufgabe.save()
        self.assertEqual(testaufgabe.status, c.AUFGABE_STATUS_IP, '---Falscher Status---')
        testaufgabe.status = c.AUFGABE_STATUS_PA
        testaufgabe.save()
        self.assertEqual(testaufgabe.status, c.AUFGABE_STATUS_PA, '---Falscher Status---')
        self.assertEqual(testaufgabe.getStati(), dict(AUFGABE_STATUS[1:2]), '---Die möglichen Zustände sind nicht korrekt!---')
        testaufgabe.status = c.AUFGABE_STATUS_CL
        testaufgabe.save()
        self.assertEqual(testaufgabe.status, c.AUFGABE_STATUS_CL, '---Falscher Status---')
        self.assertEqual(testaufgabe.getStati(), dict(AUFGABE_STATUS[1:2]), '---Die möglichen Zustände sind nicht korrekt!---')

        #Testen, ob eine Aufgabe mit dem gleichen Namen erstellt werden kann
        aufgabe1 = Aufgabe(ersteller=testUser, bearbeiter=testUser, projekt=anderesProjekt, titel='anderer Titel', beschreibung='Beschreibung der Testaufgabe', faelligkeitsDatum=fDatum)
        self.assertRaisesRegexp(IntegrityError, c.FEHLER_AUFGABE_NAME, aufgabe1.save)
        self.assertEqual(Aufgabe.objects.all().count(), 1, '---Eine Aufgabe mit gleichen Namen wurde erstellt!---')

        #Testen, ob eine Aufgabe mit einem Faelligkeitsdatum, das in Vergangenheit liegt, erstellt werden kann
        aufgabe1=Aufgabe(ersteller=testUser, projekt=anderesProjekt, titel='Aufgabe zum Testen', beschreibung='Beschreibung der Testaufgabe', faelligkeitsDatum=fDatum)
        aufgabe1.faelligkeitsDatum = timezone.make_aware(datetime.datetime.now() - datetime.timedelta(days=1), timezone.get_default_timezone())
        self.assertRaisesRegexp(IntegrityError, c.FEHLER_AUFGABE_DATUM, aufgabe1.save)
        self.assertEqual(Aufgabe.objects.all().count(), 1, '---Eine Aufgabe mit falschen Datum wurde erstellt!---')

        #Testen, ob eine Aufgabe in einem Projekt, das den Status "Geschlossen" hat, erstellt werden kann
        testprojekt.status = c.PROJEKT_STATUS_CL
        testprojekt.save()
        aufgabe1 = Aufgabe(ersteller=testUser, bearbeiter=testUser, projekt=testprojekt, titel='Aufgabe zum Testen', beschreibung='Beschreibung der Testaufgabe', faelligkeitsDatum=fDatum)
        self.assertRaisesRegexp(IntegrityError, c.FEHLER_AUFGABE_PROJEKTSTATUS, aufgabe1.save)
        self.assertEqual(Aufgabe.objects.all().count(), 1, '---Eine Aufgabe im geschlossenen Projekt wurde erstellt!---')
        #<--------------------------------------------------------------------

    def testViews(self):

        # Vorbereitung
        testUser = TeamhubUser(username='user', email='user@user.com', is_staff=True)
        testUser.set_password("user")
        testUser.save()

        #-----------------TeamhubUser--------------->

        #Einloggen
        self.client.login(username='user', password='user')
        self.assertIn('_auth_user_id', self.client.session)

        # Einen TeamhubUser ohne Berechtigung Erstellen
        self.client.post('/benutzer/', {'username':'userOhneBerechtigung', 'email':'keineBerechtigung@user.com', 'is_staff':False})

        # Erstellte Benutzer wird getestet
        userOhneBerechtigung=TeamhubUser.objects.get(username='userOhneBerechtigung')
        self.assertEqual(userOhneBerechtigung.username, 'userOhneBerechtigung', '---Benutzername ist nicht korrekt---')
        self.assertEqual(userOhneBerechtigung.email, 'keineBerechtigung@user.com', '---Email ist nicht korrekt---')
        self.assertEqual(userOhneBerechtigung.is_staff, False, '---Benutzerberechtigung ist nicht korrekt---')

        #Ausloggen
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')

        # Validierung von Passwörtern und Passwort ändern
        self.client.login(username='userOhneBerechtigung', password='test')
        response=self.client.post('/passwaendern/',{'passwAlt':'passwort', 'passwNeu1':'12345', 'passwNeu2':'12345'})
        self.assertFormError(response, 'form', None, c.FEHLER_PASSWD_ALT)
        response=self.client.post('/passwaendern/',{'passwAlt':'test', 'passwNeu1':'passwort', 'passwNeu2':'password'})
        self.assertFormError(response, 'form', None, c.FEHLER_PASSWD_NEU)
        response=self.client.post('/passwaendern/',{'passwAlt':'test', 'passwNeu1':'user', 'passwNeu2':'user'})
        self.assertEqual(response.context['erfolg'], c.PASSWD_GEAENDERT, '---Keine Erfolgsmeldung!---')
        userOhneBerechtigung=TeamhubUser.objects.get(username='userOhneBerechtigung')
        self.assertEqual(userOhneBerechtigung.check_password('user'), True, '---Passwort ist nicht korrekt!---')

        # Profil bearbeiten und Fehler bei falschen Benutzernamenformat
        response=self.client.post('/profil/',{'username':'Benutzer mit Leerzeichen', 'first_name':'Max', 'last_name':'Mustermann', 'email':'max@gmail.com'})
        self.assertFormError(response, 'form', 'username', c.FEHLER_TEAMHUBUSER_USERNAME_INVALID)
        self.client.post('/profil/',{'username':'OhneBerechtigung', 'first_name':'Max', 'last_name':'Mustermann', 'email':'max@gmail.com'})
        userOhneBerechtigung=TeamhubUser.objects.get(username='OhneBerechtigung')
        self.assertEqual(userOhneBerechtigung.username, 'OhneBerechtigung', '---Benutzername ist nicht korrekt!---')
        self.assertEqual(userOhneBerechtigung.first_name, 'Max', '---Vorname ist nicht korrekt!---')
        self.assertEqual(userOhneBerechtigung.last_name, 'Mustermann', '---Nachname ist nicht korrekt!---')
        self.assertEqual(userOhneBerechtigung.email, 'max@gmail.com', '---Email ist nicht korrekt!---')

        #Berechtigung prüfen (teamleiterBerechtigung in decorators.py)
        response=self.client.post('/benutzer/')
        self.assertRedirects(response, '/')
        response=self.client.post('/passwzurueck/')
        self.assertRedirects(response, '/')

        # Passwort zurücksetzen
        self.client.get('/logout/')
        self.client.login(username='user', password='user')
        userOhneBerechtigung=TeamhubUser.objects.get(username='OhneBerechtigung')
        self.client.post('/passwzurueck/',{'benutzerliste':userOhneBerechtigung.pk})
        userOhneBerechtigung=TeamhubUser.objects.get(username='OhneBerechtigung')
        self.assertEqual(userOhneBerechtigung.check_password('user'), False, '---Passwort ist nicht korrekt!---')
        self.assertEqual(userOhneBerechtigung.check_password('test'), True, '---Passwort ist nicht korrekt!---')

        #<-------------------------------------------

        #------------------Projekt------------------>

        # Prüfen ob Projekttabelle leer ist
        response=self.client.post('/projekte/')
        self.assertItemsEqual(response.context['projektliste'], [], '---Es sind schon Projekte vorhanden!---')
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')

        # Testprojekt wird erstellt
        self.client.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')
        response=self.client.post('/projekte/')
        self.assertItemsEqual(response.context['projektliste'], Projekt.objects.all(), '---Es wurde kein Projekt erstellt!---')

        # Prüfung des Testprojekts auch ProjektDetails
        testprojekt = Projekt.objects.get(name='TestProjekt')
        response=self.client.post('/projekte/'+str(testprojekt.pk)+'/')
        self.assertEqual(response.context['projekt'], testprojekt, '---Erstellter und gespeicherter Projekt stimmen nicht überein!---')
        self.assertEqual(testprojekt.besitzer, testUser, '---Projektbesitzer ist nicht korrekt!---')
        self.assertEqual(testprojekt.name, 'TestProjekt', '---Projektname ist nicht korrekt!---')
        self.assertEqual(testprojekt.beschreibung, 'Eine Beschreibung des Projekts', '---Projektbeschreibung ist nicht korrekt!---')
        self.assertEqual(testprojekt.status, c.PROJEKT_STATUS_OP, '---Projektstatus ist nicht korrekt!---')

        # Testprojekt bearbeiten
        self.client.post('/projekte/' + str(testprojekt.pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': c.PROJEKT_STATUS_CL})

        # Prüfung des bearbeiteten Testprojekts
        testprojekt = Projekt.objects.get(name='TestProjektNummer2')
        self.assertEqual(testprojekt.name, 'TestProjektNummer2', '---Projektname ist nicht korrekt!---')
        self.assertEqual(testprojekt.beschreibung, 'Eine andere Beschreibung des Projekts', '---Projektbeschreibung ist nicht korrekt!---')
        self.assertEqual(testprojekt.status, c.PROJEKT_STATUS_CL, '---Projektstatus ist nicht korrekt!---')
        response=self.client.post('/projekte/'+str(testprojekt.pk)+'/')
        self.assertEqual(response.context['projekt'], testprojekt, '---Erstellter und gespeicherter Projekt stimmen nicht überein!---')

        # Testen von Zugriffsberechtigungen (teamleiterBerechtigung in decorators.py)
        self.client.get('/logout/')
        self.client.login(username='OhneBerechtigung', password='test')
        response = self.client.post('/projekte/erstellen/')
        self.assertRedirects(response, '/')
        response = self.client.post('/projekte/' + str(testprojekt.pk) + '/bearbeiten/')
        self.assertRedirects(response, '/')
        response = self.client.post('/benutzer/')
        self.assertRedirects(response, '/')



        #<----------------------------------------------------------------------

        #--------------------Aufgabe------------------------------------------->
        # Vorbereitung
        testprojektnummer2 = Projekt(besitzer=testUser, name='Ein Projekt zum Testen', beschreibung='Eine Beschreibung des Projekts Nummer 2',status=c.PROJEKT_STATUS_OP)
        testprojektnummer2.save()

        # Prüfen ob Aufgabentabelle leer ist
        self.assertEqual(Aufgabe.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')

        # Eine gültige Testaufgabe wird erstellt ,'erstellDatum':timezone.now(),'aenderungsDatum':timezone.now()
        self.client.post('/aufgabe/erstellen/', {'bearbeiter': testUser.pk, 'projekt': testprojektnummer2.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})

        # Prüfung der Testaufgabe auch AufgabeDetails
        testaufgabe = Aufgabe.objects.get(pk=1)
        response=self.client.post('/aufgabe/'+str(testaufgabe.pk)+'/')
        self.assertEqual(response.context['aufgabe'], testaufgabe, '---Erstellter und gespeicherte Aufgabe stimmen nicht überein!---')
        self.assertEqual(testaufgabe.titel, 'Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(testaufgabe.bearbeiter, testUser, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.ersteller, userOhneBerechtigung, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.prioritaet, c.PRIORITAET_ME, '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(testaufgabe.projekt, testprojektnummer2, '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.beschreibung, 'Beschreibung der Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual((testaufgabe.faelligkeitsDatum + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), self.faelligkeitsDatumRichtig, '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')

        # Geschäftsregeln testen (gleichzeitig decorateSave in decorators.py)
        response = self.client.post('/aufgabe/erstellen/', {'bearbeiter': testUser.pk, 'projekt': testprojektnummer2.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        self.assertFormError(response, 'form', 'titel', c.FEHLER_AUFGABE_NAME)

        response = self.client.post('/aufgabe/erstellen/', {'bearbeiter': testUser.pk, 'projekt': testprojektnummer2.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Eine andere Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumFalsch})
        self.assertFormError(response, 'form', 'faelligkeitsDatum', c.FEHLER_AUFGABE_DATUM)

        response = self.client.post('/aufgabe/erstellen/', {'bearbeiter': testUser.pk, 'projekt': testprojekt.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Eine andere Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        self.assertFormError(response, 'form', None, c.FEHLER_AUFGABE_PROJEKTSTATUS)

        # Testen ob eine Aufgabe mit gleichem Namen, aber im anderen Projekt erstellt werden kann
        testprojekt.status=c.PROJEKT_STATUS_OP
        testprojekt.save()
        self.client.post('/aufgabe/erstellen/', {'bearbeiter': testUser.pk, 'projekt': testprojekt.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        testaufgabe2 = Aufgabe.objects.get(titel="Testaufgabe", projekt=testprojekt)
        response=self.client.post('/aufgabe/'+str(testaufgabe2.pk)+'/')
        self.assertEqual(response.context['aufgabe'], testaufgabe2, '---Erstellter und gespeicherte Aufgabe stimmen nicht überein!---')

        # Die Testaufgabe wird verändert
        self.client.post('/aufgabe/' + str(testaufgabe.pk) + '/bearbeiten/', {'bearbeiter': userOhneBerechtigung.pk, 'projekt': testprojekt.pk, 'prioritaet': c.PRIORITAET_LO, 'titel': "Andere Testaufgabe", 'beschreibung': "Beschreibung der anderen Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig2})

        # Prüfung der veränderten Testaufgabe
        testaufgabe = Aufgabe.objects.get(pk=1)
        response=self.client.post('/aufgabe/'+str(testaufgabe.pk)+'/')
        self.assertEqual(response.context['aufgabe'], testaufgabe, '---Bearbeitete und gespeicherte Aufgabe stimmen nicht überein!---')
        self.assertEqual(testaufgabe.titel, 'Andere Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(testaufgabe.bearbeiter, userOhneBerechtigung, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.ersteller, userOhneBerechtigung, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.prioritaet, c.PRIORITAET_LO, '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(testaufgabe.projekt, testprojekt, '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.beschreibung, 'Beschreibung der anderen Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual((testaufgabe.faelligkeitsDatum + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), self.faelligkeitsDatumRichtig2, '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')

        # Testen von Zugriffsberechtigungen (aufgabeBearbeitenBerechtigung in decorators.py)
        self.client.get('/logout/')
        userOhneBerechtigung = TeamhubUser(username='keineBerechtigung', email='user@user.com', is_staff=False)
        userOhneBerechtigung.set_password("user")
        userOhneBerechtigung.save()
        self.client.login(username='keineBerechtigung', password='user')
        response = self.client.post('/aufgabe/' + str(testaufgabe.pk) + '/bearbeiten/')
        self.assertRedirects(response, '/')

        #<----------------------------------------------------------------------

        #----------------------Listenansichten--------------------------------->

        # Vorbereitung
        self.client.get('/logout/')
        self.client.login(username='OhneBerechtigung', password='test')
        userOhneBerechtigung=TeamhubUser.objects.get(username='OhneBerechtigung')

        # Dashboard
        response=self.client.post('/')
        self.assertItemsEqual(response.context['meineAufgaben'], Aufgabe.objects.filter(bearbeiter=userOhneBerechtigung).order_by('faelligkeitsDatum'), '---Falsche Lise---')

        # offene Aufgabe anzeigen
        response=self.client.post('/aufgabe/offeneAufgaben/')
        self.assertItemsEqual(response.context['meineAufgaben'], Aufgabe.objects.filter(status=c.AUFGABE_STATUS_OP).order_by('faelligkeitsDatum'), '---Falsche Lise---')

        #von mir erstellte Aufgaben anzeigen
        response=self.client.post('/aufgabe/vonMirErstellteAufgaben/')
        self.assertItemsEqual(response.context['meineAufgaben'], Aufgabe.objects.filter(ersteller=userOhneBerechtigung).order_by('faelligkeitsDatum'), '---Falsche Lise---')


        #<---------------------------------------------------------------------

        #---------------------------Suchfunktion------------------------------>

        # Vorbereitung
        self.client.post('/aufgabe/erstellen/', {'bearbeiter': userOhneBerechtigung.pk, 'projekt': testprojekt.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Testaufgabe für Suche", 'beschreibung': "Beschreibung der Testaufgabe für Suche", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        self.client.post('/aufgabe/erstellen/', {'bearbeiter': userOhneBerechtigung.pk, 'projekt': testprojektnummer2.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "TestaufgabeNummer2 für Suche", 'beschreibung': "Beschreibung der 2. Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})

        # Testen von Suchanfragen
        aufgabeQuery = Aufgabe.objects.all()

        response = self.client.get('/suchen/', {'search': 'Test', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'], aufgabeQuery, '---Falsche Suchergebnisse---')
        response = self.client.get('/suchen/', {'search': 'Beschreibung', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'], aufgabeQuery, '---Falsche Suchergebnisse---')
        response = self.client.get('/suchen/', {'search': 'Beschreibung der Testaufgabe für Suche', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'], aufgabeQuery.filter(titel="Testaufgabe für Suche"), '---Falsche Suchergebnisse---')
        response = self.client.get('/suchen/', {'search': 'Test', 'projekt': 'Ein Projekt zum Testen'})
        self.assertItemsEqual(response.context['aufgabe'], aufgabeQuery.filter(titel="TestaufgabeNummer2 für Suche"), '---Falsche Suchergebnisse---')
        response = self.client.get('/suchen/', {'search': 'TestaufgabeNummer2 für Suche', 'projekt': 'TestProjektNummer2'})
        self.assertItemsEqual(response.context['aufgabe'], [], '---Falsche Suchergebnisse---')
        response = self.client.get('/suchen/', {'search': '', 'projekt': ''})
        self.assertEqual(response.context['anfrage'], "Bitte geben Sie ein Suchbegriff ein!!!", '---Falsche Suchergebnisse---')

        #<---------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()