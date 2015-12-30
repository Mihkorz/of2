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


class IndexPage(TemplateView):
    template_name = 'website/index.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('profiles_index', slug=request.user.username)
        else:
            return super(IndexPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(IndexPage, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context
    
class AboutPage(TemplateView):
    template_name = 'website/about.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('profiles_index', slug=request.user.username)
        else:
            return super(AboutPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(AboutPage, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context
    
class LoginPage(TemplateView):
    template_name = "website/login.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LoginPage, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(LoginPage, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context

class Logout(TemplateView):
    template_name="website/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)    
        return redirect('website_index')
    
class LorealReport(TemplateView):
    template_name = "website/loreal_report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(LorealReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(LorealReport, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context

class ReportJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        file_name = request.GET.get('file_name')
        sample = request.GET.get('sample')
        sample_name = 'Tumour_'+sample+'.CEL'
        
        df_pas = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/"+file_name,
                                sheetname='PAS', index_col='Pathway')
        df_pas1 = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/"+file_name,
                                 sheetname='PAS1', index_col='Pathway')
        s_pas = df_pas[sample_name]
        s_pas.name = 'PAS'
        s_pas1 = df_pas1[sample_name]
        s_pas1.name = 'PAS1'
        db = df_pas['Database']
        
        joined = pd.concat([s_pas, s_pas1, db], axis=1)
        joined.reset_index(inplace=True)
        joined = joined[['Pathway', 'Database', 'PAS', 'PAS1']]
        joined_json = joined.to_json(orient='values')
        
        
        
        response_data = {'data': json.loads(joined_json)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl
import struct

def shiftedColorMap(cmap, start=0, midpoint=0, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
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
        
        pathway = Pathway.objects.get(organism='human', name=self.request.GET['pathway'], database=self.request.GET['db'])
        
        gene_data = []
        for gene in pathway.gene_set.all():
                nodes = ','.join([str(i) for i in Node.objects.filter(pathway=pathway, component__name=gene.name).distinct()])
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'Node(s)':nodes })   
           
        gene_df = pd.DataFrame(gene_data).set_index('SYMBOL')
            
        
        
        
        filename = 'cnr_'+self.request.GET['filename']
        sample = 'Tumour_'+self.request.GET['sample']+'.CEL'
        
        df_file_cnr = pd.read_excel(settings.MEDIA_ROOT+"/../static/report/"+filename, index_col='SYMBOL')
        df_cnr_raw = df_file_cnr[[sample]]
        df_cnr_differential = df_cnr_raw[df_cnr_raw[sample]!=1]
        df_cnr_differential.columns = ['CNR']
        
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

    
    
        
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    