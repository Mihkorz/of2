# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import networkx as nx

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.conf import settings

from .models import Report

class ReportList(ListView):
    model = Report
    template_name = 'report/report_list.html'
    context_object_name = 'reports'
    paginate_by = 100
    
    
    def dispatch(self, request, *args, **kwargs):
        return super(ReportList, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(ReportList, self).get_context_data(**kwargs)
        
        
        context['test'] = "Test"
        
        return context

class ReportDetail(DetailView):
    model = Report
    template_name = 'report/report_detail.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super(ReportDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(ReportDetail, self).get_context_data(**kwargs)
        
        
        context['test'] = "Test"
        
        return context

class ReportGeneVolcanoJson(TemplateView):
    template_name="website/bt_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneVolcanoJson, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        file_name = request.POST.get('file_name')
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/"+file_name, sep='\t')
        try:
            df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
            df_gene.rename(columns={'gene': 'Symbol'}, inplace=True)
        except:
            df_gene = df_gene[['SYMBOL', 'logFC', 'adj.P.Val']]
            df_gene.rename(columns={'SYMBOL': 'Symbol'}, inplace=True)
            
        df_gene['logFC'] = df_gene['logFC'].round(decimals=2)
        
        df_gene['_row'] = df_gene['adj.P.Val'].round(decimals=2)
         
        df_gene = df_gene[(df_gene['adj.P.Val']<0.05) & (np.absolute(df_gene['logFC'])>0.4)] 
         
        df_gene['adj.P.Val'] = -1*np.log10(df_gene['adj.P.Val'])        
         
        #raise Exception('fuck')
        output_json = df_gene.to_json(orient='records')        
        
        response_data =json.loads(output_json)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    def get(self, request, *args, **kwargs):
        
        file_name = 'EPL_vs_ES.txt'
        file_out = 'box_EPL_vs_ES.onc.tab'
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/users/admin/bt-new/input/"+file_name, sep='\t')
        df_gene.set_index('SYMBOL', inplace=True)
        
        
        def boxplot(row):
            print row.name
            sss = pd.Series()
            
            r_norm = row.filter(like='Normal_')
            r_tumour = row.filter(like='Tumour')       
                
            median = np.around(np.median(r_norm), decimals=0) 
            upper_quartile = np.around(np.percentile(r_norm, 75), decimals=0)
            lower_quartile = np.around(np.percentile(r_norm, 25), decimals=0)
            iqr = upper_quartile - lower_quartile
            upper_whisker = np.around(r_norm[r_norm<=upper_quartile+1.5*iqr], decimals=0).max()
            lower_whisker = np.around(r_norm[r_norm>=lower_quartile-1.5*iqr], decimals=0).min()
                
            sss['Normal_median'] = median
            sss['Normal_upper_quartile'] = upper_quartile
            sss['Normal_lower_quartile'] = lower_quartile
            sss['Normal_upper_whisker'] = upper_whisker
            sss['Normal_lower_whisker'] = lower_whisker
            
            median = np.around(np.median(r_tumour), decimals=0) 
            upper_quartile = np.around(np.percentile(r_tumour, 75), decimals=0)
            lower_quartile = np.around(np.percentile(r_tumour, 25), decimals=0)
            iqr = upper_quartile - lower_quartile
            upper_whisker = np.around(r_tumour[r_tumour<=upper_quartile+1.5*iqr], decimals=0).max()
            lower_whisker = np.around(r_tumour[r_tumour>=lower_quartile-1.5*iqr], decimals=0).min()
                
            sss['Tumour_median'] = median
            sss['Tumour_upper_quartile'] = upper_quartile
            sss['Tumour_lower_quartile'] = lower_quartile
            sss['Tumour_upper_whisker'] = upper_whisker
            sss['Tumour_lower_whisker'] = lower_whisker
            
            sss.name = row.name
            return sss
        
        count_df = df_gene.apply(boxplot ,axis=1)
        
        count_df.to_csv(settings.MEDIA_ROOT+"/users/admin/bt-new/input/box_"+file_name)
        
        raise Exception('stop') 
    
class ReportGeneTableJson(TemplateView):
    template_name="report/report_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        
        if file_name!='all':
            
            
            df_gene = pd.read_csv(settings.MEDIA_ROOT+"/"+file_name, sep='\t')
            try:
                df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
            except:
                df_gene = df_gene[['SYMBOL', 'logFC', 'adj.P.Val']]
                
            df_gene['logFC'] = df_gene['logFC'].round(decimals=2)         
        
            df_gene = df_gene[(df_gene['adj.P.Val']<0.05) & (np.absolute(df_gene['logFC'])>0.4)] 
        
            
        
        else:
            df_ES = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_ES.DE.tab",
                                 sep='\t', index_col='gene')            
            df_ASC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_ASC.DE.tab",
                                 sep='\t', index_col='gene')
            df_ABC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_ABC.DE.tab",
                                 sep='\t', index_col='gene')
            df_AEC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_AEC.DE.tab",
                                 sep='\t', index_col='gene')
            df_ANC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_ANC.DE.tab",
                                 sep='\t', index_col='gene')
            df_CCL = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_CCL.DE.tab",
                                 sep='\t', index_col='gene')
            
            df_gene = pd.DataFrame()
            df_gene['1'] = df_ES['logFC'].round(decimals=2)
            df_gene['2'] = df_ASC['logFC'].round(decimals=2)
            df_gene['3'] = df_ABC['logFC'].round(decimals=2)
            df_gene['4'] = df_AEC['logFC'].round(decimals=2)
            df_gene['5'] = df_ANC['logFC'].round(decimals=2)
            df_gene['6'] = df_CCL['logFC'].round(decimals=2)
            
            
            
            df_gene.reset_index(inplace=True)
            #raise Exception('gene table')

        output_json = df_gene.to_json(orient='values')
        response_data = {'data': json.loads(output_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    
    
    
    