# coding: utf-8
"""
.. module:: tests
:platform: Unix, Windows
:synopsis: Unit tests for teamhub package.

.. moduleauthor:: Dennis, Ruslan, Tim, Veronika


"""
import datetime, unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from teamhub.models import Projekt, Aufgabe, AUFGABE_STATUS
import teamhub.stringConst as c
from django.utils import timezone
from django.db.utils import IntegrityError

class TestCase(TestCase):

    def setUp(self):
        '''Sets the basic test environment. This function is called before every unit test.
'''
        self.c = Client()
        self.testUser = User(username='tim', email='tim.jagodzinski@gmail.com', is_staff=True)
        self.testUser.set_password("tim")
        self.testUser.save()
        self.c.login(username='tim', password='tim')
        self.faelligkeitsDatumRichtig='2015-12-12 12:00'
        self.faelligkeitsDatumRichtig2='2014-12-12 12:00'
        self.faelligkeitsDatumFalsch='2010-12-12 12:00'

    def testProjekt(self):
        '''Unit tests concerning Projekt objects.
'''
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')

        #Testprojekt wird erstellt
        self.c.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')

        #Prüfung des Testprojekts
        testprojekt=Projekt.objects.get(pk=1)
        self.assertEqual(testprojekt.besitzer, self.testUser, '---Projektbesitzer ist nicht korrekt!---')
        self.assertEqual(testprojekt.name, 'TestProjekt', '---Projektname ist nicht korrekt!---')
        self.assertEqual(testprojekt.beschreibung, 'Eine Beschreibung des Projekts', '---Projektbeschreibung ist nicht korrekt!---')

        #Testprojekt bearbeiten
        self.c.post('/projekte/' + str(testprojekt.pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': c.PROJEKT_STATUS_CL})

        #Prüfung des Testprojekts
        testprojekt=Projekt.objects.get(pk=1)
        self.assertEqual(testprojekt.name, 'TestProjektNummer2', '---Projektname ist nicht korrekt!---')
        self.assertEqual(testprojekt.beschreibung, 'Eine andere Beschreibung des Projekts', '---Projektbeschreibung ist nicht korrekt!---')
        
        #Testen von Zugriffsberechtigungen        
        userOhneBerechtigung=User(username='user', email='user@user.com', is_staff=False)
        userOhneBerechtigung.set_password("user")
        userOhneBerechtigung.save()
        self.c.login(username='user', password='user')
        response=self.c.post('/projekte/erstellen/')
        self.assertRedirects(response, '/')
        response=self.c.post('/projekte/' + str(testprojekt.pk) + '/bearbeiten/')
        self.assertRedirects(response, '/')
        response=self.c.post('/benutzer/')
        self.assertRedirects(response, '/')

    def testAufgabe(self):
        '''Unit tests concerning Aufgabe objects.
'''
        self.c.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        projekt=Projekt.objects.get(pk=1)
        self.assertEqual(Aufgabe.objects.all().count(), 0, '---Aufgabentabelle ist nicht leer!---')
        
        #Eine gültige Testaufgabe wird erstellt ,'erstellDatum':timezone.now(),'aenderungsDatum':timezone.now()
        self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': projekt.pk, 'prioritaet': 'ME', 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})

        #Prüfung der Testaufgabe
        testaufgabe=Aufgabe.objects.get(pk=1)
        self.assertEqual(testaufgabe.titel, 'Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(testaufgabe.bearbeiter, self.testUser, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.ersteller, self.testUser, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.prioritaet, 'ME', '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(testaufgabe.projekt, projekt, '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.beschreibung, 'Beschreibung der Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual((testaufgabe.faelligkeitsDatum + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), '2015-12-12 12:00', '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')

        #Geschäftsregeln testen
        response = self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': projekt.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        self.assertFormError(response, 'form', 'titel', c.FEHLER_AUFGABE_NAME)

        response = self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': projekt.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Eine andere Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumFalsch})
        self.assertFormError(response, 'form', 'faelligkeitsDatum', c.FEHLER_AUFGABE_DATUM)

        self.c.post('/projekte/' + str(projekt.pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': c.PROJEKT_STATUS_CL})
        response = self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': projekt.pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Eine andere Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        self.assertFormError(response, 'form', None, c.FEHLER_AUFGABE_PROJEKTSTATUS)

        #Die Testaufgabe wird verändert
        self.c.post('/projekte/' + str(projekt.pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': c.PROJEKT_STATUS_OP})
        self.c.post('/projekte/erstellen/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine Beschreibung des Projekts Nummer 2'})
        testprojektnummer2=Projekt.objects.get(name='TestProjektNummer2')
        testUser1 = User(username='user', email='user@gmail.com', is_staff=True)
        testUser1.set_password("user")
        testUser1.save()
        self.c.post('/aufgabe/' + str(testaufgabe.pk) + '/bearbeiten/', {'bearbeiter': testUser1.pk, 'projekt': testprojektnummer2.pk, 'prioritaet': c.PRIORITAET_LO, 'titel': "Andere Testaufgabe", 'beschreibung': "Beschreibung der anderen Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig2})

        #Prüfung der veränderten Testaufgabe
        testaufgabe=Aufgabe.objects.get(pk=1)
        self.assertEqual(testaufgabe.titel, 'Andere Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(testaufgabe.bearbeiter, testUser1, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.ersteller, self.testUser, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.prioritaet, 'LO', '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(testaufgabe.projekt, testprojektnummer2, '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(testaufgabe.beschreibung, 'Beschreibung der anderen Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual((testaufgabe.faelligkeitsDatum + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), self.faelligkeitsDatumRichtig2, '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')
        
        #Testen von Zugriffsberechtigungen 
        userOhneBerechtigung=User(username='user1', email='user@user.com', is_staff=False)
        userOhneBerechtigung.set_password("user")
        userOhneBerechtigung.save()
        self.c.login(username='user1', password='user')
        response=self.c.post('/aufgabe/' + str(testaufgabe.pk) + '/bearbeiten/')
        self.assertRedirects(response, '/')
        
    def testAufgabeStatusUebergaengeundSaveMethodeAufgabe(self):      
        testProjekt=Projekt(besitzer=self.testUser, name='testProjekt',beschreibung='Test,test,test!!!',status=c.PROJEKT_STATUS_OP)
        testProjekt.save()
        
        #Ein Datum-Objekt erstellen(Morgen)
        fDatum=timezone.make_aware(datetime.datetime.now()+datetime.timedelta(days=1), timezone.get_default_timezone())
        
        #Eine gültige Aufgabe erstellen
        aufgabe=Aufgabe(ersteller=self.testUser, projekt=testProjekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum)
        aufgabe.save()
        
        #Übergänge zwischen verschiedenen Status testen
        self.assertEqual(aufgabe.status,c.AUFGABE_STATUS_OP,'---Falscher Status---')
        self.assertEqual(aufgabe.getStati(),dict(AUFGABE_STATUS[3:]),'---Die möglichen Zustände sind nicht korrekt!---')
        aufgabe.bearbeiter=self.testUser
        aufgabe.save()
        self.assertEqual(aufgabe.status,c.AUFGABE_STATUS_IP,'---Falscher Status---')
        self.assertEqual(aufgabe.getStati(),dict(AUFGABE_STATUS[2:]),'---Die möglichen Zustände sind nicht korrekt!---')
        aufgabe.bearbeiter=None
        aufgabe.save()
        self.assertEqual(aufgabe.status,c.AUFGABE_STATUS_OP,'---Falscher Status---')
        aufgabe.status=c.AUFGABE_STATUS_PA
        aufgabe.save()
        self.assertEqual(aufgabe.getStati(),dict(AUFGABE_STATUS[1:2]),'---Die möglichen Zustände sind nicht korrekt!---')
        
        
        #Testen, ob eine Aufgabe mit dem gleichen Namen erstellt werden kann
        aufgabe1=Aufgabe(ersteller=self.testUser, bearbeiter=self.testUser, projekt=testProjekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum)
        self.assertRaisesRegexp(IntegrityError, c.FEHLER_AUFGABE_NAME, aufgabe1.save)
        
        #Testen, ob eine Aufgabe mit einem Faelligkeitsdatum, das in Vergangenheit liegt, erstellt werden kann
        aufgabe.faelligkeitsDatum=timezone.make_aware(datetime.datetime.now()-datetime.timedelta(days=1), timezone.get_default_timezone())
        self.assertRaisesRegexp(IntegrityError, c.FEHLER_AUFGABE_DATUM, aufgabe.save)
        
        #Testen, ob eine Aufgabe in einem Projekt, das den Status "Geschlossen" hat, erstellt werden kann
        testProjekt.status=c.PROJEKT_STATUS_CL
        testProjekt.save()
        aufgabe1=Aufgabe(ersteller=self.testUser, bearbeiter=self.testUser, projekt=testProjekt, titel="Aufgabe zum Testen", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum)
        self.assertRaisesRegexp(IntegrityError, c.FEHLER_AUFGABE_PROJEKTSTATUS, aufgabe1.save)
        
        
        
    def testSuche(self):
        '''Unit tests concerning search functionality.
'''
        self.c.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        self.c.post('/projekte/erstellen/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine Beschreibung des 2. Projekts'})
        self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(name='TestProjekt').pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(name='TestProjektNummer2').pk, 'prioritaet': c.PRIORITAET_ME, 'titel': "TestaufgabeNummer2", 'beschreibung': "Beschreibung der 2. Testaufgabe", 'faelligkeitsDatum': self.faelligkeitsDatumRichtig})
        
        aufgabeQuery=Aufgabe.objects.all()
        
        response = self.c.get('/suchen/', {'search': 'Test', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'].all(), aufgabeQuery, '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'Beschreibung', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'].all(), aufgabeQuery, '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'Beschreibung der Testaufgabe', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'].all(), aufgabeQuery.filter(titel="Testaufgabe"), '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'Test', 'projekt': 'TestProjekt'})
        self.assertItemsEqual(response.context['aufgabe'].all(), aufgabeQuery.filter(titel="Testaufgabe"), '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'TestaufgabeNummer2', 'projekt': 'TestProjekt'})
        self.assertItemsEqual(response.context['aufgabe'].all(), [], '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': '', 'projekt': ''})
        self.assertEqual(response.context['anfrage'], "Bitte geben Sie ein Suchbegriff ein!!!", '---Falsche Suchergebnisse---')
              
    def test_login(self):
        self.c.login(username='tim', password='tim')
        self.assertIn('_auth_user_id', self.c.session)
        
    def test_logout(self):
        self.c.login(username='tim', password='tim')
        response = self.c.get('/logout/')
        self.assertRedirects(response, '/login/')


if __name__ == "__main__":
    unittest.main()