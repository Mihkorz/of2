# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Report, GeneGroup

class GeneGroupInline(admin.TabularInline):
    model = GeneGroup
     
class ReportAdmin(admin.ModelAdmin):
    def targets_list(self):
        #return self.target_set.all()
        return ", ".join(target.name for target in self.target_set.all())
    list_display = ('title', 'organization', 'created_at')
    search_fields = ['title', 'organization']
    
        
    inlines = [
        GeneGroupInline,
    ]

class GeneGroupAdmin(admin.ModelAdmin):
    fields = ['name','tip', 'drug']
    list_display = ('name', 'tip', 'drug')
    search_fields = ['name', 'drug__name']
    list_filter = ('drug__name',)


admin.site.register(Report, ReportAdmin)