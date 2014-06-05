# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Pathway, Drug

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
        context['allPathways'] = Pathway.objects.count()        
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

class PathwayAjaxSearch(ListView):
    """
    Renders objects for Ajax Search
    """
    model = Pathway
    template_name = 'database/pathway_ajax_search.html'
    context_object_name = 'pathways'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return Pathway.objects.filter(name__icontains=q)
    
    
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
    