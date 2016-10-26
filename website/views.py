# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import networkx as nx

from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.conf import settings

from core.models import Pathway, Node, Component


class IndexPage(TemplateView):
    template_name = 'website/index.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        #if request.user.is_authenticated():
        #    return redirect('profiles_index', slug=request.user.username)
        #else:
        return super(IndexPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(IndexPage, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context
    
class AboutPage(TemplateView):
    template_name = 'website/about.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('profiles_index', slug=request.user.username)
        else:
            return super(AboutPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(AboutPage, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context
    
class LoginPage(TemplateView):
    template_name = "website/login.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LoginPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(LoginPage, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context

class Logout(TemplateView):
    template_name="website/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)    
        return redirect('website_index')
    


    
    
        
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    