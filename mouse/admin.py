# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import MouseMapping, MousePathway, MouseGene, \
                    MouseMetabolismPathway, MouseMetabolismGene

class MouseMappingAdmin(admin.ModelAdmin):
    filelds = ['human_gene_symbol', 'mouse_gene_symbol']
    list_display = ('human_gene_symbol', 'mouse_gene_symbol')
    search_fields = ['human_gene_symbol', 'mouse_gene_symbol']

class MousePathwayAdmin(admin.ModelAdmin):
    fields = ['name',  'amcf', 'info', 'comment']
    list_display = ('name', 'amcf', 'gene_list')
    search_fields = ['name']
    
    
class MouseGeneAdmin(admin.ModelAdmin):
    #form = GeneForm
    
    list_display = ('name', 'pathway', 'arr')
    search_fields = ['name', 'pathway__name']
    list_filter = ('pathway__name',)

class MouseMetabolismPathwayAdmin(admin.ModelAdmin):
    fields = ['name',  'amcf', 'info', 'comment']
    list_display = ('name', 'amcf', 'gene_list')
    search_fields = ['name']
    
    
class MouseMetabolismGeneAdmin(admin.ModelAdmin):
    #form = GeneForm
    
    list_display = ('name', 'pathway', 'arr')
    search_fields = ['name', 'pathway__name']
    list_filter = ('pathway__name',)

#admin.site.register(MouseMapping, MouseMappingAdmin)    
#admin.site.register(MousePathway, MousePathwayAdmin)  
#admin.site.register(MouseGene, MouseGeneAdmin)
#admin.site.register(MouseMetabolismPathway, MouseMetabolismPathwayAdmin)  
#admin.site.register(MouseMetabolismGene, MouseMetabolismGeneAdmin)  