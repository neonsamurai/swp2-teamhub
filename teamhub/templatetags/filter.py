# coding: utf-8
from django import template
from teamhub.models import AUFGABE_STATUS

register = template.Library()

@register.filter(name='getItem')
def get_item(dictionary, key):
    return dict(AUFGABE_STATUS)[key]