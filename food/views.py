
import json
import pandas as pd

from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.db.models import Q

from .models import Mainfooddesc

class FoodIndex(TemplateView):
    
    template_name = 'food/index.html'
    
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  
        
        return super(FoodIndex, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(FoodIndex, self).get_context_data(**kwargs)
        
        
        
        #raise Exception('fuck')
        
        context['test'] = "Test"
        
        return context

class FoodSearch(TemplateView): 
    template_name="report/report_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(FoodSearch, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        search_text = request.GET.get('search_text')
        food_groups = json.loads(request.GET.get('food_groups'))
        
        try:
            best_search = Mainfooddesc.objects.using('food').get(main_food_description=search_text+', NFS')
        except:
            try:
                best_search = Mainfooddesc.objects.using('food').get(main_food_description=search_text+', raw')
            except:
                best_search = 'Nothing found'
            
        primary_search = Mainfooddesc.objects.using('food').filter(main_food_description__istartswith=search_text)
        secondary_search = Mainfooddesc.objects.using('food').filter(main_food_description__icontains=search_text)
        
        pr_query = Q()
        sec_query = Q()
        
        for group in food_groups:
            
            pr_query = pr_query | Q(food_code__startswith=int(group))
            sec_query = sec_query | Q(food_code__startswith=int(group))
        
        primary_search = primary_search.filter(pr_query)
        secondary_search = secondary_search.filter(sec_query)
        
        blocked_id = primary_search.values('food_code')
        secondary_search = secondary_search.exclude(food_code__in=blocked_id)        
            
        
        lprim = primary_search.values_list('main_food_description', flat=True)
        lsec = secondary_search.values_list('main_food_description', flat=True)
        
        if not lprim:
            lprim_reponse = ['Nothing Found']
        else:
            lprim_reponse = [x.encode('UTF8') for x in lprim]
        if not lsec:
            lsec_reponse = ['Nothing Found']
        else:
            lsec_reponse = [x.encode('UTF8') for x in lsec]
        
         
        response_data = {
                         'best_search': best_search.main_food_description,
                         'primary_search': lprim_reponse,
                         'secondary_search': lsec_reponse
                         }
        #raise Exception('food')      
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    
    
    
    
    
    
    
    