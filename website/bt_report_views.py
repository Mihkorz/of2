# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import networkx as nx
import itertools

from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from core.models import Pathway, Node, Component

class BTReport(TemplateView):
    template_name = "website/bt_report.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(BTReport, self).get_context_data(**kwargs)
        
        lGenes = ['COL1A1', 'COL1A2', 'KRT7', 'HYAL1', 'HYAL2', 'HYAL4', 'HAS1', 'HAS2',
               'ELN', 'MMP1', 'MMP13', 'MMP8', 'FN1', 'WNT1', 'EGF', 'EGFR', 'GH1', 'TGFB1',
               'TGFBR1', 'TGFBR2',
               'FGF1', 'FGFR1']
        
        context['lGenes'] = lGenes
        
        return context
    
    
class BTGeneVolcanoJson(TemplateView):
    template_name="website/bt_report.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTGeneVolcanoJson, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        file_name = request.POST.get('file_name')
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name, sep='\t')
        
        df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
        
        df_gene.rename(columns={'gene': 'Symbol'}, inplace=True)
        df_gene['_row'] = 'hahaha'
         
        df_gene = df_gene[(df_gene['adj.P.Val']<0.05) & (np.absolute(df_gene['logFC'])>1)] 
         
        df_gene['adj.P.Val'] = -1*np.log10(df_gene['adj.P.Val'])        
         
        #raise Exception('fuck')
        output_json = df_gene.to_json(orient='records')        
        
        response_data =json.loads(output_json)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    def get(self, request, *args, **kwargs):
        
        file_name = 'EPL_vs_ES.onc.tab11'
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/users/admin/bt/input/"+file_name, sep='\t')
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
        
        count_df.to_csv(settings.MEDIA_ROOT+"/users/admin/bt/input/box_"+file_name)
        
        raise Exception('stop') 

class BTReportGeneTableJson(TemplateView):
    template_name="website/bt_report.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTReportGeneTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name, sep='\t')
        
        df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
        
        df_gene = df_gene[(df_gene['adj.P.Val']<0.05) & (np.absolute(df_gene['logFC'])>1)] 
        
        output_json = df_gene.to_json(orient='values')

        #raise Exception('gene table')
        response_data = {'data': json.loads(output_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
class BTReportGeneBoxplotJson(TemplateView):
    template_name="website/report.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTReportGeneBoxplotJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene  = request.GET.get('gene')
        
        
        
        df_ES = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ES.onc.tab",
                                index_col='SYMBOL', )
        df_ASC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ASC.onc.tab",
                                index_col='SYMBOL', )
        df_ABC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ABC.onc.tab",
                                index_col='SYMBOL', )
        df_AEC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_AEC.onc.tab",
                                index_col='SYMBOL', )
        df_ANC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ANC.onc.tab",
                                index_col='SYMBOL', )
        df_CCL = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_CCL.onc.tab",
                                index_col='SYMBOL', )
        
        #raise Exception('boxplot')
        series_tumour = []
        series_norm = []
        i=0
        for df in [df_ES, df_ASC, df_ABC, df_AEC, df_ANC, df_CCL]:
            
            
                
            filered_df = df[[x for x in df if 'Tumour' in x]]
                
            row_gene = filered_df.loc[gene]      
        
            median = np.around(np.log2(row_gene['Tumour_median']), decimals=2)  
            upper_quartile = np.around(np.log2(row_gene['Tumour_upper_quartile']), decimals=2) 
            lower_quartile = np.around(np.log2(row_gene['Tumour_lower_quartile'] ), decimals=2)           
            upper_whisker = np.around(np.log2(row_gene['Tumour_upper_whisker']), decimals=2) 
            lower_whisker = np.around(np.log2(row_gene['Tumour_lower_whisker']), decimals=2) 
              
            lSerie = [lower_whisker, lower_quartile, median, upper_quartile, upper_whisker]
                 
            series_tumour.append(lSerie)
            
            if i==0:
                filered_df = df[[x for x in df if 'Norm' in x]]
                
                row_gene = filered_df.loc[gene]      
        
                median = np.around(np.log2(row_gene['Normal_median']), decimals=2) 
                upper_quartile = np.around(np.log2(row_gene['Normal_upper_quartile']), decimals=2) 
                lower_quartile = np.around(np.log2(row_gene['Normal_lower_quartile']), decimals=2)            
                upper_whisker = np.around(np.log2(row_gene['Normal_upper_whisker']), decimals=2) 
                lower_whisker = np.around(np.log2(row_gene['Normal_lower_whisker']), decimals=2)
              
                lSerie = [lower_whisker, lower_quartile, median, upper_quartile, upper_whisker]
                series_tumour.append(lSerie)
                
            
            i=i+1
        
        #raise Exception('boxplot') 
        s1 = {
              'name': 'boxplot',              
              'data': series_tumour,
              'tooltip': {
                          'headerFormat': '<em>Skin type: {point.key}</em><br/>'
                          }
              }
        
        
        
        response_data = s1
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")













