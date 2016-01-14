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


class LorealReport(TemplateView):
    template_name = "website/loreal_report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LorealReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(LorealReport, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context


class ReportGeneScatterJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneScatterJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')        
        
        df_gene = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/cnr_"+file_name,
                                index_col='SYMBOL')
        
        df_tumour = df_gene[[x for x in df_gene.columns if 'Tumour' in x]]
        s_tumour = df_tumour.mean(axis=1).round(decimals=2)
        
        df_norm = df_gene[[x for x in df_gene.columns if 'Norm' in x]]
        s_norm = df_norm.mean(axis=1).round(decimals=2)        
        
        df_output = pd.DataFrame()
        
        df_output['x'] = s_tumour
        df_output['y'] = s_norm
        df_output = df_output.multiply(df_gene['gMean_norm'], axis=0)
        df_output = np.log2(df_output)
        
        df_output = df_output[df_output['x']>0 ]
        
        df_output.index.name='name'
        df_output.reset_index(inplace=True)
        
        df_output = df_output.to_json(orient='records')        
        
        response_data =  json.loads(df_output)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
class ReportGeneTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        df_gene = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/cnr_"+file_name,
                                index_col='SYMBOL')
        
        df_tumour = df_gene[[x for x in df_gene.columns if 'Tumour' in x]]
        s_tumour = df_tumour.mean(axis=1)
        s_tumour = np.log2(s_tumour).round(decimals=2)
        df_output = pd.DataFrame()
        df_output['log2FoldChange'] = s_tumour
        df_output['pval'] = df_gene['p_value']
        df_output['padj'] = df_gene['q_value']
        
        df_output = df_output[df_output['log2FoldChange']>0 ]
        df_output.index.name = 'Gene'
        df_output.reset_index(inplace=True)
        #raise Exception('gene table')
        
        output_json = df_output.to_json(orient='values')
        
        
        
        response_data = {'data': json.loads(output_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class ReportGeneDetailJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportGeneDetailJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene_name = request.GET.get('gene')
        file_name = request.GET.get('file_name')
        
        df_gene = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/cnr_"+file_name,
                                index_col='SYMBOL')
        
        df_tumour = df_gene[[x for x in df_gene.columns if 'Tumour' in x]]
        s_tumour = df_tumour.mean(axis=1)
        
        df_norm = df_gene[[x for x in df_gene.columns if 'Norm' in x]]
        s_norm = df_norm.mean(axis=1)       
        
        df_output = pd.DataFrame()
        
        df_output['x'] = s_tumour
        df_output['y'] = s_norm
        df_output = df_output.multiply(df_gene['gMean_norm']  , axis=0)
        
        df_output = df_output[df_output['x']>0 ]
        
        gene_row = df_output.loc[gene_name].round(decimals=0)
        
        response_data = {}
        response_data['NHE'] = [
                   ['NHE', gene_row['y']],
                   ['Case', 0]
                   ]
        response_data['Case'] = [
                   ['NHE', 0],
                   ['Case', gene_row['x']]
                   ]
        
        #raise Exception('gene detail')
        return HttpResponse(json.dumps(response_data), content_type="application/json")



class ReportPathwayScatterJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportPathwayScatterJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name1 = request.GET.get('file_name1') 
        file_name2 = request.GET.get('file_name2')       
        
        
        df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+file_name1,
                                sheetname='PAS1', index_col='Pathway')
        df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+file_name2,
                                 sheetname='PAS1', index_col='Pathway')
        
        df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
        s1_tumour = df1_tumour.mean(axis=1)
        
        df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
        s2_tumour = df2_tumour.mean(axis=1)               
        
        df_output = pd.DataFrame()
        
        df_output['x'] = s1_tumour
        df_output['y'] = s2_tumour
        
        #df_output = df_output[df_output['x']>0 ]
        #df_output = df_output[df_output['y']>0 ]
        
        df_output.index.name='name'
        df_output.reset_index(inplace=True)
        
        df_output = df_output.to_json(orient='records')        
        #raise Exception('path scatter')
        response_data =  json.loads(df_output)
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class ReportPathwayTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportPathwayTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name1 = request.GET.get('file_name1')
        file_name2 = request.GET.get('file_name2')
        
        if file_name1 == file_name2 == 'all':
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
            
            df_output.reset_index(inplace=True)
            
            
        else:
            df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+file_name1,
                                sheetname='PAS1', index_col='Pathway')
            df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+file_name2,
                                 sheetname='PAS1', index_col='Pathway')
        
            df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
            s1_tumour = df1_tumour.mean(axis=1).round(decimals=2)
        
            df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
            s2_tumour = df2_tumour.mean(axis=1).round(decimals=2)               
        
            df_output = pd.DataFrame()
        
            df_output['1'] = s1_tumour
            df_output['2'] = s2_tumour
        
            df_output.reset_index(inplace=True)
        
        
        
        df_json = df_output.to_json(orient='values')
        
        
        
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
        
        pathway = Pathway.objects.filter(organism='human', name=self.request.GET['pathway']).exclude(database='primary_old')[0]
        
        gene_data = []
        for gene in pathway.gene_set.all():
                nodes = ','.join([str(i) for i in Node.objects.filter(pathway=pathway, component__name=gene.name).distinct()])
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'Node(s)':nodes })   
           
        gene_df = pd.DataFrame(gene_data).set_index('SYMBOL')    
        
        filename = 'cnr_'+self.request.GET['filename']
        
        
        df_file_cnr = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/loreal/"+filename, index_col='SYMBOL')
        
        df_cnr_raw = df_file_cnr[[x for x in df_file_cnr.columns if 'Tumour' in x]]
        df_cnr_raw = df_cnr_raw.mean(axis=1).round(decimals=2)
        
        df_cnr_differential = df_cnr_raw[df_cnr_raw!=1]
        df_cnr_differential.name = 'CNR'
        
        joined_df = gene_df.join(df_cnr_differential, how='inner')
        joined_df.reset_index(inplace=True)
        joined_df.index += 1
        context['joined'] = joined_df.to_html(classes=['table', 'table-bordered', 'table-striped'])
        context['diff_genes_count'] = len(joined_df.index)
        
        
        nComp = []
        
        G=nx.DiGraph()
        
        for _, row in joined_df.iterrows():                
            
            loComp = Component.objects.filter(name = row['SYMBOL'], node__pathway=pathway)
            
            for comp in loComp:
                comp.cnr = row['CNR']
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