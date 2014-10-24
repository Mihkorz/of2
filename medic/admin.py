from django.contrib import admin

from .models import Nosology, TreatmentMethod

class NosologyAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Nosology, NosologyAdmin) 

class TreatmentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'nosology')

admin.site.register(TreatmentMethod, TreatmentMethodAdmin) 


