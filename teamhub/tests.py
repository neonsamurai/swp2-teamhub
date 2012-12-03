# coding: utf-8
"""
.. module:: tests
   :platform: Unix, Windows
   :synopsis: Unit tests for teamhub package.

.. moduleauthor:: Dennis, Rouslan, Tim, Veronika


"""
import datetime, unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from teamhub.models import Projekt, Aufgabe


class TestCase(TestCase):

    def setUp(self):
        '''Sets the basic test environment. This function is called before every unit test.
        '''
        self.c = Client()
        self.testUser = User(username='tim', email='tim.jagodzinski@gmail.com', is_staff=True)
        self.testUser.set_password("tim")
        self.testUser.save()
        self.c.login(username='tim', password='tim')

    def testProjekt(self):
        '''Unit tests concerning Projekt objects.
        '''
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')

        #Testprojekt wird erstellt
        self.c.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')

        #Prüfung des Testprojekts
        self.assertEqual(Projekt.objects.get(pk=1).besitzer, self.testUser, '---Projektbesitzer ist nicht korrekt!---')
        self.assertEqual(Projekt.objects.get(pk=1).name, 'TestProjekt', '---Projektname ist nicht korrekt!---')
        self.assertEqual(Projekt.objects.get(pk=1).beschreibung, 'Eine Beschreibung des Projekts', '---Projektbeschreibung ist nicht korrekt!---')

        #Testprojekt bearbeiten
        self.c.post('/projekte/' + str(Projekt.objects.get(pk=1).pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': "CL"})

        #Prüfung des Testprojekts
        self.assertEqual(Projekt.objects.get(pk=1).name, 'TestProjektNummer2', '---Projektname ist nicht korrekt!---')
        self.assertEqual(Projekt.objects.get(pk=1).beschreibung, 'Eine andere Beschreibung des Projekts', '---Projektbeschreibung ist nicht korrekt!---')

    def testAufgabe(self):
        '''Unit tests concerning Aufgabe objects.
        '''
        self.c.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        self.assertEqual(Aufgabe.objects.all().count(), 0, '---Aufgabentabelle ist nicht leer!---')

        #Eine gültige Testaufgabe wird erstellt ,'erstellDatum':timezone.now(),'aenderungsDatum':timezone.now()
        self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(pk=1).pk, 'prioritaet': 'ME', 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': '2015-12-12 12:00'})

        #Prüfung der Testaufgabe
        self.assertEqual(Aufgabe.objects.get(pk=1).titel, 'Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).bearbeiter, self.testUser, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).ersteller, self.testUser, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).prioritaet, 'ME', '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).projekt, Projekt.objects.get(pk=1), '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).beschreibung, 'Beschreibung der Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual((Aufgabe.objects.get(pk=1).faelligkeitsDatum + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), '2015-12-12 12:00', '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')

        #Geschäftsregeln testen
        response = self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(pk=1).pk, 'prioritaet': 'ME', 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': '2015-12-12 12:00'})
        self.assertFormError(response, 'form', 'titel', "Es existiert schon eine Aufgabe mit dem Namen!")

        response = self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(pk=1).pk, 'prioritaet': 'ME', 'titel': "Eine andere Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': '2010-12-12 12:00'})
        self.assertFormError(response, 'form', 'faelligkeitsDatum', "Fälligkeitsdatum darf nicht in der Vergangenheit liegen!")

        self.c.post('/projekte/' + str(Projekt.objects.get(pk=1).pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': "CL"})
        response = self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(pk=1).pk, 'prioritaet': 'ME', 'titel': "Eine andere Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': '2010-12-12 12:00'})
        self.assertFormError(response, 'form', None, "Das Projektstatus darf nicht geschlossen sein!")

        #Die Testaufgabe wird verändert
        self.c.post('/projekte/' + str(Projekt.objects.get(pk=1).pk) + '/bearbeiten/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine andere Beschreibung des Projekts', 'status': "OP"})
        self.c.post('/projekte/erstellen/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine Beschreibung des Projekts Nummer 2'})
        testUser1 = User(username='user', email='user@gmail.com', is_staff=True)
        testUser1.set_password("user")
        testUser1.save()
        self.c.post('/aufgabe/' + str(Aufgabe.objects.get(pk=1).pk) + '/bearbeiten/', {'bearbeiter': testUser1.pk, 'projekt': Projekt.objects.get(name='TestProjektNummer2').pk, 'prioritaet': 'LO', 'titel': "Andere Testaufgabe", 'beschreibung': "Beschreibung der anderen Testaufgabe", 'faelligkeitsDatum': '2014-12-12 12:00'})

        #Prüfung der veränderten Testaufgabe
        self.assertEqual(Aufgabe.objects.get(pk=1).titel, 'Andere Testaufgabe', '---Aufgabentitel ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).bearbeiter, testUser1, '---Bearbeiter der Aufgabe ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).ersteller, self.testUser, '---Ersteller der Aufgabe ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).prioritaet, 'LO', '---Aufgabenpriorität ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).projekt, Projekt.objects.get(name='TestProjektNummer2'), '---Projekt der Aufgabe ist nicht korrekt!---')
        self.assertEqual(Aufgabe.objects.get(pk=1).beschreibung, 'Beschreibung der anderen Testaufgabe', '---Aufgabenbeschreibung ist nicht korrekt!---')
        self.assertEqual((Aufgabe.objects.get(pk=1).faelligkeitsDatum + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'), '2014-12-12 12:00', '---Fälligkeitsdatum der Aufgabe ist nicht korrekt!---')

    def testSuche(self):
        '''Unit tests concerning search functionality.
        '''
        self.c.post('/projekte/erstellen/', {'name': 'TestProjekt', 'beschreibung': 'Eine Beschreibung des Projekts'})
        self.c.post('/projekte/erstellen/', {'name': 'TestProjektNummer2', 'beschreibung': 'Eine Beschreibung des 2. Projekts'})
        self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(name='TestProjekt').pk, 'prioritaet': 'ME', 'titel': "Testaufgabe", 'beschreibung': "Beschreibung der Testaufgabe", 'faelligkeitsDatum': '2015-12-12 12:00'})
        self.c.post('/aufgabe/erstellen/', {'bearbeiter': self.testUser.pk, 'projekt': Projekt.objects.get(name='TestProjektNummer2').pk, 'prioritaet': 'ME', 'titel': "TestaufgabeNummer2", 'beschreibung': "Beschreibung der 2. Testaufgabe", 'faelligkeitsDatum': '2015-12-12 12:00'})

        response = self.c.get('/suchen/', {'search': 'Test', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'].all(), Aufgabe.objects.all(), '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'Beschreibung', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'].all(), Aufgabe.objects.all(), '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'Beschreibung der Testaufgabe', 'projekt': ''})
        self.assertItemsEqual(response.context['aufgabe'].all(), Aufgabe.objects.all().filter(titel="Testaufgabe"), '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'Test', 'projekt': 'TestProjekt'})
        self.assertItemsEqual(response.context['aufgabe'].all(), Aufgabe.objects.all().filter(titel="Testaufgabe"), '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': 'TestaufgabeNummer2', 'projekt': 'TestProjekt'})
        self.assertItemsEqual(response.context['aufgabe'].all(), [], '---Falsche Suchergebnisse---')
        response = self.c.get('/suchen/', {'search': '', 'projekt': ''})
        self.assertEqual(response.context['anfrage'], "Bitte geben Sie ein Suchbegriff ein!!!", '---Falsche Suchergebnisse---')


if __name__ == "__main__":
    unittest.main()
