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



class ProjektTest(TestCase):
   
    def test_Projekt_Erstellen(self):
        #Zwei Testuser werden erstellt
        besitzer1 = User(username='user', password='1234')
        besitzer2 = User(username='other_user', password='1234')
        besitzer1.save();
        besitzer2.save();
        
        #self.queryset=[]
        #Projekt.objects.all()
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
        #Testprojekt wird erstellt
        self.testProjekt = Projekt(besitzer=besitzer1, name='testProjekt', beschreibung='Test,test,test!!!', status='OP')
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
        testProjekt.save()
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')
        
        
        self.assertEqual(self.testProjekt.id, 1, '---Projektid stimmt nicht!---') 
        self.assertEqual(self.testProjekt.name, 'testProjekt', '---Projektname stimmt nicht!---')        
        self.assertEqual(self.testProjekt.beschreibung, 'Test,test,test!!!', '---Projektbeschreibung stimmt nicht!---')
        self.assertEqual(self.testProjekt.status, 'OP', '---Projektstatus stimmt nicht!---')
        self.assertEqual(self.testProjekt.besitzer, besitzer1, '---Projektbesitzer stimmt nicht!---')
        
        #Im Testprojekt werden die Daten ausgetauscht
        self.testProjekt.besitzer = besitzer2
        self.testProjekt.beschreibung = 'Eine andere Beschreibung'
        self.testProjekt.name = 'Projekt-Test'
        self.testProjekt.status = 'CL'
        self.testProjekt.save()
        
        self.assertEqual(self.testProjekt.name, 'Projekt-Test', '---Projektname stimmt nicht!---')        
        self.assertEqual(self.testProjekt.beschreibung, 'Eine andere Beschreibung', '---Projektbeschreibung stimmt nicht!---')
        self.assertEqual(self.testProjekt.status, 'CL', '---Projektstatus stimmt nicht!---')
        self.assertEqual(self.testProjekt.besitzer, besitzer2, '---Projektbesitzer stimmt nicht!---')
        
        testProjekt.delete();
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
if __name__ == "__main__":
    unittest.main()











