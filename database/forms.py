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
        self.fields['fromnode'].choices = nodes_by_pathway()
        self.fields['tonode'].choices = nodes_by_pathway()
    
class GeneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GeneForm, self).__init__(*args, **kwargs)
        #self.fields['node'].choices = nodes_by_pathway()
    
def nodes_by_pathway():
    choices = []
    
    for path in Pathway.objects.all().prefetch_related('node_set'):
        new_path  = []
        sub_nodes = []
        
        for node in path.node_set.all():
            sub_nodes.append([node.id, node.name])
        
        new_path = [path.name, sub_nodes]
        choices.append(new_path)
        
    return choices

            