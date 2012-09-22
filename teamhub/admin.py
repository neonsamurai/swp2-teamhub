from django.contrib import admin
from teamhub.models import Aufgabe

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