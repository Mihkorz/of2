# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Pathway

class PathwayList(ListView):
    """
    List of Pathways in BioChem DB section
    """    
    model = Pathway
    template_name = 'database/pathway_list.html'
    context_object_name = 'pathways'
    paginate_by = 20
        
    def get_context_data(self, **kwargs):
        context = super(PathwayList, self).get_context_data(**kwargs)        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PathwayList, self).dispatch(request, *args, **kwargs)
      
    
class PathwayDetail(DetailView):
    """
    Details page for particular pathway
    """
    model = Pathway
    template_name = 'database/pathway_detail.html'
    context_object_name = 'pathway'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PathwayDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(PathwayDetail, self).get_context_data(**kwargs)
        
        dRelations = []
        for node in self.object.node_set.all(): # drawing relations 
            for inrel in node.inrelations.all():
                relColor = 'black'
                if inrel.reltype == '1':
                    relColor = 'green'
                if inrel.reltype == '0':
                    relColor = 'red'
                dRelations.append({ inrel.fromnode.name : [inrel.tonode.name, relColor] })      
        context['dRelations'] = dRelations
        return context