# coding: utf-8
from django.contrib.auth.models import User

class lgUser:
   def user_have_permissions(self, user):
       return user.is_staff
   
   def user_erstellen(self, user):
       if User.objects.filter(username=user.username).count()!=0:
           return False
       user.save()
       user.set_password("test")
       user.save()
       return True   