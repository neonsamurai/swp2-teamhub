from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from teamhub.models import Aufgabe, Projekt
from teamhub.forms import projektForm

def projektErstellen(form):
    if form.is_valid():
        newProject = form.save()
        return newProject