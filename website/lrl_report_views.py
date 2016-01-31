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

class LRLReport(TemplateView):
    template_name = "website/lrl_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(LRLReport, self).get_context_data(**kwargs)
        
        lEmbryonicGenes =[ 'PCDHB2', 'PCDHB17', 'CSTF3', 'LOC644919', 'ITGA11', 'SMA4',
                          'LOC727877', 'MAST2', 'TMEM18', 'LOC100130914', 'ADSSL1', 'ZNF767',
                          'C19orf25', 'C19orf6', 'NKTR', 'LOC286208', 'GOLGA8A', 'CDK5RAP3',
                          'OPN3', 'MGC16384', 'ZNF33A', 'LOC100190939', 'TPM1', 'GSDMB']
               
        lAdultGenes = ['COX7A1', 'ZNF280D', 'LOC441408', 'TRIM4', 'NIN', 'NAALADL1', 'ASF1B',
                       'COMT', 'CAT', 'C18orf56', 'LOC440731', 'HOXA5', 'LOC375295', 'POLQ',
                       'CAT', 'MEG3', 'CDT1', 'FOS']
        
        context['lEmbryonicGenes'] = lEmbryonicGenes
        
        context['lAdultGenes'] = lAdultGenes
        
        return context


class LRLReportGeneScatterJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportGeneScatterJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')        
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name,
                                sep='\t', index_col='SYMBOL')
        
        
        df_tumour = df_gene[[x for x in df_gene.columns if 'Tumour' in x]]
        s_tumour = df_tumour.mean(axis=1).round(decimals=2)
        
        df_norm = df_gene[[x for x in df_gene.columns if 'Norm' in x]]
        s_norm = df_norm.mean(axis=1).round(decimals=2)        
        
        df_output = pd.DataFrame()
        
        df_output['x'] = s_tumour
        df_output['y'] = s_norm
        
        df_fc = df_output.div(df_output.y, axis='index')
        df_fc = np.log2(df_fc)
        
        df_output = df_output[np.absolute(df_fc['x'])>1]
        
        df_output = np.log2(df_output)
        
        df_output.index.name='name'
        df_output.reset_index(inplace=True)
        
        df_output = df_output.to_json(orient='records')        
        
        response_data =  json.loads(df_output)
        return HttpResponse(json.dumps(response_data), content_type="application/json")    

class LRLReportGeneTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportGeneTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name,
                                sep='\t', index_col='SYMBOL')
        
        df_tumour = df_gene[[x for x in df_gene.columns if 'Tumour' in x]]
        s_tumour = df_tumour.mean(axis=1).round(decimals=2)
        
        df_norm = df_gene[[x for x in df_gene.columns if 'Norm' in x]]
        s_norm = df_norm.mean(axis=1).round(decimals=2)        
        
        df_output = pd.DataFrame()
        
        df_output['x'] = s_tumour
        df_output['y'] = s_norm
        
        df_output = df_output.div(df_output.y, axis='index')
        df_output = np.log2(df_output)
        
        df_output = df_output[np.absolute(df_output['x'])>1]
        
        
        df_output.index.name = 'Gene'
        df_output.reset_index(inplace=True)
        
        output_json = df_output.to_json(orient='values')
        
        response_data = {'data': json.loads(output_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
 
    
class LRLReportGeneDetailJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportGeneDetailJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene_name = request.GET.get('gene')
        file_name = request.GET.get('file_name')
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name,
                                sep='\t', index_col='SYMBOL')
        
        df_gene = np.log2(df_gene)
        
        df_output = pd.DataFrame()
        
        gene_row = df_gene.loc[gene_name].round(decimals=2)
        
        response_data = {}
        
        lNHE = []
        lCase = []
        for index, value in gene_row.iteritems():
            if 'Tumour' in index:
                index = index.replace('Tumour_', '').replace('.CEL', '')
                lNHE.append([index, 0])
                lCase.append([index, value])
            if 'Norm' in index:
                index = index.replace('Normal_', '').replace('.CEL', '')
                lNHE.append([index, value])
                lCase.append([index, 0])
             

        response_data['NHE'] = lNHE        
        response_data['Case'] = lCase
        
        #
        return HttpResponse(json.dumps(response_data), content_type="application/json")   


class LRLGeneVolcanoJson(TemplateView):
    template_name="website/bt_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLGeneVolcanoJson, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        file_name = request.POST.get('file_name')        
        
        df_input = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name, index_col='SYMBOL')
        
        df1_tumour = df_input[[x for x in df_input.columns if 'Tumour' in x]]
        s1_tumour = np.log2(df1_tumour.mean(axis=1)).round(decimals=2)
        
        df_gene = pd.DataFrame()
        
        df_gene['logFC'] = s1_tumour
        df_gene['adj.P.Val'] = df_input['q_value']
        
        df_gene.reset_index(inplace=True)
        #raise Exception('fuck')
        df_gene.rename(columns={'SYMBOL': 'Symbol'}, inplace=True)
        
        df_gene['logFC'] = df_gene['logFC'].round(decimals=2)
        
        df_gene['_row'] = df_gene['adj.P.Val'].round(decimals=2)
         
        df_gene = df_gene[(df_gene['adj.P.Val']<0.05) & (np.absolute(df_gene['logFC'])>0)] 
         
        df_gene['adj.P.Val'] = -1*np.log10(df_gene['adj.P.Val'])        
         
        
        output_json = df_gene.to_json(orient='records')        
        
        response_data =json.loads(output_json)
        return HttpResponse(json.dumps(response_data), content_type="application/json")    
    
    
    
    
    
    
    
    