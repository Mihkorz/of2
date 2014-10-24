# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Drug, Target, Pathway, Node, Component, Gene, Relation
from .forms import ComponentForm, GeneForm, RealtionForm

import copy

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse


class TargetInline(admin.TabularInline):
    model = Target
     
class DrugAdmin(admin.ModelAdmin):
    def targets_list(self):
        #return self.target_set.all()
        return ", ".join(target.name for target in self.target_set.all())
    list_display = ('name', 'db', 'tip', targets_list)
    search_fields = ['name']
    exclude = ('targets',)
        
    inlines = [
        TargetInline,
    ]
    
def copy_pathway(modeladmin, request, queryset):
    for path in queryset:
        path_copy = Pathway(name = path.name+'_copy', amcf=path.amcf, info = path.info, comment=path.comment)
        path_copy.save()
        
        for node in path.node_set.all():
            new_node = Node(name=node.name, comment=node.comment, pathway=path_copy)
            new_node.save()
            for component in node.component_set.all():
                new_component = Component(name = component.name, comment=component.comment, node=new_node)
                new_component.save()
        
        for gene in path.gene_set.all():
            new_gene = Gene(name = gene.name, arr=gene.arr, comment=gene.comment, pathway=path_copy, node=new_node)
            new_gene.save()
            
        for node in path.node_set.all():
            for inrel in node.inrelations.all():
                from_new = Node.objects.get(name=inrel.fromnode.name, pathway=path_copy)
                to_new = Node.objects.get(name=inrel.tonode.name, pathway=path_copy)
                new_rel = Relation(fromnode=from_new, tonode=to_new, reltype=inrel.reltype)
                new_rel.save()         

copy_pathway.short_description = "Copy selected pathways"

        
class PathwayAdmin(admin.ModelAdmin):
    actions = [copy_pathway]
    fields = ['name','amcf', 'info', 'comment']
    list_display = ('name', 'node_list', 'gene_list','amcf')
    search_fields = ['name']
    
    
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'pathway','component_list', 'in_rel', 'out_rel')
    search_fields = ['name', 'pathway__name']
    list_filter = ('pathway__name',)
    
class ComponentAdmin(admin.ModelAdmin):
    form = ComponentForm
    list_display = ('name', 'node','pathway')
    search_fields = ['name', 'node__name']
    
class GeneAdmin(admin.ModelAdmin):
    form = GeneForm
    
    list_display = ('name', 'pathway', 'arr')
    search_fields = ['name', 'pathway__name']
    list_filter = ('pathway__name',)
    
class RelationAdmin(admin.ModelAdmin):
    form = RealtionForm
    list_display = ('id', 'reltype','fromnode', 'tonode', 'comment' )
    
class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
    
    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


#admin.site.register(LogEntry, LogEntryAdmin) 
admin.site.register(Drug, DrugAdmin)     
admin.site.register(Pathway, PathwayAdmin) 
admin.site.register(Node, NodeAdmin)
admin.site.register(Component, ComponentAdmin)  
admin.site.register(Gene, GeneAdmin) 
admin.site.register(Relation, RelationAdmin)


