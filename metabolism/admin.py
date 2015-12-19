# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import MetabolismPathway, MetabolismGene

class MetabolismPathwayAdmin(admin.ModelAdmin):
    fields = ['name', 'pathway_id', 'link_to_picture','amcf', 'info', 'comment']
    list_display = ('name', 'amcf')
    search_fields = ['name']
    
    
class MetabolismGeneAdmin(admin.ModelAdmin):
    #form = GeneForm
    
    list_display = ('name', 'pathway', 'arr')
    search_fields = ['name', 'pathway__name']
    list_filter = ('pathway__name',)
    
#admin.site.register(MetabolismPathway, MetabolismPathwayAdmin)  
#admin.site.register(MetabolismGene, MetabolismGeneAdmin) 