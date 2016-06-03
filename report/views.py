# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import csv

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Report, GeneGroup, PathwayGroup
from core.models import Pathway, Node, Component

class ReportList(ListView):
    model = Report
    template_name = 'report/report_list.html'
    context_object_name = 'reports'
    paginate_by = 100
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportList, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(ReportList, self).get_context_data(**kwargs)
        
        
        context['test'] = "Test"
        
        return context

class ReportDetail(DetailView):
    model = Report
    template_name = 'report/report_detail.html'
    
    @method_decorator(login_required)
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
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/"+file_name)
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
                
    
class ReportGeneTableJson(TemplateView): 
    template_name="report/report_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        
        if file_name!='all':
            
            
            df_gene = pd.read_csv(settings.MEDIA_ROOT+"/"+file_name)
            try:
                df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
            except:
                df_gene = df_gene[['SYMBOL', 'logFC', 'adj.P.Val']]
                
            df_gene['logFC'] = df_gene['logFC'].round(decimals=2)         
        
            df_gene = df_gene[(df_gene['adj.P.Val']<0.05) & (np.absolute(df_gene['logFC'])>0.4)] 
        
            
        
        else:
            report = Report.objects.get(pk=request.GET.get('reportID'))
            lgroups = []
            for group in report.genegroup_set.all():
                lgroups.append(pd.read_csv(group.doc_logfc.path, index_col='SYMBOL'))
            
            df_gene = pd.DataFrame()
            
            for idx, val in enumerate(lgroups):
                df_gene[idx] = val['logFC'].round(decimals=2)

            df_gene.reset_index(inplace=True)
            #raise Exception('gene table')

        output_json = df_gene.to_json(orient='values')
        response_data = {'data': json.loads(output_json)}
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class ReportGeneScatterJson(TemplateView):
    template_name="report/report_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneScatterJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = settings.MEDIA_ROOT+'/'+request.GET.get('file_name')
        
        with open(file_name, 'rb') as csvfile:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(csvfile.read(), delimiters='\t,;')
            csvfile.seek(0)
            
        df_gene = pd.read_csv(file_name, delimiter=dialect.delimiter,
                                 index_col='SYMBOL')
        
        
        df_tumour = df_gene[[x for x in df_gene.columns if 'Tumour' in x]]
        s_tumour = df_tumour.mean(axis=1).round(decimals=2)
        
        df_norm = df_gene[[x for x in df_gene.columns if 'Norm' in x]]
        s_norm = df_norm.mean(axis=1).round(decimals=2)        
        
        df_output = pd.DataFrame()
        
        df_output['x'] = s_tumour
        df_output['y'] = s_norm
        
        df_output['FC'] = s_tumour.divide(s_norm)
        
        df_output = np.log2(df_output)
        
        df_output = df_output[np.absolute(df_output['FC'])>2]
        
        
        
        df_output = df_output[df_output['x']>0 ]
        df_output = df_output[df_output['y']>0 ]
        #raise Exception('scatter')
        df_output.index.name='name'
        df_output.reset_index(inplace=True)
        
        df_output = df_output.to_json(orient='records')        
        
        
        response_data =  json.loads(df_output)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        
class ReportGeneTableScatterJson(TemplateView): 
    template_name="report/report_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneTableScatterJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        
        if file_name!='all':
            
            
            
            
            df_gene = pd.read_csv(settings.MEDIA_ROOT+"/"+file_name)
            try:
                df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
            except:
                df_gene = df_gene[['SYMBOL', 'logFC', 'adj.P.Val']]
                
            df_gene['logFC'] = df_gene['logFC'].round(decimals=2)
                     
            df_gene.replace([np.inf, -np.inf], np.nan, inplace=True)
            df_gene = df_gene[(np.absolute(df_gene['logFC'])>2)] 
            #raise Exception('scatter table')
            
        
        else:
            report = Report.objects.get(pk=request.GET.get('reportID'))
            lgroups = []
            for group in report.genegroup_set.all():
                lgroups.append(pd.read_csv(group.doc_logfc.path, index_col='SYMBOL'))
            
            df_gene = pd.DataFrame()
            
            for idx, val in enumerate(lgroups):
                df_gene[idx] = val['logFC'].round(decimals=2)

            df_gene.reset_index(inplace=True)
            #raise Exception('gene table')

        output_json = df_gene.to_json(orient='values')
        response_data = {'data': json.loads(output_json)}
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")        
    
    
        
class ReportGeneBoxplotJson(TemplateView):
    
    template_name="report/report_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneBoxplotJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene  = request.GET.get('gene')        
        report = Report.objects.get(pk=request.GET.get('reportID'))
        
        df_list = []
        
        for group in report.genegroup_set.all():
            
            df_group = pd.read_csv(group.doc_boxplot.path,
                                   index_col='SYMBOL')
            df_list.append(df_group)
        
        series_tumour = []
        series_norm = []
        i=0
        for df in df_list:          
                
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
                          'headerFormat': '<em>Group: {point.key}</em><br/>'
                          }
              }        
        
        response_data = s1
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")  
    
class ReportPathwayTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportPathwayTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name1 = request.GET.get('file_name1')
        file_name2 = request.GET.get('file_name2')
        is_metabolic = request.GET.get('is_metabolic')
        
        report = Report.objects.get(pk=request.GET.get('reportID'))
        
        if is_metabolic =='false':
            is_metabolic = False
        else:
            is_metabolic = True
        
        if file_name1 == file_name2 == 'all':
            
            lgroups = []
            for group in report.pathwaygroup_set.all():
                df_path = pd.read_csv(group.doc_proc.path, index_col='Pathway')
                if is_metabolic:
                    df_path = df_path[df_path['Database']=='metabolism']
                else:
                    df_path = df_path[df_path['Database']!='metabolism']
                lgroups.append(df_path)
            
            df_output = pd.DataFrame()
            
            for idx, val in enumerate(lgroups):
                df_output[idx] = val['0'].round(decimals=2)
            
            try:
                df_output.drop(['Target_drugs_pathway'], inplace=True)
            except:
                pass
            df_output.reset_index(inplace=True)
            
            
        else:
            df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+file_name1,
                                sheetname='PAS1', index_col='Pathway')
            df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+file_name2,
                                 sheetname='PAS1', index_col='Pathway')
        
            
            if is_metabolic:
                df_1 = df_1[df_1['Database']=='metabolism']
                df_2 = df_2[df_2['Database']=='metabolism']
            else:
                df_1 = df_1[df_1['Database']!='metabolism']
                df_2 = df_2[df_2['Database']!='metabolism']
            
            df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
            s1_tumour = df1_tumour.mean(axis=1).round(decimals=2)
        
            df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
            s2_tumour = df2_tumour.mean(axis=1).round(decimals=2)               
        
            df_output = pd.DataFrame()
        
            df_output['1'] = s1_tumour
            df_output['2'] = s2_tumour
            try:
                df_output.drop(['Target_drugs_pathway'], inplace=True)
            except:
                pass
            df_output.reset_index(inplace=True)
        
        
        
        df_json = df_output.to_json(orient='values')
        
        
        
        response_data = {'aaData': json.loads(df_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
class ReportAjaxPathwayVenn(TemplateView):
    template_name="website/report_ajax_venn.html"
    def dispatch(self, request, *args, **kwargs):
        return super(ReportAjaxPathwayVenn, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
          
        report = Report.objects.get(pk=request.GET.get('reportID'))
        group_names = self.request.GET.get('group_names')
        is_metabolic = self.request.GET.get('is_metabolic')
        regulation = self.request.GET.get('regulation')
        path_gene = self.request.GET.get('path_gene')
        
        lgroup = group_names.split('vs')
        
        name1 = lgroup[0]
        name2 = lgroup[1]
        name3 = lgroup[2]
        #raise Exception('VENN!!!!')
        
        venn_cyrcles = []
        
        
        if path_gene == 'pathways':
            
            group1 = PathwayGroup.objects.get(name=lgroup[0], report=report)
            file_name1 = group1.doc_proc
            
            group2 = PathwayGroup.objects.get(name=lgroup[1], report=report)
            file_name2 = group2.doc_proc
            
            group3 = PathwayGroup.objects.get(name=lgroup[2], report=report)
            file_name3 = group3.doc_proc
            
            df1 = pd.read_csv(file_name1, index_col='Pathway')
            df2 = pd.read_csv(file_name2, index_col='Pathway')
            df3 = pd.read_csv(file_name3, index_col='Pathway')
                                    
            
            #raise Exception('VENN!!!!')           
            
            if is_metabolic=='true':
                df1 = df1[df1['Database']=='metabolism']
                df2 = df2[df2['Database']=='metabolism']
                df3 = df3[df3['Database']=='metabolism']
            else:
                df1 = df1[df1['Database']!='metabolism']
                df2 = df2[df2['Database']!='metabolism']
                df3 = df3[df3['Database']!='metabolism']
                
        elif path_gene == 'genes':
            
            group1 = GeneGroup.objects.get(name=lgroup[0], report=report)
            file_name1 = group1.doc_logfc.path
            
            group2 = GeneGroup.objects.get(name=lgroup[1], report=report)
            file_name2 = group2.doc_logfc.path
            
            group3 = GeneGroup.objects.get(name=lgroup[2], report=report)
            file_name3 = group3.doc_logfc.path
            
            df1 = pd.read_csv(file_name1, index_col='SYMBOL')
            if df1['adj.P.Val'].all() == 1:
                df1 = df1[(np.absolute(df1['logFC'])>2)]                
            else:
                df1 = df1[(df1['adj.P.Val']<0.05) & (np.absolute(df1['logFC'])>0.4)]         
            
            df2 = pd.read_csv(file_name2, index_col='SYMBOL')
            if df2['adj.P.Val'].all() == 1:
                df2 = df2[(np.absolute(df2['logFC'])>2)]
            else:
                df2 = df2[(df2['adj.P.Val']<0.05) & (np.absolute(df2['logFC'])>0.4)] 
            df3 = pd.read_csv(file_name3, index_col='SYMBOL')
            if df1['adj.P.Val'].all() == 1:
                df3 = df3[(np.absolute(df3['logFC'])>2)]
            else:
                df3 = df3[(df3['adj.P.Val']<0.05) & (np.absolute(df3['logFC'])>0.4)] 
            
            df1 = pd.DataFrame(df1['logFC']) 
            df2 = pd.DataFrame(df2['logFC'])
            df3 = pd.DataFrame(df3['logFC'])
            df1.columns = ['0']
            df2.columns = ['0']
            df3.columns = ['0']
            
            
        
        dict_s = {}
        list_s = [name1, name2, name3]
            
        st1_tumour = df1['0']
        st1_tumour_up = st1_tumour[st1_tumour>0]
        st1_tumour_down = st1_tumour[st1_tumour<0]
        if regulation == 'updown':
            venn_cyrcles.append({'sets': [name1], 'size': (st1_tumour_up.count()+st1_tumour_down.count()),
                                     'id': '1+updown+'+name1+'+'+is_metabolic})
        elif regulation == 'up':
            venn_cyrcles.append({'sets': [name1], 'size': (st1_tumour_up.count()),
                                     'id': '1+up+'+name1+'+'+is_metabolic})
        elif regulation == 'down':
            venn_cyrcles.append({'sets': [name1], 'size': (st1_tumour_down.count()),
                                     'id': '1+down+'+name1+'+'+is_metabolic})
        dict_s[name1] = st1_tumour
        dict_s[name1+' up'] = st1_tumour_up.index
        dict_s[name1+' down'] = st1_tumour_down.index        
          
           
        st2_tumour = df2['0']
        st2_tumour_up = st2_tumour[st2_tumour>0]
        st2_tumour_down = st2_tumour[st2_tumour<0]
        if regulation == 'updown':
            venn_cyrcles.append({'sets': [name2], 'size': (st2_tumour_up.count()+st2_tumour_down.count()),
                                     'id': '1+updown+'+name2+'+'+is_metabolic})
        elif regulation == 'up':
            venn_cyrcles.append({'sets': [name2], 'size': (st2_tumour_up.count()),
                                     'id': '1+up+'+name2+'+'+is_metabolic})
        elif regulation == 'down':
            venn_cyrcles.append({'sets': [name2], 'size': (st2_tumour_down.count()),
                                     'id': '1+down+'+name2+'+'+is_metabolic})    
        dict_s[name2] = st2_tumour
        dict_s[name2+' up'] = st2_tumour_up.index
        dict_s[name2+' down'] = st2_tumour_down.index
          
        st3_tumour = df3['0']
        st3_tumour_up = st3_tumour[st3_tumour>0]
        st3_tumour_down = st3_tumour[st3_tumour<0]
        if regulation == 'updown':
                venn_cyrcles.append({'sets': [name3], 'size': (st3_tumour_up.count()+st3_tumour_down.count()),
                                     'id': '1+updown+'+name3+'+'+is_metabolic})
        elif regulation == 'up':
                venn_cyrcles.append({'sets': [name3], 'size': (st3_tumour_up.count()),
                                     'id': '1+up+'+name3+'+'+is_metabolic})
        elif regulation == 'down':
                venn_cyrcles.append({'sets': [name3], 'size': (st3_tumour_down.count()),
                                     'id': '1+down+'+name3+'+'+is_metabolic})
        dict_s[name3] = st3_tumour
        dict_s[name3+' up'] = st3_tumour_up.index
        dict_s[name3+' down'] = st3_tumour_down.index
        
        
         
            
        combinations_2= list(itertools.combinations(list_s, 2)) # get all pairs of items
        for idx, combination in enumerate(combinations_2):
                
            index1_up = dict_s[combination[0]+' up']
            index1_down = dict_s[combination[0]+' down']
            index2_up = dict_s[combination[1]+' up']                
            index2_down = dict_s[combination[1]+' down']
            if regulation == 'updown':
                intersection = len(index1_up.intersection(index2_up))+len(index1_down.intersection(index2_down))
                id_x = '2+updown+'+combination[0]+'vs'+ combination[1]+'+'+is_metabolic
            elif regulation == 'up':
                intersection = len(index1_up.intersection(index2_up))
                id_x = '2+up+'+combination[0]+'vs'+ combination[1]+'+'+is_metabolic
            elif regulation == 'down':
                intersection = len(index1_down.intersection(index2_down))
                id_x = '2+down+'+combination[0]+'vs'+ combination[1]+'+'+is_metabolic
            venn_cyrcles.append({'sets': [combination[0], combination[1]],
                                     'size': intersection,
                                     'id': id_x })
             
        combinations_3= list(itertools.combinations(list_s, 3)) # get all triplets of items
        for idx, combination in enumerate(combinations_3):
                
            index1_up = dict_s[combination[0]+' up']
            index1_down = dict_s[combination[0]+' down']
            index2_up = dict_s[combination[1]+' up']                
            index2_down = dict_s[combination[1]+' down']
            index3_up = dict_s[combination[2]+' up']                
            index3_down = dict_s[combination[2]+' down']
                
            inter_up = (index1_up.intersection(index2_up)).intersection(index3_up)
            inter_down = (index1_down.intersection(index2_down)).intersection(index3_down)
            if regulation == 'updown':
                intersection = len(inter_up)+len(inter_down)
                id_x = '3+updown+'+combination[0]+'vs'+combination[1]+'vs'+combination[2]+'+'+is_metabolic
            elif regulation == 'up':
                intersection = len(inter_up)
                id_x = '3+up+'+combination[0]+'vs'+combination[1]+'vs'+combination[2]+'+'+is_metabolic
            elif regulation == 'down':
                intersection = len(inter_down)
                id_x = '3+down+'+combination[0]+'vs'+combination[1]+'vs'+combination[2]+'+'+is_metabolic
            venn_cyrcles.append({'sets': [combination[0], combination[1], combination[2]],
                                     'size': intersection,
                                     'id': id_x})
 
            #raise Exception('venn all')

        response_data= venn_cyrcles

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
class ReportAjaxPathwayVennTable(TemplateView):
    template_name="website/report_ajax_venn.html"
    def dispatch(self, request, *args, **kwargs):
        return super(ReportAjaxPathwayVennTable, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        inter_num = int(self.request.GET.get('inter_num'))
        regulation = self.request.GET.get('regulation')
        members = self.request.GET.get('members')
        is_metabolic = self.request.GET.get('is_metabolic')
        path_gene = self.request.GET.get('path_gene')
        
        lMembers = members.split('vs')
        
        report = Report.objects.get(pk=self.request.GET.get('reportID'))
        
        
        if inter_num == 1:
            if path_gene == 'pathways':
                
                group1 = PathwayGroup.objects.get(name=lMembers[0], report=report)
                df_1 = pd.read_csv(group1.doc_proc.path, index_col='Pathway')
                                        
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                
            elif path_gene =='genes':
                
                group1 = GeneGroup.objects.get(name=lMembers[0], report=report)
                
                df_1 = pd.read_csv(group1.doc_logfc.path,  index_col='SYMBOL')
                if df_1['adj.P.Val'].all() == 1:
                    df_1 = df_1[(np.absolute(df_1['logFC'])>2)]
                else:            
                    df_1 = df_1[(df_1['adj.P.Val']<0.05) & (np.absolute(df_1['logFC'])>0.4)]
                df_1 = pd.DataFrame(df_1['logFC'])
                df_1.columns = ['0']
                
            s_tumour = df_1['0'].round(decimals=2)
            s_tumour.name = lMembers[0]
            if regulation == 'updown':
                s_tumour = s_tumour[s_tumour!=0]
            elif regulation == 'up':            
                s_tumour = s_tumour[s_tumour>0]
            elif regulation == 'down':  
                s_tumour = s_tumour[s_tumour<0]
            
            df_1_tumour = pd.DataFrame(s_tumour)
            df_1_tumour.reset_index(inplace=True)
            df_json = df_1_tumour.to_json(orient='values')
            
        
        elif inter_num == 2:
            if path_gene == 'pathways':
                
                group1 = PathwayGroup.objects.get(name=lMembers[0], report=report)
                df_1 = pd.read_csv(group1.doc_proc.path, index_col='Pathway')
                                
                group2 = PathwayGroup.objects.get(name=lMembers[1], report=report)
                df_2 = pd.read_csv(group2.doc_proc.path, index_col='Pathway')
                
            
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
            elif path_gene =='genes':
                
                group1 = GeneGroup.objects.get(name=lMembers[0], report=report)
                group2 = GeneGroup.objects.get(name=lMembers[1], report=report)
                
                df_1 = pd.read_csv(group1.doc_logfc.path,  index_col='SYMBOL')
                df_2 = pd.read_csv(group2.doc_logfc.path,  index_col='SYMBOL') 
                
                if df_1['adj.P.Val'].all() == 1:
                    df_1 = df_1[(np.absolute(df_1['logFC'])>2)]
                else:           
                    df_1 = df_1[(df_1['adj.P.Val']<0.05) & (np.absolute(df_1['logFC'])>0.4)]
                if df_2['adj.P.Val'].all() == 1:
                    df_2 = df_2[(np.absolute(df_2['logFC'])>2)]
                else:
                    df_2 = df_2[(df_2['adj.P.Val']<0.05) & (np.absolute(df_2['logFC'])>0.4)]
                
                df_1 = pd.DataFrame(df_1['logFC'])
                df_2 = pd.DataFrame(df_2['logFC'])
                df_1.columns = ['0']
                df_2.columns = ['0']
            
            s_tumour1 = df_1['0'].round(decimals=2)
            s_tumour1.name = lMembers[0]
            
            s_tumour2 = df_2['0'].round(decimals=2)
            s_tumour2.name = lMembers[1]
            if regulation == 'updown':
                s_tumour1_up = s_tumour1[s_tumour1>0]
                s_tumour1_down = s_tumour1[s_tumour1<0]
                s_tumour2_up = s_tumour2[s_tumour2>0]
                s_tumour2_down = s_tumour2[s_tumour2<0]
                
                df_up = pd.DataFrame(s_tumour1_up).join(pd.DataFrame(s_tumour2_up), how='inner', sort=True)         
                df_down = pd.DataFrame(s_tumour1_down).join(pd.DataFrame(s_tumour2_down), how='inner', sort=True)
                joined_df = df_up.append(df_down)
            elif regulation == 'up':            
                s_tumour1 = s_tumour1[s_tumour1>0]
                s_tumour2 = s_tumour2[s_tumour2>0]
                joined_df = pd.DataFrame(s_tumour1).join(pd.DataFrame(s_tumour2), how='inner')
            elif regulation == 'down':  
                s_tumour1 = s_tumour1[s_tumour1<0]
                s_tumour2 = s_tumour2[s_tumour2<0]
                joined_df = pd.DataFrame(s_tumour1).join(pd.DataFrame(s_tumour2), how='inner')
            
            joined_df.reset_index(inplace=True)
            df_json = joined_df.to_json(orient='values')
            
        elif inter_num == 3:
            if path_gene == 'pathways':
                group1 = PathwayGroup.objects.get(name=lMembers[0], report=report)
                df_1 = pd.read_csv(group1.doc_proc.path, index_col='Pathway')
                
                group2 = PathwayGroup.objects.get(name=lMembers[1], report=report)
                df_2 = pd.read_csv(group2.doc_proc.path, index_col='Pathway')
               
                group3 = PathwayGroup.objects.get(name=lMembers[2], report=report)
                df_3 = pd.read_csv(group3.doc_proc.path,  index_col='Pathway')
                
            
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                    df_3 = df_3[df_3['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
                    df_3 = df_3[df_3['Database']!='metabolism']
            
            elif path_gene =='genes':
                group1 = GeneGroup.objects.get(name=lMembers[0], report=report)
                group2 = GeneGroup.objects.get(name=lMembers[1], report=report)
                group3 = GeneGroup.objects.get(name=lMembers[2], report=report)
                
                df_1 = pd.read_csv(group1.doc_logfc.path,  index_col='SYMBOL')
                df_2 = pd.read_csv(group2.doc_logfc.path,  index_col='SYMBOL') 
                df_3 = pd.read_csv(group3.doc_logfc.path,  index_col='SYMBOL') 
                
                if df_1['adj.P.Val'].all() == 1:
                    df_1 = df_1[(np.absolute(df_1['logFC'])>2)]
                else:               
                    df_1 = df_1[(df_1['adj.P.Val']<0.05) & (np.absolute(df_1['logFC'])>0.4)]
                if df_2['adj.P.Val'].all() == 1:
                    df_2 = df_2[(np.absolute(df_2['logFC'])>2)]
                else:
                    df_2 = df_2[(df_2['adj.P.Val']<0.05) & (np.absolute(df_2['logFC'])>0.4)]
                if df_3['adj.P.Val'].all() == 1:
                    df_3 = df_3[(np.absolute(df_3['logFC'])>2)]
                else:
                    df_3 = df_3[(df_3['adj.P.Val']<0.05) & (np.absolute(df_3['logFC'])>0.4)]                
                
                df_1 = pd.DataFrame(df_1['logFC'])
                df_2 = pd.DataFrame(df_2['logFC'])
                df_3 = pd.DataFrame(df_3['logFC'])
                df_1.columns = ['0']
                df_2.columns = ['0']
                df_3.columns = ['0']
            
            
            s_tumour1 = df_1['0'].round(decimals=2)
            s_tumour1.name = lMembers[0]
           
            s_tumour2 = df_2['0'].round(decimals=2)
            s_tumour2.name = lMembers[1]
            
            s_tumour3 = df_3['0'].round(decimals=2)
            s_tumour3.name = lMembers[2]
            
            if regulation == 'updown':
                s_tumour1_up = s_tumour1[s_tumour1>0]
                s_tumour1_down = s_tumour1[s_tumour1<0]
                s_tumour2_up = s_tumour2[s_tumour2>0]
                s_tumour2_down = s_tumour2[s_tumour2<0]
                s_tumour3_up = s_tumour3[s_tumour3>0]
                s_tumour3_down = s_tumour3[s_tumour3<0]
                
                df_up = pd.DataFrame(s_tumour1_up).join(pd.DataFrame(s_tumour2_up), how='inner', sort=True)
                df_up = df_up.join(pd.DataFrame(s_tumour3_up), how='inner', sort=True)         
                df_down = pd.DataFrame(s_tumour1_down).join(pd.DataFrame(s_tumour2_down), how='inner', sort=True)
                df_down = df_down.join(pd.DataFrame(s_tumour3_down), how='inner', sort=True) 
                joined_df = df_up.append(df_down)
            elif regulation == 'up':            
                s_tumour1 = s_tumour1[s_tumour1>0]
                s_tumour2 = s_tumour2[s_tumour2>0]
                s_tumour3 = s_tumour3[s_tumour3>0]
                joined_df = pd.DataFrame(s_tumour1).join(pd.DataFrame(s_tumour2), how='inner')
                joined_df = joined_df.join(pd.DataFrame(s_tumour3), how='inner')
            elif regulation == 'down':  
                s_tumour1 = s_tumour1[s_tumour1<0]
                s_tumour2 = s_tumour2[s_tumour2<0]
                joined_df = pd.DataFrame(s_tumour1).join(pd.DataFrame(s_tumour2), how='inner')
                joined_df = joined_df.join(pd.DataFrame(s_tumour3), how='inner')
            
            joined_df.reset_index(inplace=True)
            df_json = joined_df.to_json(orient='values')
            
        response_data = {'aaData': json.loads(df_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl
import struct

def shiftedColorMap(cmap, start=0, midpoint=0, stop=1.0, name='shiftedcmap'):

    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap
    
class ReportAjaxPathDetail(TemplateView):
    template_name = 'website/report_ajax_pathway_detail.html'
    
   
    
    def dispatch(self, request, *args, **kwargs):
        return super(ReportAjaxPathDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ReportAjaxPathDetail, self).get_context_data(**kwargs)
        
        report = Report.objects.get(pk=self.request.GET['reportID'])
        group = GeneGroup.objects.get(report=report, name=self.request.GET['group_name'])
        organism = self.request.GET['organism']

        
        pathway = Pathway.objects.filter(organism=organism, name=self.request.GET['pathway']).exclude(database__in=['primary_old', 'aging'])[0]
        
        gene_data = []
        for gene in pathway.gene_set.all():
                nodes = ','.join([str(i) for i in Node.objects.filter(pathway=pathway, component__name=gene.name).distinct()])
                
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'Node(s)':nodes })   
           
        gene_df = pd.DataFrame(gene_data).set_index('SYMBOL')
               
        df_file_cnr = pd.read_csv(group.doc_logfc.path, index_col='SYMBOL')
        
        if df_file_cnr['adj.P.Val'].all() == 1:
                    df_file_cnr = df_file_cnr[(np.absolute(df_file_cnr['logFC'])>2)]
        else:        
            df_file_cnr = df_file_cnr[(df_file_cnr['adj.P.Val']<0.05) & (np.absolute(df_file_cnr['logFC'])>0.4)] 
        df_file_cnr = df_file_cnr['logFC'].round(decimals=2)
        
        
        df_file_cnr.name = 'log2(Fold-change)' #log2(Fold-change)
        
        joined_df = gene_df.join(df_file_cnr, how='inner')
        joined_df.reset_index(inplace=True)
        
        joined_df.index += 1
        
        context['joined'] = joined_df[['SYMBOL', 'Node(s)', 'log2(Fold-change)']].to_html(classes=['table', 'table-bordered', 'table-striped'])
        context['diff_genes_count'] = len(joined_df.index)
         
        nComp = []
        
        G=nx.DiGraph()
        
        for _, row in joined_df.iterrows():                
            
            loComp = Component.objects.filter(name = row['SYMBOL'], node__pathway=pathway)
            
            for comp in loComp:
                comp.cnr = np.power(2, row['log2(Fold-change)'])
                nComp.append(comp)
                    
        lNodes = []
        lNEL = []        
        
        for node in pathway.node_set.all():
            
            lcurrentComponents = [i.name for i in node.component_set.all()]
            
            node.nel = 0.0
            node.numDiffComp = 0
            node.sumDiffComp = 0.0
            node.color = "grey"
            node.strokeWidth = 1
            for component in nComp:
                if component.name in lcurrentComponents: 
                    if component.cnr != 0:
                        node.numDiffComp += 1
                        node.sumDiffComp += float(component.cnr)
            if node.numDiffComp >0 :
                node.nel = node.sumDiffComp / node.numDiffComp
                lNEL.append(node.sumDiffComp / node.numDiffComp)
            lNodes.append(node)
                
        if lNEL: #check if list is not empty
            #choosing colormap for static image
            lNEL = np.log(lNEL)
            mmin = np.min(lNEL)
            mmax = np.max(np.absolute(lNEL)) # absolute was made for Aliper special, remove if needed
            mid = 1 - mmax/(mmax + abs(mmin))
        
            if mmax<0 and mmin<0:                    
                shifted_cmap = plt.get_cmap('Reds_r')
                mmax = 0
            if  mmax>0 and mmin>0:
                shifted_cmap = plt.get_cmap('Greens')
                mmin = 0
            else:  
                cmap = plt.get_cmap('PiYG')
                shifted_cmap = shiftedColorMap(cmap, start=0, midpoint=mid, stop=1, name='shrunk')
            cNormp  = colors.Normalize(vmin=mmin, vmax=mmax)
            scalarMap = cmx.ScalarMappable(norm=cNormp, cmap=shifted_cmap)
        
        finalNodes = []
        for nod in lNodes:
            if nod.nel > 1:
                nod.color = "green"
                nod.strokeWidth = np.log2(nod.nel)
            if nod.nel <= 1 and nod.nel > 0:
                nod.color = "red"
                nod.strokeWidth = np.log2(nod.nel)
            finalNodes.append(nod)
            
            if nod.nel!=0:
                ffil = "#"+struct.pack('BBB',*scalarMap.to_rgba(np.log(nod.nel), bytes=True)[:3]).encode('hex').upper()
            else:
                ffil = "grey"
            G.add_node(nod.name, color='black',style='filled',
                               fillcolor=ffil)            
        
        context['colorNodes'] = finalNodes              
        
        dRelations = []
        for node in pathway.node_set.all():
            for inrel in node.inrelations.all():
                relColor = 'black'
                if inrel.reltype == '1':
                    relColor = 'green'
                if inrel.reltype == '0':
                    relColor = 'red'
                dRelations.append({ inrel.fromnode.name : [inrel.tonode.name, relColor] })
                G.add_edge(inrel.fromnode.name.encode('ascii','ignore'), inrel.tonode.name.encode('ascii','ignore'), color=relColor)      
        
        # DRAW STATIC IMAGE
        A=nx.to_agraph(G)
        A.layout(prog='dot')
        A.draw(settings.MEDIA_ROOT+"/pathway.svg")
        
        context['pathway'] = pathway
        context['dRelations'] = dRelations
        import random 
        context['rand'] = random.random() 
        
        
        
        return context    
    