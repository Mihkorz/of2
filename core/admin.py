from django.contrib import admin

from .models import Pathway, Gene, Node, Component, Relation
from database.forms import ComponentForm, GeneForm, RealtionForm

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
    fields = ['name', 'amcf', 'info', 'comment']
    list_display = ('name', 'organism', 'database', 'node_list', 'gene_list','amcf')
    search_fields = ['name']
    list_filter = ('database', 'organism')
    
    
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
    
admin.site.register(Pathway, PathwayAdmin) 
admin.site.register(Node, NodeAdmin)
admin.site.register(Component, ComponentAdmin)  
admin.site.register(Gene, GeneAdmin) 
admin.site.register(Relation, RelationAdmin)
