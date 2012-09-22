from django.contrib import admin
from teamhub.models import Aufgabe, Projekt

class AufgabeAdmin(admin.ModelAdmin):
    list_display = ('titel', 'ersteller', 'erstellDatum')
    
# Auto populate ForeignKey field ersteller on save in admin site
    def save_model(self, request, obj, form, change): 
        obj.ersteller = request.user
        obj.save()

    def save_formset(self, request, form, formset, change): 
        if formset.model == Aufgabe:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.ersteller = request.user
                instance.save()
        else:
            formset.save()
            
admin.site.register(Aufgabe, AufgabeAdmin)

class ProjektAdmin(admin.ModelAdmin):
    list_display = ('name', 'besitzer')
    
# Auto populate ForeignKey field ersteller on save in admin site
    def save_model(self, request, obj, form, change): 
        obj.besitzer = request.user
        obj.save()

    def save_formset(self, request, form, formset, change): 
        if formset.model == Projekt:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.besitzer = request.user
                instance.save()
        else:
            formset.save()
            
admin.site.register(Projekt, ProjektAdmin)