# -*- coding: utf-8 -*-

import networkx as nx

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import  Drug
from core.models import Pathway


class PathwayList(ListView):
    """
    List of Pathways in BioChem DB section
    """    
    template_name = 'database/pathway_list.html'
    context_object_name = 'pathways'
    paginate_by = 20
    
    
    def get_queryset(self):
        qs = Pathway.objects.filter(organism=self.kwargs['organism'], database=self.kwargs['database']) 
        return qs
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PathwayList, self).dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(PathwayList, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['allPathways'] = queryset.count()
        context['organism'] = self.kwargs['organism']
        context['database'] = self.kwargs['database']
        return context
        
      
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
        
        G=nx.DiGraph() #drawing static picture
        for node in self.object.node_set.all():
            G.add_node(node, color='black',style='filled',
                               fillcolor='white')
        
        dRelations = []
        for node in self.object.node_set.all(): # drawing relations
             
            for inrel in node.inrelations.all():
                relColor = 'black'
                if inrel.reltype == '1':
                    relColor = 'green'
                if inrel.reltype == '0':
                    relColor = 'red'
                dRelations.append({ inrel.fromnode.name : [inrel.tonode.name, relColor] })
                G.add_edge(inrel.fromnode.name.encode('ascii','ignore'), 
                            inrel.tonode.name.encode('ascii','ignore'), color=relColor)      
        
        A=nx.to_agraph(G)
        A.layout(prog='dot')
        
        A.draw(settings.MEDIA_ROOT+"/pathway_pics/"+self.object.organism+"/"+self.object.database+"/"+self.object.name+".svg")
        
        context['dRelations'] = dRelations
        context['organism'] = self.kwargs['organism']
        context['database'] = self.kwargs['database']
        
        
        
        
        
        return context

class PathwayAjaxSearch(ListView):
    """
    Renders objects for Ajax Search
    """
    model = Pathway
    template_name = 'database/pathway_ajax_search.html'
    context_object_name = 'pathways'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        organism = self.request.GET.get('o', '')
        database = self.request.GET.get('db', '')
        return Pathway.objects.filter(name__icontains=q, organism=organism, database=database)
    
    
class DrugList(ListView):
    """
    List of all Drugs in Drugs DB section
    """
    
    model = Drug
    template_name = 'database/drug_list.html'
    context_object_name = 'drugs'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super(DrugList, self).get_context_data(**kwargs)
        context['allDrugs'] = Drug.objects.count()       
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DrugList, self).dispatch(request, *args, **kwargs) 

 
class DrugDetail(DetailView):
    """
    Details page for particular Drug
    """
    
    model = Drug
    template_name = 'database/drug_detail.html'
    context_object_name = 'drug'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DrugDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DrugDetail, self).get_context_data(**kwargs)

        return context

class DrugAjaxSearch(ListView):
    """
    List of all Drugs in Drugs DB section
    """
    
    model = Drug
    template_name = 'database/drug_ajax_search.html'
    context_object_name = 'drugs'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return Drug.objects.filter(name__icontains=q)
    