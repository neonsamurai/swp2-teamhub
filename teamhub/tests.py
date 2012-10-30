"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from teamhub.models import Projekt
from django.contrib.auth.models import User

class ProjektTest(TestCase):

    
    def test_Projekt_Erstellen(self):
        #Zwei Testuser werden erstellt
        self.besitzer1=User(username='user',password='1234')
        self.besitzer2=User(username='other_user',password='1234')
        self.besitzer1.save();
        self.besitzer2.save();
        
        #self.queryset=[]
        #Projekt.objects.all()
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
        #Testprojekt wird erstellt
        self.testProjekt = Projekt(besitzer=self.besitzer1, name='testProjekt',beschreibung='Test,test,test!!!',status='OP')
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
        self.testProjekt.save()
        self.assertEqual(Projekt.objects.all().count(), 1, '---Projekttabelle ist nicht korrekt!---')
        
        
        self.assertEqual(self.testProjekt.id, 1,'---Projektid stimmt nicht!---') 
        self.assertEqual(self.testProjekt.name,'testProjekt','---Projektname stimmt nicht!---')        
        self.assertEqual(self.testProjekt.beschreibung,'Test,test,test!!!','---Projektbeschreibung stimmt nicht!---')
        self.assertEqual(self.testProjekt.status,'OP','---Projektstatus stimmt nicht!---')
        self.assertEqual(self.testProjekt.besitzer,self.besitzer1,'---Projektbesitzer stimmt nicht!---')
        
        #Im Testprojekt werden die Daten ausgetauscht
        self.testProjekt.besitzer=self.besitzer2
        self.testProjekt.beschreibung='Eine andere Beschreibung'
        self.testProjekt.name='Projekt-Test'
        self.testProjekt.status='CL'
        self.testProjekt.save()
        
        self.assertEqual(self.testProjekt.name,'Projekt-Test','---Projektname stimmt nicht!---')        
        self.assertEqual(self.testProjekt.beschreibung,'Eine andere Beschreibung','---Projektbeschreibung stimmt nicht!---')
        self.assertEqual(self.testProjekt.status,'CL','---Projektstatus stimmt nicht!---')
        self.assertEqual(self.testProjekt.besitzer,self.besitzer2,'---Projektbesitzer stimmt nicht!---')
        
        
        self.testProjekt.delete();
        self.assertEqual(Projekt.objects.all().count(), 0, '---Projekttabelle ist nicht leer!---')
        
if __name__ == "__main__":
    unittest.main()











