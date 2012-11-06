"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from teamhub.models import Projekt, Aufgabe
from django.contrib.auth.models import User
from django.test.client import Client
from teamhub.lg.lg_Aufgabe import lgAufgabe
from teamhub.lg.lg_Projekt import lgProjekt
from teamhub.lg.lg_User import lgUser
from django.utils import timezone
import datetime

class AufgabeViewsTestCase(TestCase):
            
    def setUp(self):
        self.c = Client()
        User.objects.create_user(username='tim', email='tim.jagodzinski@gmail.com', password='tim')
        testUser = User.objects.get(username='tim')
        Projekt.objects.create(besitzer=testUser, name='Testprojekt', beschreibung='Beschreibung des Testprojekts', status='OP')
        testProjekt = Projekt.objects.get(pk=1)
        Aufgabe.objects.create(ersteller=testUser, bearbeiter=testUser, projekt=testProjekt, titel="Testaugabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum='2015-12-12 12:00')
        testAufgabe = Aufgabe.objects.get(pk=1)
    
    def test_login(self):
        self.c.login(username='tim', password='tim')
        self.assertIn('_auth_user_id', self.c.session)
    
    def test_dashboard(self):
        self.c.login(username='tim', password='tim')
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('meineAufgaben' in response.context)
        self.assertEqual(response.context['meineAufgaben'][0].pk, 1)
        
    def test_logout(self):
        self.c.login(username='tim', password='tim')
        response = self.c.get('/logout/')
        self.assertRedirects(response, '/login/')

class ProjektTest(TestCase):

    
    def test_Projekt_Erstellen(self):
        #Zwei Testuser werden erstellt
        besitzer1=User(username='user',password='1234')
        besitzer2=User(username='other_user',password='1234')
        besitzer1.save();
        besitzer2.save();
        
        #self.queryset=[]
        #Projekt.objects.all()
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
        #Testprojekt wird erstellt
        testProjekt = Projekt(besitzer=besitzer1, name='testProjekt',beschreibung='Test,test,test!!!',status='OP')
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
        testProjekt.save()
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')
        
        
        self.assertEqual(testProjekt.id, 1,'---Projektid stimmt nicht!---') 
        self.assertEqual(testProjekt.name,'testProjekt','---Projektname stimmt nicht!---')        
        self.assertEqual(testProjekt.beschreibung,'Test,test,test!!!','---Projektbeschreibung stimmt nicht!---')
        self.assertEqual(testProjekt.status,'OP','---Projektstatus stimmt nicht!---')
        self.assertEqual(testProjekt.besitzer, besitzer1,'---Projektbesitzer stimmt nicht!---')
        
        #Im Testprojekt werden die Daten ausgetauscht
        testProjekt.besitzer=besitzer2
        testProjekt.beschreibung='Eine andere Beschreibung'
        testProjekt.name='Projekt-Test'
        testProjekt.status='CL'
        testProjekt.save()
        
        self.assertEqual(testProjekt.name,'Projekt-Test','---Projektname stimmt nicht!---')        
        self.assertEqual(testProjekt.beschreibung,'Eine andere Beschreibung','---Projektbeschreibung stimmt nicht!---')
        self.assertEqual(testProjekt.status,'CL','---Projektstatus stimmt nicht!---')
        self.assertEqual(testProjekt.besitzer,besitzer2,'---Projektbesitzer stimmt nicht!---')
        
        
        testProjekt.delete();
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
class Lg_Test(TestCase):
    
    def test_lgProjekt(self):
        user=User(username='user', email='user@user.com', password='user', is_staff=True)
        user.save()
        testProjekt=Projekt(besitzer=user, name='testProjekt',beschreibung='Test,test,test!!!',status='OP')
        self.assertTrue(lgProjekt().lg_projekt_isValid(testProjekt))
        self.assertEqual(Projekt.objects.get(name='testProjekt'), testProjekt)
        
        testProjekt1=Projekt(besitzer=user, name='testProjekt',beschreibung='Test,test,test!!!',status='OP')
        self.assertFalse(lgProjekt().lg_projekt_isValid(testProjekt1))
        self.assertEqual(Projekt.objects.filter(name='testProjekt').count(), 1)

        testProjekt.beschreibung="Andere Beschreibung!"
        self.assertTrue(lgProjekt().lg_projekt_isValid(testProjekt))
        self.assertEqual(Projekt.objects.get(name='testProjekt').beschreibung, "Andere Beschreibung!")
        
    def test_lgAufgabe(self):
        user=User(username='user', email='user@user.com', password='user', is_staff=True)
        user.save()
        testProjekt=Projekt(besitzer=user, name='testProjekt',beschreibung='Test,test,test!!!',status='OP')
        testProjekt.save()
        aufgabe=Aufgabe(ersteller=user, bearbeiter=user, projekt=testProjekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=timezone.now())
        
        self.assertTrue(lgAufgabe().lg_aufgabe_isValid(aufgabe))
        self.assertEqual(Aufgabe.objects.filter(titel="Testaufgabe").count(), 1)
        
        aufgabe1=Aufgabe(ersteller=user, bearbeiter=user, projekt=testProjekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=timezone.now())
        self.assertFalse(lgAufgabe().lg_aufgabe_isValid(aufgabe1))
        self.assertEqual(Aufgabe.objects.filter(titel="Testaufgabe").count(), 1)
        
        aufgabe.faelligkeitsDatum = timezone.now() - datetime.timedelta(days=1)
        self.assertFalse(lgAufgabe().lg_aufgabe_isValid(aufgabe))

        testProjekt1=Projekt(besitzer=user, name='Projekttest',beschreibung='Test,test,test!!!',status='CL')
        testProjekt.save()
        aufgabe.projekt=testProjekt1
        self.assertFalse(lgAufgabe().lg_aufgabe_isValid(aufgabe))
        
if __name__ == "__main__":
    unittest.main()











