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

class GPReport(TemplateView):
    template_name = "website/gp_report.html"
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(GPReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(GPReport, self).get_context_data(**kwargs)
        
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
    
    
class GPReportPathwayTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(GPReportPathwayTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name1 = request.GET.get('file_name1')
        file_name2 = request.GET.get('file_name2')
        is_metabolic = request.GET.get('is_metabolic')
        
        
        if file_name1 == 'all':
            
            if file_name2 == "MCF7":
                df_Myricetin = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_Myricetin.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
                df_Epigallocatechin = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_Epigallocatechin gallate.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
                df_acetylcysteine = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_N-acetylcysteine.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
            else:
                df_Myricetin = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
                df_Epigallocatechin = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
                df_acetylcysteine = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx",
                                 sheetname='PAS1', index_col='Pathway')
            
            
            if is_metabolic == 'meta':
                df_acetylcysteine = df_acetylcysteine[df_acetylcysteine['Database']=='metabolism']
                df_Myricetin = df_Myricetin[df_Myricetin['Database']=='metabolism']
                df_Epigallocatechin = df_Epigallocatechin[df_Epigallocatechin['Database']=='metabolism']
                
            elif is_metabolic == 'path':
                df_acetylcysteine = df_acetylcysteine[(df_acetylcysteine['Database']!='metabolism' )]
                df_Myricetin = df_Myricetin[(df_Myricetin['Database']!='metabolism' )]
                df_Epigallocatechin = df_Epigallocatechin[(df_Epigallocatechin['Database']!='metabolism' )]
            
                df_acetylcysteine = df_acetylcysteine[df_acetylcysteine['Database']!='aging']
                df_Myricetin = df_Myricetin[df_Myricetin['Database']!='aging']
                df_Epigallocatechin = df_Epigallocatechin[df_Epigallocatechin['Database']!='aging']
            elif is_metabolic == 'age':
                df_acetylcysteine = df_acetylcysteine[df_acetylcysteine['Database']=='aging']
                df_Myricetin = df_Myricetin[df_Myricetin['Database']=='aging']
                df_Epigallocatechin = df_Epigallocatechin[df_Epigallocatechin['Database']=='aging']     
            
            
            
            df_acetylcysteine_tumour = df_acetylcysteine[[x for x in df_acetylcysteine.columns if 'Tumour' in x]]
            s_acetylcysteine_tumour = df_acetylcysteine_tumour.mean(axis=1).round(decimals=2)
            df_Myricetin_tumour = df_Myricetin[[x for x in df_Myricetin.columns if 'Tumour' in x]]
            s_Myricetin_tumour = df_Myricetin_tumour.mean(axis=1).round(decimals=2)
            df_Epigallocatechin_tumour = df_Epigallocatechin[[x for x in df_Epigallocatechin.columns if 'Tumour' in x]]
            s_Epigallocatechin_tumour_tumour = df_Epigallocatechin_tumour.mean(axis=1).round(decimals=2)

            
            df_output = pd.DataFrame()
            df_output['1'] = s_acetylcysteine_tumour
            df_output['2'] = s_Myricetin_tumour
            df_output['3'] = s_Epigallocatechin_tumour_tumour
            
            
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
        
            
            if is_metabolic=='meta':
                df_1 = df_1[df_1['Database']=='metabolism']
                df_2 = df_2[df_2['Database']=='metabolism']
            elif is_metabolic=='age' :
                df_1 = df_1[df_1['Database']=='aging']
                df_2 = df_2[df_2['Database']=='aging']
            elif is_metabolic=='path' :    
                df_1 = df_1[df_1['Database']!='metabolism']
                df_2 = df_2[df_2['Database']!='metabolism']
                
                df_1 = df_1[df_1['Database']!='aging']
                df_2 = df_2[df_2['Database']!='aging']
            
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
    
class GPReportAjaxPathDetail(TemplateView):
    template_name = 'website/report_ajax_pathway_detail.html'
    
   
    
    def dispatch(self, request, *args, **kwargs):
        return super(GPReportAjaxPathDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(GPReportAjaxPathDetail, self).get_context_data(**kwargs)
        
        pathway = Pathway.objects.filter(organism='human', name=self.request.GET['pathway']).exclude(database__in=['primary_old', 'kegg'])[0]
        
        gene_data = []
        for gene in pathway.gene_set.all():
                nodes = ','.join([str(i) for i in Node.objects.filter(pathway=pathway, component__name=gene.name).distinct()])
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'Node(s)':nodes })   
           
        gene_df = pd.DataFrame(gene_data).set_index('SYMBOL')    
        
        filename = 'cnr_'+self.request.GET['filename']+'.xlsx'
        
        
        df_file_cnr = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+filename)
        
        df1_tumour = df_file_cnr[[x for x in df_file_cnr.columns if 'Tumour' in x]]
        df_file_cnr['CNR'] = df1_tumour.mean(axis=1).round(decimals=2) 
        df_file_cnr = df_file_cnr[['SYMBOL', 'CNR']]
        
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
    
    
class GPReportAjaxPathwayVenn(TemplateView):
    template_name="website/report_ajax_venn.html"
    def dispatch(self, request, *args, **kwargs):
        return super(GPReportAjaxPathwayVenn, self).dispatch(request, *args, **kwargs)
    
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
        
        
        if path_gene == 'pathways' or path_gene=='MCF7':
            df1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+file_name1,
                                  sheetname='PAS1', index_col='Pathway')
            df2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+file_name2,
                                 sheetname='PAS1', index_col='Pathway')
            df3 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+file_name3,
                                  sheetname='PAS1', index_col='Pathway')           
         
            if is_metabolic=='meta':
                df1 = df1[df1['Database']=='metabolism']
                df2 = df2[df2['Database']=='metabolism']
                df3 = df3[df3['Database']=='metabolism']
            elif is_metabolic=='age':
                df1 = df1[df1['Database']=='aging']
                df2 = df2[df2['Database']=='aging']
                df3 = df3[df3['Database']=='aging']
            elif is_metabolic=='path':
                df1 = df1[(df1['Database']!='metabolism') ]
                df2 = df2[(df2['Database']!='metabolism') ]
                df3 = df3[(df3['Database']!='metabolism')]
                
                df1 = df1[df1['Database']!='aging']
                df2 = df2[df2['Database']!='aging']
                df3 = df3[df3['Database']!='aging']
                
            df1_tumour = df1[[x for x in df1.columns if 'Tumour' in x]]
            df1['0'] = df1_tumour.mean(axis=1).round(decimals=2)
            
            df2_tumour = df2[[x for x in df2.columns if 'Tumour' in x]]
            df2['0'] = df2_tumour.mean(axis=1).round(decimals=2)
            
            df3_tumour = df3[[x for x in df3.columns if 'Tumour' in x]]
            df3['0'] = df3_tumour.mean(axis=1).round(decimals=2)
                 
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
    
class GPReportAjaxPathwayVennTable(TemplateView):
    template_name="website/report_ajax_venn.html"
    def dispatch(self, request, *args, **kwargs):
        return super(GPReportAjaxPathwayVennTable, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        inter_num = int(self.request.GET.get('inter_num'))
        regulation = self.request.GET.get('regulation')
        members = self.request.GET.get('members')
        is_metabolic = self.request.GET.get('is_metabolic')
        path_gene = self.request.GET.get('path_gene')
        
        lMembers = members.split('vs')
        
        
        
        if inter_num == 1:
            if path_gene == 'pathways':
                df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+lMembers[0]+".xlsx",
                                  sheetname='PAS1', index_col='Pathway')
            
                
                if is_metabolic=='true':
                    df_1 = df_1[df_1['Database']=='metabolism']
                else:                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    
                df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
                df_1['0'] = df1_tumour.mean(axis=1).round(decimals=2)       
                
            elif path_gene =='MCF7':
                df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_"+lMembers[0]+".xlsx",
                                  sheetname='PAS1', index_col='Pathway')
            
                
                if is_metabolic=='meta':
                    df_1 = df_1[df_1['Database']=='metabolism']
                elif is_metabolic=='age':
                    df_1 = df_1[df_1['Database']=='aging']
                elif is_metabolic=='path':                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_1 = df_1[df_1['Database']!='aging']
                    
                df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
                df_1['0'] = df1_tumour.mean(axis=1).round(decimals=2) 
            
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
                df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+lMembers[0]+".xlsx",
                                 sheetname='PAS1',index_col='Pathway') 
                df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+lMembers[1]+".xlsx",
                                 sheetname='PAS1',index_col='Pathway')
            
                if is_metabolic=='meta':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                elif is_metabolic=='age':
                    df_1 = df_1[df_1['Database']=='aging']
                    df_2 = df_2[df_2['Database']=='aging']
                elif is_metabolic=='path':                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
                    
                    df_1 = df_1[df_1['Database']!='aging']
                    df_2 = df_2[df_2['Database']!='aging']
            
                df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
                df_1['0'] = df1_tumour.mean(axis=1).round(decimals=2)
                df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
                df_2['0'] = df2_tumour.mean(axis=1).round(decimals=2)
            
            elif path_gene =='MCF7':
                df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_"+lMembers[0]+".xlsx",
                                 sheetname='PAS1',index_col='Pathway') 
                df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_"+lMembers[1]+".xlsx",
                                 sheetname='PAS1',index_col='Pathway')
            
                if is_metabolic=='meta':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                elif is_metabolic=='age':
                    df_1 = df_1[df_1['Database']=='aging']
                    df_2 = df_2[df_2['Database']=='aging']
                elif is_metabolic=='path':               
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
                    
                    df_1 = df_1[df_1['Database']!='aging']
                    df_2 = df_2[df_2['Database']!='aging']
            
                df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
                df_1['0'] = df1_tumour.mean(axis=1).round(decimals=2)
                df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
                df_2['0'] = df2_tumour.mean(axis=1).round(decimals=2)
                
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
                df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+lMembers[0]+".xlsx",
                                sheetname='PAS1',index_col='Pathway') 
                df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+lMembers[1]+".xlsx",
                                 sheetname='PAS1',index_col='Pathway')
                df_3 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/"+lMembers[2]+".xlsx",
                                sheetname='PAS1',index_col='Pathway')
            
                if is_metabolic=='meta':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                    df_3 = df_3[df_3['Database']=='metabolism']
                    
                elif is_metabolic=='age':
                    df_1 = df_1[df_1['Database']=='aging']
                    df_2 = df_2[df_2['Database']=='aging']
                    df_3 = df_3[df_3['Database']=='aging']
                elif is_metabolic=='path':                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
                    df_3 = df_3[df_3['Database']!='metabolism']
                    
                    df_1 = df_1[df_1['Database']!='aging']
                    df_2 = df_2[df_2['Database']!='aging']
                    df_3 = df_3[df_3['Database']!='aging']
                    
                df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
                df_1['0'] = df1_tumour.mean(axis=1).round(decimals=2)
                df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
                df_2['0'] = df2_tumour.mean(axis=1).round(decimals=2)
                df3_tumour = df_3[[x for x in df_3.columns if 'Tumour' in x]]
                df_3['0'] = df3_tumour.mean(axis=1).round(decimals=2)
            
            if path_gene == 'MCF7':
                df_1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_"+lMembers[0]+".xlsx",
                                sheetname='PAS1',index_col='Pathway') 
                df_2 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_"+lMembers[1]+".xlsx",
                                 sheetname='PAS1',index_col='Pathway')
                df_3 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/GPcomp/output_"+lMembers[2]+".xlsx",
                                sheetname='PAS1',index_col='Pathway')
            
                if is_metabolic=='meta':
                    df_1 = df_1[df_1['Database']=='metabolism']
                    df_2 = df_2[df_2['Database']=='metabolism']
                    df_3 = df_3[df_3['Database']=='metabolism']
                    
                elif is_metabolic=='age':
                    df_1 = df_1[df_1['Database']=='aging']
                    df_2 = df_2[df_2['Database']=='aging']
                    df_3 = df_3[df_3['Database']=='aging']
                elif is_metabolic=='path':                
                    df_1 = df_1[df_1['Database']!='metabolism']
                    df_2 = df_2[df_2['Database']!='metabolism']
                    df_3 = df_3[df_3['Database']!='metabolism']
                    
                    df_1 = df_1[df_1['Database']!='aging']
                    df_2 = df_2[df_2['Database']!='aging']
                    df_3 = df_3[df_3['Database']!='aging']
                    
                df1_tumour = df_1[[x for x in df_1.columns if 'Tumour' in x]]
                df_1['0'] = df1_tumour.mean(axis=1).round(decimals=2)
                df2_tumour = df_2[[x for x in df_2.columns if 'Tumour' in x]]
                df_2['0'] = df2_tumour.mean(axis=1).round(decimals=2)
                df3_tumour = df_3[[x for x in df_3.columns if 'Tumour' in x]]
                df_3['0'] = df3_tumour.mean(axis=1).round(decimals=2)
            
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
                s_tumour3 = s_tumour3[s_tumour3<0]
                joined_df = pd.DataFrame(s_tumour1).join(pd.DataFrame(s_tumour2), how='inner')
                joined_df = joined_df.join(pd.DataFrame(s_tumour3), how='inner')
            
            joined_df.reset_index(inplace=True)
            df_json = joined_df.to_json(orient='values')
            
        response_data = {'aaData': json.loads(df_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")    