# -*- coding: utf-8 -*-
import json
import time
import numpy as np
import pandas as pd


from celery.result import AsyncResult
from celery import group, chord
from .tasks import add, countArr
        

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Pathway            

class Celery(TemplateView):
    """
    Testing Celery tasks
    """
    template_name = 'core/celery.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Celery, self).dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super(Celery, self).get_context_data(**kwargs)
        df = pd.DataFrame(np.random.randn(10, 5),
                       columns=['a', 'b', 'c', 'd', 'e'])
        
        
        
        
        start = time.time()
        pathways = Pathway.objects.filter(organism='human', database='primary_old')
        sss = pd.Series()
        
        
        #res = chord()()
        #for i in range(5):
        res = add.delay(5,6)
        result = res.get()    
        
       
            
        stop = time.time() - start
        raise Exception('celery')
        
        #
        #context ['result'] = a.get()   
        
        
        return context
    
        
class TaskStatus(TemplateView):
    """ Testing Celery task status via Ajax"""
    
    template_name = 'core/test.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        if self.request.is_ajax():
            
            
            task_id = self.request.POST.get('task_id')
            task = AsyncResult(task_id)
            state = task.state
            result = task.result if task.result else 'not done'
            
            data = {'state': state,
                    'result': result}
            
            
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
        
            return super(TaskStatus, self).dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
              
        context = super(TaskStatus, self).get_context_data(**kwargs)
        
        return context