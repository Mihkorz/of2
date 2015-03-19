# -*- coding: utf-8 -*-

import os
import time
import pandas.rpy.common as com
import csv
import numpy as np
from pandas import DataFrame, read_csv
from rpy2.robjects.packages import importr
from collections import defaultdict

from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.conf import settings

from .forms import XpnParametersForm


class XpnForm(FormView):
    
    form_class = XpnParametersForm
    success_url = '/thanks/'
    
    template_name = 'core/xpnform.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(XpnForm, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):        
        context = super(XpnForm, self).get_context_data(**kwargs)
        
        context['test'] = 'test'
        return context
    
    def rename_df_columns(self, df):
        
        name_counts = defaultdict(int)
        new_col_names = []
            
        for name in df.columns:
            new_count = name_counts[name] + 1
            new_col_names.append("{}.{}".format(name, new_count))
            name_counts[name] = new_count 
                
            
        df.columns = new_col_names
        return df
    
    def form_valid(self, form):
        
        pl1 = form.cleaned_data.get('pl1', False)
        pl2 = form.cleaned_data.get('pl2', False)
        k = form.cleaned_data.get('k', 10)
        l = form.cleaned_data.get('l', 4)
        log_scale = form.cleaned_data.get('log_scale', True)
        p1_names = form.cleaned_data.get('p1_names', 0)
        p2_names = form.cleaned_data.get('p2_names', 0)
        gene_cluster = form.cleaned_data.get('gene_cluster', 'kmeans')
        assay_cluster = form.cleaned_data.get('assay_cluster', 'kmeans')
        corr = form.cleaned_data.get('corr', 'pearson')
        iterations = form.cleaned_data.get('iterations', 30)
        skip_match = form.cleaned_data.get('skip_match', False) 
        
        sniffer = csv.Sniffer()
        dialect_pl1 = sniffer.sniff(pl1.read(), delimiters='\t,; ') # defining the separator of the csv file
        pl1.seek(0)
        df_pl1 = read_csv(pl1, delimiter=dialect_pl1.delimiter, index_col=0)
                
        dialect_pl2 = sniffer.sniff(pl2.read(), delimiters='\t,; ') # defining the separator of the csv file
        pl2.seek(0)
        df_pl2 = read_csv(pl2, delimiter=dialect_pl2.delimiter, index_col=0)
        
        if log_scale:
            df_pl1 = np.log(df_pl1).fillna(0)
            df_pl2 = np.log(df_pl2).fillna(0)
        
        len_col_pl1 = len(df_pl1.columns)
        len_col_pl2 = len(df_pl2.columns)
        
        if abs(np.log2(len_col_pl1/len_col_pl2))>2:
            raise forms.ValidationError(u"Error! Datasets can't be compared.\
                                          Number of samples in one dataset is at least 4 \
                                          times larger than in the other.")
        
        diff = abs(len_col_pl1-len_col_pl2)
        
        np.random.seed(5) #fix random number generator for the sake of reproducibility
        
        if len_col_pl1>len_col_pl2:
            if abs(np.log2(len_col_pl1/len_col_pl2)<1):
                choice = np.random.choice(len_col_pl2, diff, replace=False) #create random sample from df columns
            else:
                choice = np.random.choice(len_col_pl2, diff, replace=True)               
            
            adjusted_df = df_pl2[choice]
            adjusted_df = self.rename_df_columns(adjusted_df)       
            df_pl2 = df_pl2.join(adjusted_df)   
            
        else:
            if abs(np.log2(len_col_pl1/len_col_pl2)<1):
                choice = np.random.choice(len_col_pl1, diff, replace=False)
            else:
                choice = np.random.choice(len_col_pl1, diff, replace=True)
            adjusted_df = df_pl2[choice]            
            adjusted_df = self.rename_df_columns(adjusted_df)            
            df_pl1 = df_pl1.join(adjusted_df)
        
        Rdf_pl1 = com.convert_to_r_dataframe(df_pl1)
        Rdf_pl2 = com.convert_to_r_dataframe(df_pl2)
        try:
            conor = importr("CONOR")
            R_output = conor.xpn(Rdf_pl1, Rdf_pl2, p1_names=p1_names, p2_names=p2_names,
                                 iterations=iterations, K=k, L=l )
        except:
            raise
        py_output = com.convert_robj(R_output)

        df_out_x = DataFrame(py_output['x'])
        df_out_y = DataFrame(py_output['y'])        
        df_out_x.index.name = df_out_y.index.name = 'SYMBOL'
        
        df_output_all = df_out_x.join(df_out_y, lsuffix='_x', rsuffix='_y')
        filename = pl1.name+pl2.name+".csv"
        output_file = settings.MEDIA_ROOT+"/XPN/"+filename
        
        df_output_all.to_csv(output_file) 
        
        return HttpResponseRedirect(reverse('xpn_done', args=[filename]))
        
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        
        
class XpnDone(TemplateView):
    template_name = 'core/xpndone.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(XpnDone, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):        
        context = super(XpnDone, self).get_context_data(**kwargs)
        output_file = self.args[0]
        context['output_file'] = output_file
        return context
    
class PrevFile:
    pass

class XpnPrevFiles(TemplateView):
    template_name = 'core/xpnprevfiles.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(XpnPrevFiles, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
                
        context = super(XpnPrevFiles, self).get_context_data(**kwargs)
        path = settings.MEDIA_ROOT+"/XPN/"
        dirs = os.listdir(path)
        lFiles = []
        for files in dirs:
            f = PrevFile()
            stat = os.stat(settings.MEDIA_ROOT+"/XPN/"+files)
            f.name = files
            f.created = time.ctime(stat.st_ctime)
            f.size = stat.st_size/1048576
            lFiles.append(f)
            
        lFiles.sort(key=lambda x: x.created, reverse=True)
        context['filelist'] = lFiles       
        
        
        
        return context 
    
    
    
    
    