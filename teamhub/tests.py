# coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from teamhub.models import Projekt, Aufgabe
from django.contrib.auth.models import User
#from django.test.client import Client
from django.utils import timezone
import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

class AufgabeTest(TestCase):
    def test_Aufgabe(self):
        user=User(username='user', email='user@user.com', password='user')
        user.save()
        testProjekt=Projekt(besitzer=user, name='testProjekt',beschreibung='Test,test,test!!!',status='OP')
        testProjekt.save()
        #Ein Datum-Objekt erstellen(Morgen)
        fDatum=timezone.make_aware(datetime.datetime.now()+datetime.timedelta(days=1), timezone.get_default_timezone())
        
        #Eine gültige Aufgabe erstellen
        aufgabe=Aufgabe(ersteller=user, bearbeiter=user, projekt=testProjekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum)
        aufgabe.save()
        
        #Testen, ob eine Aufgabe mit dem gleichen Namen erstellt werden kann 
        aufgabe1=Aufgabe(ersteller=user, bearbeiter=user, projekt=testProjekt, titel="Testaufgabe", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum)   
        self.assertRaisesRegexp(IntegrityError, 'Es existiert schon eine Aufgabe mit dem Namen: Testaufgabe!', aufgabe1.save)
        
        #Testen, ob eine Aufgabe mit einem Faelligkeitsdatum, das in Vergangenheit liegt, erstellt werden kann
        aufgabe.faelligkeitsDatum=timezone.make_aware(datetime.datetime.now()-datetime.timedelta(days=1), timezone.get_default_timezone())  
        self.assertRaisesRegexp(IntegrityError, 'Fälligkeitsdatum darf nicht in der Vergangenheit liegen!', aufgabe.save)
        
        #Testen, ob eine Aufgabe in einem Projekt, das den Status "Geschlossen" hat, erstellt werden kann
        testProjekt.status="CL"
        testProjekt.save()
        aufgabe1=Aufgabe(ersteller=user, bearbeiter=user, projekt=testProjekt, titel="Aufgabe zum Testen", beschreibung="Beschreibung der Testaufgabe", faelligkeitsDatum=fDatum) 
        self.assertRaisesRegexp(ValidationError, 'Das Projektstatus darf nicht geschlossen sein!', aufgabe1.save)


'''
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
'''       
if __name__ == "__main__":
    unittest.main()











