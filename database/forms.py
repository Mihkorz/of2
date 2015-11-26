# -*- coding: utf-8 -*-
import logging

from django import forms

from core.models import Pathway


logger = logging.getLogger('Oncofinder')


class PathwayUpdateForm(forms.ModelForm):
    
    class Meta(object):
        model = Pathway
        exclude = ('info', 'comment', )
    

class ComponentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)
        self.fields['node'].choices = nodes_by_pathway()
        
class RealtionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RealtionForm, self).__init__(*args, **kwargs)
        
        try:
            current_rel = kwargs['instance']
            current_path_db = current_rel.fromnode.pathway.database
            current_path_org = current_rel.fromnode.pathway.organism
            
        except:
            current_path_db = current_path_org = None
            
        
            
        
        
        self.fields['fromnode'].choices = nodes_by_pathway(current_path_db, current_path_org)
        self.fields['tonode'].choices = nodes_by_pathway(current_path_db, current_path_org)
        
        
    
class GeneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GeneForm, self).__init__(*args, **kwargs)
        #self.fields['node'].choices = nodes_by_pathway()
    
def nodes_by_pathway(db, organism):
    choices = []
    if db and organism:
        paths = Pathway.objects.filter(organism=organism, database=db).prefetch_related('node_set')
    else:
        paths = Pathway.objects.filter(organism='human', database__in=['primary_old','primary_new']).order_by('database', 'name').prefetch_related('node_set')
    for path in paths:
        new_path  = []
        sub_nodes = []
        
        for node in path.node_set.all():
            sub_nodes.append([node.id, node.name])
        
        new_path = [path.name+' org: '+path.organism+' db: '+path.database, sub_nodes]
        choices.append(new_path)
        
    return choices

            