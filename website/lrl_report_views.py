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
        
        dSamples={'Retinoic acid': {'id': 'ra',
                                    'data': [['ra_24_01', '24h 0.1 micromol'],
                                    ['ra_24_1', '24h 1 micromol'],
                                    ['ra_48_01', '48h 0.1 micromol'],
                                    ['ra_48_1', '48h 1 micromol']]
                                    },
                  'Metformin hydrochloride': {'id': 'mh',
                                              'data': [['mh_24_2', '24h 2 micromol'],
                                                      ['mh_24_2', '24h 2 micromol'],
                                                      ['mh_24_2', '24h 2 micromol'],
                                                      ['mh_24_2', '24h 2 micromol']]
                                              },
                  'Capryloylsalicylic acid': {'id': 'ca',
                                              'data': [['ca_24_5', '24h 5 micromol'],
                                                      ['ca_24_10', '24h 10 micromol'],
                                                      ['ca_48_5', '48h 5 micromol'],
                                                      ['ca_48_10', '48h 10 micromol']]
                                              },
                  'Resveratrol': {'id': 're',
                                              'data': [['re_24_10', '24h 10 nmol'],
                                                      ['re_24_50', '24h 50 micromol'],
                                                      ['re_48_10', '24h 10 nmol'],
                                                      ['re_48_50', '48h 50 micromol']]
                                              }
                   }
        
        context['dSamples'] = dSamples
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
    

class LRLReportPathwayTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportPathwayTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')

        
        if file_name == 'all':
            dfnhk = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/output_loreal_preprocessed_NHK.txt.xlsx",
                                sheetname='PAS1', index_col='Pathway')
            df1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/output_loreal_preprocessed_RhE (Type 1).txt.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
            df2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/output_loreal_preprocessed_RhE (Type 2).txt.xlsx",
                                sheetname='PAS1', index_col='Pathway')
            df3 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/output_loreal_preprocessed_RhE (Type 3).txt.xlsx",
                                 sheetname='PAS1', index_col='Pathway')

                
            dfnhk_tumour = dfnhk[[x for x in dfnhk.columns if 'Tumour' in x]]
            snkh_tumour = dfnhk_tumour.mean(axis=1).round(decimals=2)
            df1_tumour = df1[[x for x in df1.columns if 'Tumour' in x]]
            s1_tumour = df1_tumour.mean(axis=1).round(decimals=2)
            df2_tumour = df2[[x for x in df2.columns if 'Tumour' in x]]
            s2_tumour = df2_tumour.mean(axis=1).round(decimals=2)
            df3_tumour = df3[[x for x in df3.columns if 'Tumour' in x]]
            s3_tumour = df3_tumour.mean(axis=1).round(decimals=2)
            
            df_output = pd.DataFrame()
            df_output['1'] = snkh_tumour
            df_output['2'] = s1_tumour
            df_output['3'] = s2_tumour
            df_output['4'] = s3_tumour
            try:
                df_output.drop(['Target_drugs_pathway'], inplace=True)
            except:
                pass
            df_output.reset_index(inplace=True)
            
            
        else:
            
            df = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name,
                                sheetname='PAS1', index_col='Pathway')
            
            t_name = [x for x in df.columns if 'Tumour' in x][0]
            
            df = df[df[t_name]!=0]
            
            df[t_name] = df[t_name].round(decimals=2)
            
            df = df.drop('Database', 1)
            
            
            try:
                df.drop(['Target_drugs_pathway'], inplace=True)
            except:
                pass
            df.reset_index(inplace=True)
        
        
        
        df_json = df.to_json(orient='values')
        
        
        
        response_data = {'aaData': json.loads(df_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    
    
        
    
    
    
    
    
    