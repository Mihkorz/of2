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

class Demo2Report(TemplateView):
    template_name = "website/demo2_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(Demo2Report, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(Demo2Report, self).get_context_data(**kwargs)
        
        lEmbryonicGenes =[ 'PCDHB2', 'PCDHB17', 'CSTF3', 'LOC644919', 'ITGA11', 'SMA4',
                          'LOC727877', 'MAST2', 'TMEM18', 'LOC100130914', 'ADSSL1', 'ZNF767',
                          'C19orf25', 'C19orf6', 'NKTR', 'LOC286208', 'GOLGA8A', 'CDK5RAP3',
                          'OPN3', 'MGC16384', 'ZNF33A', 'LOC100190939', 'TPM1', 'GSDMB', 'NR3C1']
               
        lAdultGenes = ['COX7A1', 'ZNF280D', 'LOC441408', 'TRIM4', 'NIN', 'NAALADL1', 'ASF1B',
                       'COMT', 'CAT', 'C18orf56', 'LOC440731', 'HOXA5', 'LOC375295', 'POLQ',
                        'MEG3', 'CDT1', 'FOS']
        
        context['lEmbryonicGenes'] = lEmbryonicGenes
        
        context['lAdultGenes'] = lAdultGenes
        
        return context
    
    
class BTGeneVolcanoJson(TemplateView):
    template_name="website/bt_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTGeneVolcanoJson, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        file_name = request.POST.get('file_name')
        
        df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name, sep='\t')
        
        df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
        
        df_gene.rename(columns={'gene': 'Symbol'}, inplace=True)
        
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

class BTReportGeneTableJson(TemplateView):
    template_name="website/bt_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTReportGeneTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        
        if file_name!='all':
            df_gene = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name, sep='\t')
        
            df_gene = df_gene[['gene', 'logFC', 'adj.P.Val']]
        
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
    
class BTReportGeneBoxplotJson(TemplateView):
    template_name="website/report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTReportGeneBoxplotJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene  = request.GET.get('gene')
        
        
        
        df_ES = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ES.onc.tab",
                                index_col='SYMBOL', sep='\t' )
        df_ASC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ASC.onc.tab",
                                index_col='SYMBOL', sep='\t')
        df_ABC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ABC.onc.tab",
                                index_col='SYMBOL', )
        df_AEC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_AEC.onc.tab",
                                index_col='SYMBOL', sep='\t')
        df_ANC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_ANC.onc.tab",
                                index_col='SYMBOL', sep='\t')
        df_CCL = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/box_EPL_vs_CCL.onc.tab",
                                index_col='SYMBOL', sep='\t')
        
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
                          'headerFormat': '<em>Group: {point.key}</em><br/>'
                          }
              }
        
        
        
        response_data = s1
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class BTReportPathwayTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(BTReportPathwayTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name1 = request.GET.get('file_name1')
        file_name2 = request.GET.get('file_name2')
        is_metabolic = request.GET.get('is_metabolic')
        if is_metabolic =='false':
            is_metabolic = False
        else:
            is_metabolic = True
        
        if file_name1 == file_name2 == 'all':
            df_ES = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_ES.csv",
                                 index_col='Pathway')
            df_ASC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_ASC.csv",
                                 index_col='Pathway')
            df_ABC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_ABC.csv",
                                 index_col='Pathway')
            df_AEC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_AEC.csv",
                                 index_col='Pathway')
            df_ANC = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_ANC.csv",
                                 index_col='Pathway')
            df_CCL = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_CCL.csv",
                                 index_col='Pathway')
            
            if is_metabolic:
                df_ES = df_ES[df_ES['Database']=='metabolism']
                df_ASC = df_ASC[df_ASC['Database']=='metabolism']
                df_ABC = df_ABC[df_ABC['Database']=='metabolism']
                df_AEC = df_AEC[df_AEC['Database']=='metabolism']
                df_ANC = df_ANC[df_ANC['Database']=='metabolism']
                df_CCL = df_CCL[df_CCL['Database']=='metabolism']
            else:
                df_ES = df_ES[df_ES['Database']!='metabolism']
                df_ASC = df_ASC[df_ASC['Database']!='metabolism']
                df_ABC = df_ABC[df_ABC['Database']!='metabolism']
                df_AEC = df_AEC[df_AEC['Database']!='metabolism']
                df_ANC = df_ANC[df_ANC['Database']!='metabolism']
                df_CCL = df_CCL[df_CCL['Database']!='metabolism']
            
            
            
            df_output = pd.DataFrame()
            df_output['1'] = df_ES['0'].round(decimals=2)
            df_output['2'] = df_ASC['0'].round(decimals=2)
            df_output['3'] = df_ABC['0'].round(decimals=2)
            df_output['4'] = df_AEC['0'].round(decimals=2)
            df_output['5'] = df_ANC['0'].round(decimals=2)
            df_output['6'] = df_CCL['0'].round(decimals=2)
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
    
class BTReportAjaxPathDetail(TemplateView):
    template_name = 'website/report_ajax_pathway_detail.html'
    
   
    
    def dispatch(self, request, *args, **kwargs):
        return super(BTReportAjaxPathDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(BTReportAjaxPathDetail, self).get_context_data(**kwargs)
        
        pathway = Pathway.objects.filter(organism='human', name=self.request.GET['pathway']).exclude(database='primary_old')[0]
        
        gene_data = []
        for gene in pathway.gene_set.all():
                nodes = ','.join([str(i) for i in Node.objects.filter(pathway=pathway, component__name=gene.name).distinct()])
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'Node(s)':nodes })   
           
        gene_df = pd.DataFrame(gene_data).set_index('SYMBOL')    
        
        filename = 'cnr_proc_EPL_vs_'+self.request.GET['filename']+'.csv'
        
        
        df_file_cnr = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+filename)
        
        df_file_cnr.columns = ['SYMBOL', 'CNR']
        df_file_cnr.set_index('SYMBOL', inplace=True)
        
        
        df_cnr_raw = df_file_cnr['CNR'].round(decimals=2)
        #raise Exception('draw path')
        
        df_cnr_differential = df_cnr_raw[df_cnr_raw!=1]
        df_cnr_differential.name = 'CNR' #log2(Fold-change)
        
        joined_df = gene_df.join(df_cnr_differential, how='inner')
        joined_df.reset_index(inplace=True)
        joined_df['log2(Fold-change)'] = np.log2(joined_df['CNR']).round(decimals=2)
        joined_df.index += 1
        context['joined'] = joined_df[['SYMBOL', 'Node(s)', 'log2(Fold-change)']].to_html(classes=['table', 'table-bordered', 'table-striped'])
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
    
    
class BTReportAjaxPathwayVenn(TemplateView):
    template_name="website/report_ajax_venn.html"
    def dispatch(self, request, *args, **kwargs):
        return super(BTReportAjaxPathwayVenn, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
          
                
        file_name1 = self.request.GET.get('file_name1')
        name1 = self.request.GET.get('name1')
        file_name2 = self.request.GET.get('file_name2')        
        name2 = self.request.GET.get('name2')
        file_name3 = self.request.GET.get('file_name3')        
        name3 = self.request.GET.get('name3')
        is_metabolic = self.request.GET.get('is_metabolic')
        regulation = self.request.GET.get('regulation')
        path_gene = self.request.GET.get('path_gene')
              
        
        venn_cyrcles = []
        
        
        if path_gene == 'pathways':
            df1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name1,
                                  index_col='Pathway')
            df2 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name2,
                                 index_col='Pathway')
            df3 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name3,
                                  index_col='Pathway')           
         
            if is_metabolic=='true':
                df1 = df1[df1['Database']=='metabolism']
                df2 = df2[df2['Database']=='metabolism']
                df3 = df3[df3['Database']=='metabolism']
            else:
                df1 = df1[df1['Database']!='metabolism']
                df2 = df2[df2['Database']!='metabolism']
                df3 = df3[df3['Database']!='metabolism']
                
        elif path_gene == 'genes':
            df1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name1,
                                  sep='\t', index_col='gene')
            df1 = df1[(df1['adj.P.Val']<0.05) & (np.absolute(df1['logFC'])>0.4)] 
            df2 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name2,
                                 sep='\t', index_col='gene')
            df2 = df2[(df2['adj.P.Val']<0.05) & (np.absolute(df2['logFC'])>0.4)] 
            df3 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/"+file_name3,
                                  sep='\t', index_col='gene')
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
                                     'id': '1_updown_'+name1+'_'+is_metabolic})
        elif regulation == 'up':
            venn_cyrcles.append({'sets': [name1], 'size': (st1_tumour_up.count()),
                                     'id': '1_up_'+name1+'_'+is_metabolic})
        elif regulation == 'down':
            venn_cyrcles.append({'sets': [name1], 'size': (st1_tumour_down.count()),
                                     'id': '1_down_'+name1+'_'+is_metabolic})
        dict_s[name1] = st1_tumour
        dict_s[name1+' up'] = st1_tumour_up.index
        dict_s[name1+' down'] = st1_tumour_down.index        
          
           
        st2_tumour = df2['0']
        st2_tumour_up = st2_tumour[st2_tumour>0]
        st2_tumour_down = st2_tumour[st2_tumour<0]
        if regulation == 'updown':
            venn_cyrcles.append({'sets': [name2], 'size': (st2_tumour_up.count()+st2_tumour_down.count()),
                                     'id': '1_updown_'+name2+'_'+is_metabolic})
        elif regulation == 'up':
            venn_cyrcles.append({'sets': [name2], 'size': (st2_tumour_up.count()),
                                     'id': '1_up_'+name2+'_'+is_metabolic})
        elif regulation == 'down':
            venn_cyrcles.append({'sets': [name2], 'size': (st2_tumour_down.count()),
                                     'id': '1_down_'+name2+'_'+is_metabolic})    
        dict_s[name2] = st2_tumour
        dict_s[name2+' up'] = st2_tumour_up.index
        dict_s[name2+' down'] = st2_tumour_down.index
          
        st3_tumour = df3['0']
        st3_tumour_up = st3_tumour[st3_tumour>0]
        st3_tumour_down = st3_tumour[st3_tumour<0]
        if regulation == 'updown':
                venn_cyrcles.append({'sets': [name3], 'size': (st3_tumour_up.count()+st3_tumour_down.count()),
                                     'id': '1_updown_'+name3+'_'+is_metabolic})
        elif regulation == 'up':
                venn_cyrcles.append({'sets': [name3], 'size': (st3_tumour_up.count()),
                                     'id': '1_up_'+name3+'_'+is_metabolic})
        elif regulation == 'down':
                venn_cyrcles.append({'sets': [name3], 'size': (st3_tumour_down.count()),
                                     'id': '1_down_'+name3+'_'+is_metabolic})
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
                id_x = '2_updown_'+combination[0]+'vs'+ combination[1]+'_'+is_metabolic
            elif regulation == 'up':
                intersection = len(index1_up.intersection(index2_up))
                id_x = '2_up_'+combination[0]+'vs'+ combination[1]+'_'+is_metabolic
            elif regulation == 'down':
                intersection = len(index1_down.intersection(index2_down))
                id_x = '2_down_'+combination[0]+'vs'+ combination[1]+'_'+is_metabolic
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
                id_x = '3_updown_'+combination[0]+'vs'+combination[1]+'vs'+combination[2]+'_'+is_metabolic
            elif regulation == 'up':
                intersection = len(inter_up)
                id_x = '3_up_'+combination[0]+'vs'+combination[1]+'vs'+combination[2]+'_'+is_metabolic
            elif regulation == 'down':
                intersection = len(inter_down)
                id_x = '3_down_'+combination[0]+'vs'+combination[1]+'vs'+combination[2]+'_'+is_metabolic
            venn_cyrcles.append({'sets': [combination[0], combination[1], combination[2]],
                                     'size': intersection,
                                     'id': id_x})
 
            #raise Exception('venn all')

        response_data= venn_cyrcles

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
class BTReportAjaxPathwayVennTable(TemplateView):
    template_name="website/report_ajax_venn.html"
    def dispatch(self, request, *args, **kwargs):
        return super(BTReportAjaxPathwayVennTable, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        inter_num = int(self.request.GET.get('inter_num'))
        regulation = self.request.GET.get('regulation')
        members = self.request.GET.get('members')
        is_metabolic = self.request.GET.get('is_metabolic')
        path_gene = self.request.GET.get('path_gene')
        
        lMembers = members.split('vs')
        
        
        
        if inter_num == 1:
            if path_gene == 'pathways':
                df_1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_"+lMembers[0]+".csv",
                                 index_col='Pathway')
            
                        
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                
            elif path_gene =='genes':
                df_1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_"+lMembers[0]+".DE.tab",
                                 sep='\t', index_col='gene')           
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
                df_1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_"+lMembers[0]+".csv",
                                 index_col='Pathway') 
                df_2 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_"+lMembers[1]+".csv",
                                 index_col='Pathway')
            
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
            elif path_gene =='genes':
                df_1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_"+lMembers[0]+".DE.tab",
                                 sep='\t', index_col='gene')
                df_2 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_"+lMembers[1]+".DE.tab",
                                 sep='\t', index_col='gene')           
                df_1 = df_1[(df_1['adj.P.Val']<0.05) & (np.absolute(df_1['logFC'])>0.4)]
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
                df_1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_"+lMembers[0]+".csv",
                                index_col='Pathway') 
                df_2 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_"+lMembers[1]+".csv",
                                 index_col='Pathway')
                df_3 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/pros_output_EPL_vs_"+lMembers[2]+".csv",
                                index_col='Pathway')
            
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                    df_3 = df_3[df_3['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
                    df_3 = df_3[df_3['Database']!='metabolism']
            
            elif path_gene =='genes':
                df_1 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_"+lMembers[0]+".DE.tab",
                                 sep='\t', index_col='gene')
                df_2 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_"+lMembers[1]+".DE.tab",
                                 sep='\t', index_col='gene')
                df_3 = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/bt/EPL_vs_"+lMembers[2]+".DE.tab",
                                 sep='\t', index_col='gene')           
                
                df_1 = df_1[(df_1['adj.P.Val']<0.05) & (np.absolute(df_1['logFC'])>0.4)]
                df_2 = df_2[(df_2['adj.P.Val']<0.05) & (np.absolute(df_2['logFC'])>0.4)]
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











