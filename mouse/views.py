# -*- coding: utf-8 -*-
import csv


from pandas import read_csv

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import MousePathway, MouseMapping, MouseMetabolismPathway 
#from database.models import Pathway, Gene

class MousePathwayList(ListView):
    """
    List of Pathways in BioChem DB section
    """    
    model = MousePathway
    template_name = 'mouse/pathway_list.html'
    context_object_name = 'pathways'
    paginate_by = 20
        
    def get_context_data(self, **kwargs):
        context = super(MousePathwayList, self).get_context_data(**kwargs)
        context['allPathways'] = MousePathway.objects.count()        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MousePathwayList, self).dispatch(request, *args, **kwargs)
      
    
class MousePathwayDetail(DetailView):
    """
    Details page for particular pathway
    """
    model = MousePathway
    template_name = 'mouse/pathway_detail.html'
    context_object_name = 'pathway'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MousePathwayDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MousePathwayDetail, self).get_context_data(**kwargs)
        return context

class MousePathwayAjaxSearch(ListView):
    """
    Renders objects for Ajax Search
    """
    model = MousePathway
    template_name = 'mouse/pathway_ajax_search.html'
    context_object_name = 'pathways'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return MousePathway.objects.filter(name__icontains=q)
    
class MouseMapping(ListView):
    """
    List of Human-Mouse Gene Mapping
    """    
    model = MouseMapping
    template_name = 'mouse/mapping.html'
    context_object_name = 'mappings'
    paginate_by = 100
        
    def get_context_data(self, **kwargs):
        context = super(MouseMapping, self).get_context_data(**kwargs)
        context['allPathways'] = MousePathway.objects.count()        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MouseMapping, self).dispatch(request, *args, **kwargs)
        
"""""""""""""""""""""""'  METABOLISM """"""""""""""
"""

class MouseMetabolismPathwayList(ListView):
    """
    List of Pathways in BioChem DB section
    """    
    model = MouseMetabolismPathway
    template_name = 'mouse/meta_pathway_list.html'
    context_object_name = 'pathways'
    paginate_by = 20
        
    def get_context_data(self, **kwargs):
        context = super(MouseMetabolismPathwayList, self).get_context_data(**kwargs)
        context['allPathways'] = MouseMetabolismPathway.objects.count()        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MouseMetabolismPathwayList, self).dispatch(request, *args, **kwargs)
      
    
class MouseMetabolismPathwayDetail(DetailView):
    """
    Details page for particular pathway
    """
    model = MouseMetabolismPathway
    template_name = 'mouse/meta_pathway_detail.html'
    context_object_name = 'pathway'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MouseMetabolismPathwayDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MouseMetabolismPathwayDetail, self).get_context_data(**kwargs)
        return context

class MouseMetabolismPathwayAjaxSearch(ListView):
    """
    Renders objects for Ajax Search
    """
    model = MouseMetabolismPathway
    template_name = 'mouse/pathway_ajax_search.html'
    context_object_name = 'pathways'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return MouseMetabolismPathway.objects.filter(name__icontains=q)
    
     
class MouseTest(TemplateView):
    """
    Just Testing Playground
    """
    template_name = 'mouse/test.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #messages.warning(request,  'Hello world.')
        return super(MouseTest, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(MouseTest, self).get_context_data(**kwargs)
        
        filename = settings.MEDIA_ROOT+"/users/Human_Mouse.csv"
        
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(open(filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
        df = read_csv(filename, delimiter=dialect.delimiter)
        
        context['input'] = df[:50].to_html()
        """
        paths = Pathway.objects.all()
        
        for path in paths:
            mouse_path = MousePathway(name=path.name, amcf=path.amcf, info = path.info, comment = path.comment)
            mouse_path.save()
            
            for gene in path.gene_set.all():
                mapping_genes = MouseMapping.objects.filter(human_gene_symbol = gene.name)
                
                if not mapping_genes:
                    pass
                else:
                    for m_gene in mapping_genes:
                        mouse_gene = MouseGene(name=m_gene.mouse_gene_symbol.upper(), arr = gene.arr, comment = gene.comment, pathway=mouse_path)
                        mouse_gene.save()
        
        """
        
        
        
        
            
        
  
        
        context['summ'] = filename
        
        
        
        return context
    
    