# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import MetabolismPathway

class MetabolismPathwayList(ListView):
    """
    List of Pathways in BioChem DB section
    """    
    model = MetabolismPathway
    template_name = 'metabolism/pathway_list.html'
    context_object_name = 'pathways'
    paginate_by = 20
        
    def get_context_data(self, **kwargs):
        context = super(MetabolismPathwayList, self).get_context_data(**kwargs)
        context['allPathways'] = MetabolismPathway.objects.count()        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MetabolismPathwayList, self).dispatch(request, *args, **kwargs)
      
    
class MetabolismPathwayDetail(DetailView):
    """
    Details page for particular pathway
    """
    model = MetabolismPathway
    template_name = 'metabolism/pathway_detail.html'
    context_object_name = 'pathway'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MetabolismPathwayDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MetabolismPathwayDetail, self).get_context_data(**kwargs)
        return context

class MetabolismPathwayAjaxSearch(ListView):
    """
    Renders objects for Ajax Search
    """
    model = MetabolismPathway
    template_name = 'metabolism/pathway_ajax_search.html'
    context_object_name = 'pathways'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return MetabolismPathway.objects.filter(name__icontains=q)
    
    