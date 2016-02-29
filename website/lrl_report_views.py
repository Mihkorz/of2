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
        rText = """Resveratrol is known as a compound that can extend lifespan of model 
        <a href='http://www.geroprotectors.org/compounds/GP00177' target='_blank'>organisms</a>.<br/>
                   <strong>Targets:</strong> AHR, CAR15, Carbonic anhydrases 
                   (CA1, CA2, CA3, CA4, CA9, CA5A, CA5B, CA6, CA7, CA12, CA13, CA14), 
                   PTGS1, Cytochromes (CYP1A1, CYP1A2, CYP1B1, CYP2A6, CYP2B6, CYP2E1, CYP3A4),
                    PLA2G4A, SULT1E1, TYR. <br/><br/>
                    Resveratrol is a potential oncosuppressor because of its ability to inhibit various
                     cytochromes [4].  Incubation with resveratrol resulted in suppression of expression of 
                     collagen coding genes and fibronectin gene (FN1) in keratinocytes. Also, on a gene expression
                      level resveratrol in 50 µM concentration demonstrated suppression of β subunit of AMPK.
                       Resveratrol demonstrated strong suppression of mTOR pathway with inhibition of mTORC1 
                       complex after 48 hours of incubation. Lower concentration (10 µM) showed stronger 
                       inhibition of mTOR pathway generally due to the absence of compensatory effects of 
                       upregulation Ras-ERK pathway, which can be observed in case of higher 
                       concentration (50 µM).<br/>
Higher resveratrol concentration (50 µM) showed stronger suppression
 of AMPK pathway after 48 hours of incubation than 10 µM concentration. 
 Also, after treatment with 50 µM concentration of the compound cells
  demonstrated upregulation of stress pathways, such as p38 signaling pathway, 
  PTEN Pathway DNA Repair, etc. [5]. Thus the lower concentration of resveratrol 
  seems to be more beneficial.
                    
                    """
        
        raText = """ <strong>Targets:</strong> Retinoic Acid Receptors (RARA, RARB, RARG, RXRA, RXRB, RXRG), 
        RARRES1, FFAR1, GPRC5A, RGR, PRKCA <br/><br/>
        Upregulation of HAS2, a gene that codes major hyaluronan synthase in human, is observed in all samples
         incubated with Retinoic acid. However, upregulation of AMPK pathway, which occurs in samples after
48 hours of incubation, could suppress hyaluronic acid synthesis on protein level [6,7] <br/>
After 48 hours of incubation mTOR pathway was inhibited (with both mTORC1 and mTORC2 complexes affected)
 and while suppression of mTORC1 could be beneficial to longevity, suppression of mTORC2 leads to the 
 reduction of insulin sensitivity [8].<br/>
Upregulation of TGF-beta signaling pathway occured after short period of incubation (24 hours) and 
appeared to be beneficial to the skin aging process. However, after 48 hours of incubation keratinocytes 
started to demonstrate suppression of TGF-beta pathway. TGF-beta pathway is usually depressed in photoaged 
and aged skin and causes reduction of collagen [9].<br/>
Incubation with Retinoic acid led to upregulation of stress related pathways, such as p38 signaling pathway
 and STAT3, with the suppression of anti-apoptosis pathways (strong down regulation of PTEN pathway, etc.) [10]
        
        """
        
        mhText = """<strong>Targets:</strong> EGFR, INSR, GCG, AMPK (PRKAA1, PRKAA2, PRKAB1), SLC47A1, CES1,
         DPP4, MAPK1, MAPK3, NCOA1, RPS6KB1<br/><br/>
         Metformin is a well known compound that shows strong potential to increase longevity of 
         <a href='http://www.geroprotectors.org/compounds/GP00132' target='_blank'>model organisms</a> 
         and human.<br/> 
Despite the fact that mTORC1 complex is slightly downregulated, the whole mTOR main pathway is upregulated. 
This could be due to the effects of compensation and cross-talk between mTOR and other pathways [11]. 
Higher concentration (4mM) of metformin triggered and upregulated AMPK pathway even after 24 hours of 
incubation, while 2 mM showed upregulation of AMPK only after 48 hours of incubation. Incubation of cells 
with metformin leads to strong upregulation of WNT signaling pathway, which might be beneficial to skin 
aging [12].
        """
        
        caText = """
        Suppression of COXs (Prostaglandin synthases) genes was observed only after 48 
        hours of incubation. Inhibition of KEGG Arachidonic acid metabolism Main Pathway 
        (Arachidonic acid is a predecessor of Prostaglandin) and downregulation of IL-10 
        pathway proved strong anti-inflammatory potential of Capryloyl salicylic acid.<br/>
Thus Capryloyl salicylic acid showed similar action as salicylic acid and aspirin. <br/>
Downregulation of mTOR pathway was observed after 48 hours of incubation, which could be a cellular response to upregulation after 24 hours of treatment. 
However, strong concentration and time-dependent suppression of TGF-beta pathway occurred in keratinocytes incubated with Capryloyl Salicylic acid. 
        """
        
        
        
        dSamples={'Retinoic acid': {'id': 'ra',
                                    'data': [['ra_24_01', '24h 0.1 µM'],
                                    ['ra_24_1', '24h 1 µM'],
                                    ['ra_48_01', '48h 0.1 µM'],
                                    ['ra_48_1', '48h 1 µM']],
                                    'text': raText
                                    },
                  'Metformin hydrochloride': {'id': 'mh',
                                              'data': [['mh_24_2', '24h 2 mM'],
                                                      ['mh_24_4', '24h 4 mM'],
                                                      ['mh_48_2', '48h 2 mM'],
                                                      ['mh_48_4', '48h 4 mM']],
                                              'text': mhText
                                              },
                  'Capryloyl salicylic acid': {'id': 'ca',
                                              'data': [['ca_24_5', '24h 5 µM'],
                                                      ['ca_24_10', '24h 10 µM'],
                                                      ['ca_48_5', '48h 5 µM'],
                                                      ['ca_48_10', '48h 10 µM']],
                                               'text': caText
                                              },
                  'Resveratrol': {'id': 're',
                                              'data': [['re_24_10', '24h 10 µM'],
                                                      ['re_24_50', '24h 50 µM'],
                                                      ['re_48_10', '48h 10 µM'],
                                                      ['re_48_50', '48h 50 µM']],
                                               'text': rText
                                              }
                   }
        
        context['dSamples'] = dSamples
        
        lGenes = ['COL1A1', 'COL1A2', 'KRT7', 'HYAL1', 'HYAL2',  'HAS1', 'HAS2',
               'ELN', 'MMP1', 'MMP13', 'MMP8', 'FN1', 'WNT1', 'EGF', 'EGFR', 'GH1', 'TGFB1',
               'TGFBR1', 'TGFBR2',
               'FGF1', 'FGFR1',  'MTOR']
        
        context['lGenes'] = lGenes
        
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
        df_output = np.log2(df_output).round(decimals=2)
        
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



class LRLReportGeneBoxplotJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportGeneBoxplotJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene  = request.GET.get('gene')
        
        
        
        df_ra = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/ra_concat.csv",
                                index_col='SYMBOL', )
        df_mh = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/mh_concat.csv",
                                index_col='SYMBOL', )
        df_ca = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/ca_concat.csv",
                                index_col='SYMBOL', )
        df_re = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/re_concat.csv",
                                index_col='SYMBOL', )
        
        series_tumour = []
        series_norm = []
        
        for df in [df_ra, df_mh, df_ca, df_re]:
            for t_n in ['Tumour', 'Norm']:
                
                filered_df = df[[x for x in df if t_n in x]]
                
                row_gene = np.array(filered_df.loc[gene].round(decimals=2))      
        
                median = np.around(np.median(row_gene), decimals=0) 
                upper_quartile = np.around(np.percentile(row_gene, 75), decimals=2)
                lower_quartile = np.around(np.percentile(row_gene, 25), decimals=2)
                iqr = upper_quartile - lower_quartile
                upper_whisker = np.around(row_gene[row_gene<=upper_quartile+1.5*iqr], decimals=2).max()
                lower_whisker = np.around(row_gene[row_gene>=lower_quartile-1.5*iqr], decimals=2).min()
                
                lSerie = [lower_whisker, lower_quartile, median, upper_quartile, upper_whisker]
                
                if t_n == 'Tumour':
                    series_tumour.append(lSerie)
                else:
                    series_norm.append(lSerie)
        
        
        s1 = {
              'name': 'Normal',              
              'data': series_norm,
              'tooltip': {
                          'headerFormat': '<em>Drug: {point.key}</em><br/>'
                          }
              }
        
        s2 = {
              'name': 'Case',
              'color': 'red',
              'data': series_tumour,
              'tooltip': {
                          'headerFormat': '<em>Drug: {point.key}</em><br/>'
                          }
              }
        
        
        response_data = [s1, s2]
        
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
            
            df = df[np.absolute(df[t_name])>1]
            
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
    
    

class LRLReportSideEffTableJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportSideEffTableJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        
        df = pd.read_csv(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name, sep='\t' )

        
        
        
        df_json = df.to_json(orient='values')
        
        
        
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
    
class LRLReportAjaxPathDetail(TemplateView):
    template_name = 'website/report_ajax_pathway_detail.html'
    
   
    
    def dispatch(self, request, *args, **kwargs):
        return super(LRLReportAjaxPathDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(LRLReportAjaxPathDetail, self).get_context_data(**kwargs)
        
        pathway = Pathway.objects.filter(organism='human', name=self.request.GET['pathway']).exclude(database='primary_old')[0]
        
        gene_data = []
        for gene in pathway.gene_set.all():
                nodes = ','.join([str(i) for i in Node.objects.filter(pathway=pathway, component__name=gene.name).distinct()])
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'Node(s)':nodes })   
           
        gene_df = pd.DataFrame(gene_data).set_index('SYMBOL')    
        
        filename = 'cnr_'+self.request.GET['filename']
        
        
        df_file_cnr = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+filename, index_col='SYMBOL')
        
        df_cnr_raw = df_file_cnr[[x for x in df_file_cnr.columns if 'Tumour' in x]]
        df_cnr_raw = df_cnr_raw.mean(axis=1).round(decimals=2)
        
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
    
    
class LRLReportAjaxPathLine(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LRLReportAjaxPathLine, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        path = request.GET.get('path')
        renderTo = request.GET.get('renderTo')
        
        if 're' in renderTo:
            file_name1_24 = 'output_Tumour_24h_10nmol_resveratrol.xlsx'
            file_name2_24 = 'output_Tumour_24h_50micromol_resveratrol.xlsx'
            file_name1_48 = 'output_Tumour_48h_10nmol_resveratrol.xlsx'
            file_name2_48 = 'output_Tumour_48h_50micromol_resveratrol.xlsx'
            s_name1 = '10 µM'
            s_name2 = '50 µM'           
        elif 'mh' in renderTo:
            file_name1_24 = 'output_Tumour_24h_2millimol_Metformin_hydrochloride.xlsx'
            file_name2_24 = 'output_Tumour_24h_4millimol_Metformin_hydrochloride.xlsx'
            file_name1_48 = 'output_Tumour_48h_2millimol_Metformin_hydrochloride.xlsx'
            file_name2_48 = 'output_Tumour_48h_4millimol_Metformin_hydrochloride.xlsx'
            s_name1 = '2 mM'
            s_name2 = '4 mM' 
        elif 'ca' in renderTo:
            file_name1_24 = 'output_Tumour_24h_5micromol_Capryloylsalicylic_acid.xlsx'
            file_name2_24 = 'output_Tumour_24h_10micromol_Capryloylsalicylic_acid.xlsx'
            file_name1_48 = 'output_Tumour_48h_5micromol_Capryloylsalicylic_acid.xlsx'
            file_name2_48 = 'output_Tumour_48h_10micromol_Capryloylsalicylic_acid.xlsx'
            s_name1 = '5 µM'
            s_name2 = '10 µM' 
        elif 'ra' in renderTo:
            file_name1_24 = 'output_Tumour_24h_1micromol_Retinoic_acid.xlsx'
            file_name2_24 = 'output_Tumour_24h_01micromol_Retinoic_acid.xlsx'
            file_name1_48 = 'output_Tumour_48h_1micromol_Retinoic_acid.xlsx'
            file_name2_48 = 'output_Tumour_48h_01micromol_Retinoic_acid.xlsx'
            s_name1 = '0.1 µM'
            s_name2 = '1 µM' 
        
        
        df1_24 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name1_24,
                                sheetname='PAS1', index_col='Pathway')
        name1_24 = [x for x in df1_24.columns if 'Tumour' in x][0]
        df2_24 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name2_24,
                                sheetname='PAS1', index_col='Pathway')
        name2_24 = [x for x in df2_24.columns if 'Tumour' in x][0]
        df1_48 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name1_48,
                                sheetname='PAS1', index_col='Pathway')
        name1_48 = [x for x in df1_48.columns if 'Tumour' in x][0]
        df2_48 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/lrl2016/"+file_name2_48,
                                sheetname='PAS1', index_col='Pathway')
        name2_48 = [x for x in df2_48.columns if 'Tumour' in x][0]
        
        val1_24 = df1_24.loc[path][name1_24].round(decimals=2)
        val2_24 = df2_24.loc[path][name2_24].round(decimals=2)
        val1_48 = df1_48.loc[path][name1_48].round(decimals=2)
        val2_48 = df2_48.loc[path][name2_48].round(decimals=2)
        
        
        l1 = [val1_24, val1_48]
        l2 = [val2_24, val2_48]
        
        series1 = {'name': s_name1,
                   'data': l1}
        series2 = {'name': s_name2,
                   'data': l2}
        
        response_data = {}
             

        response_data['s1'] = series1        
        response_data['s2'] = series2
        
        #
        return HttpResponse(json.dumps(response_data), content_type="application/json")       
    
    
    