# -*- coding: utf-8 -*-
import os
import csv
import numpy as np
from pandas import read_csv, read_excel, DataFrame, Series
from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, norm as scipynorm
from sklearn.metrics import roc_auc_score
import itertools

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Pathway, Gene, Node, Component, Relation
from database.models import Pathway as oPath, Gene as oGene, Node as oNode, Component as oComp, Relation as oREl
from metabolism.models import MetabolismPathway
from mouse.models import MouseMetabolismPathway, MousePathway, MouseMapping
from .stats import fdr_corr

class Ksyusha(TemplateView):
    """
    Just Testing Playground
    """
    template_name = 'core/test.html'
    
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Ksyusha, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        context = super(Ksyusha, self).get_context_data(**kwargs)
        
        """
        res_df = read_csv(settings.MEDIA_ROOT+"/auc.csv")
        _, p_value = ttest_1samp(np.array(res_df['AUC']), 0.742342342342)
        raise Exception('permutation')
        """
        
        import scipy.stats as sstats
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)
        res_file = settings.MEDIA_ROOT+'/FilesForBCModule/GSE5462_GSE9574_normalized_responders.txt'
        res_df = read_csv(res_file, delimiter='\t',
                          index_col='SYMBOL') #create DataFrame for responders
        col = sstats.uniform.rvs(size = 100)#np.array(res_df.loc['A2M'])
        ax.hist(col, normed=True, histtype='stepfilled', alpha=0.2)
        ax.legend(loc='best', frameon=False)
        plt.show()
        
        haha = sstats.normaltest(col)
        raise Exception('plot')
        
        #0.742342342342 
        arttrue = [ 1,  1,  1,  1,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
        1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
        1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,
        0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]
        aaa=list(itertools.permutations([1,2,3]))
        #pppp=list(itertools.islice(, 10))
         
        
        
        """ reading responders and non-resonders files """
        res_file = settings.MEDIA_ROOT+'/FilesForBCModule/GSE5462_GSE9574_normalized_responders.txt'
        res_df = read_csv(res_file, delimiter='\t',
                          index_col='SYMBOL') #create DataFrame for responders
        res_df.drop([x for x in res_df.columns if 'Normal' in x], axis=1, inplace=True)
                
        nres_file = settings.MEDIA_ROOT+'/FilesForBCModule/GSE5462_GSE9574_normalized_nonresponders.txt'
        nres_df = read_csv(nres_file, delimiter='\t',
                           index_col='SYMBOL') #create DataFrame for non-responderss
        
        
        
        joined_df = df_for_pas1 = res_df.join(nres_df, how='inner') #merging 2 files together
        
        original_res_columns = [col for col in joined_df.columns if '_RES' in col]#store original column names
        len_o_r_c = len(original_res_columns)
        original_nres_columns = [col for col in joined_df.columns if '_NRES' in col]
        len_o_nr_c = len(original_nres_columns)
 
        
        norms_df = df_for_pas1[[norm for norm in [col for col in df_for_pas1.columns if 'Norm' in col]]]
        log_norms_df = np.log(norms_df)#use this for t-test, assuming log(norm) is distributed normally
        s_mean_norm = norms_df.apply(gmean, axis=1) #series of mean norms for CNR
        
        df_for_pas1.drop(norms_df.columns, axis=1, inplace=True)
        
        def apply_filter(col):
            _, p_value = ttest_1samp(log_norms_df, np.log(col), axis=1)
            s_p_value = Series(p_value, index = col.index).fillna(0)
            fdr_q_values = fdr_corr(np.array(s_p_value))
            col = col[(fdr_q_values<0.05)]
            return col
        
        df_for_pas1 = df_for_pas1.apply(apply_filter, axis=0).fillna(0)
        
        df_for_pas1 = df_for_pas1.divide(s_mean_norm, axis=0).fillna(0) #acquire CNR values
        df_for_pas1.replace(0, 1, inplace=True)
        df_for_pas1 = np.log(df_for_pas1) # now we have log(CNR)
        
        pas1_all_paths = DataFrame()
        marker_pathways = []
        dIterations = {}
        lAUC = [] 
        
        sample_names = []
        for col in df_for_pas1.columns:
            sample_names+=[{'Sample': col, 'group': 'NonResponders' },
                           {'Sample': col, 'group': 'Responders'}]
        df_probability = DataFrame(sample_names)
        
         
        """Start cycle """
        for pathway in Pathway.objects.filter(organism='human', database='primary_old').prefetch_related('gene_set'):
            ar_probabilities = np.array([])
            
                       
            
            genes = DataFrame(list(pathway.gene_set.all()
                                      .values('name', 'arr'))).set_index('name')#fetch genes 
            
            genes.index.name = 'SYMBOL'
           
            joined = genes.join(df_for_pas1, how='inner').drop(['arr'], axis=1) 
            pas1_for_pathway = joined.apply(lambda x: x*genes['arr'].astype('float')).sum()            
            pas1_for_pathway = pas1_for_pathway.set_value('Pathway', pathway.name)
            pas1_for_pathway = DataFrame(pas1_for_pathway).T.set_index('Pathway')
            
            pas1_all_paths = pas1_all_paths.append(pas1_for_pathway)
            
            """ AUC calculations and determining Marker paths """
            df_res = pas1_for_pathway[original_res_columns]
            df_nres = pas1_for_pathway[original_nres_columns]
            arScore = np.append(np.array(df_res.values, dtype='float64'), np.array(df_nres.values, dtype='float64'))            
            arRes = np.ones(len_o_r_c)
            arNRes = np.zeros(len_o_nr_c)
            arTrue = np.append(arRes, arNRes)
            
            if pathway.name == 'Caspase_Cascade_Activated_Tissue_Trans_glutaminase':
                AUC = roc_auc_score(arTrue, arScore) #calculate AUC
                raise Exception(AUC)
            
                for i in range(1000):
                    
                    np.random.shuffle(arTrue)
            
                    
                    lAUC.append(AUC)
            
                #if AUC>0.7:
                #    marker_pathways.append(pathway.name)
                    
                
                    
            
            
            #raise Exception('from within cycle')  
            
             
        #pas1_all_paths.to_csv(settings.MEDIA_ROOT+"/pas1.csv")
        dAUC = {}
        dAUC['AUC'] = lAUC
        df = DataFrame(dAUC)
        df.to_csv(settings.MEDIA_ROOT+"/auc.csv")
        raise Exception('ksyusha')
        
        return context

class ConvertPath(TemplateView):
    """
    Just Testing Playground
    """
    template_name = 'core/test.html'
    
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ConvertPath, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        context = super(ConvertPath, self).get_context_data(**kwargs)
        
        
                    
        raise Exception('just stop exception. Check view!')
        """
        #human metabolism
        for mpath in MetabolismPathway.objects.all():
            npath = Pathway(name=mpath.name, amcf=mpath.amcf, info=mpath.info, comment=mpath.comment,
                            organism='human', database='metabolism')
            npath.save()
            for mgene in mpath.metabolismgene_set.all():
                ngene = Gene(name=mgene.name, arr=mgene.arr, comment=mgene.comment, pathway=npath)
                ngene.save()
               
        #mouse metabolism
        for mpath in MouseMetabolismPathway.objects.all():
            npath = Pathway(name=mpath.name, amcf=mpath.amcf, info=mpath.info, comment=mpath.comment,
                            organism='mouse', database='metabolism')
            npath.save()
            for mgene in mpath.mousemetabolismgene_set.all():
                ngene = Gene(name=mgene.name, arr=mgene.arr, comment=mgene.comment, pathway=npath)
                ngene.save()
        """
        #human OLD
        """
        for opath in oPath.objects.all():
            try: 
                npath = Pathway.objects.get(name=opath.name, organism='human', database='primary_old')
            except:
                npath = Pathway(name=opath.name, amcf=opath.amcf, info=opath.info, comment=opath.comment,
                            organism='human', database='primary_old')
                #npath.save()
                for ogene in opath.gene_set.all():
                    ngene = Gene(name=ogene.name, arr=ogene.arr, comment=ogene.comment, pathway=npath)
                    #ngene.save()
              
            for onode in opath.node_set.all():
                nnode = Node(name=onode.name, comment=onode.comment, pathway=npath)
                nnode.save()
                for ocomp in onode.component_set.all():
                    ncomp = Component(name=ocomp.name, comment=ocomp.comment, node=nnode)
                    ncomp.save()
                    
            for onode in opath.node_set.all():
                for orel in onode.inrelations.all():
                    ofrom = orel.fromnode
                    oto = orel.tonode
                    
                    nfrom = Node.objects.get(name=ofrom.name, pathway=npath)
                    nto = Node.objects.get(name=oto.name, pathway=npath)
                    
                    nrel = Relation(fromnode=nfrom, tonode=nto, reltype=orel.reltype, comment=orel.comment)
                    nrel.save()
             
        """
        #mouse old
        """
        for mpath in MousePathway.objects.all():
            npath = Pathway(name=mpath.name, amcf=mpath.amcf, info=mpath.info, comment=mpath.comment,
                            organism='mouse', database='primary_old')
            npath.save()
            for mgene in mpath.mousegene_set.all():
                ngene = Gene(name=mgene.name, arr=mgene.arr, comment=mgene.comment, pathway=npath)
                ngene.save()
        """
        #mouse new
        """
        for hpath in Pathway.objects.filter(organism='human', database='primary_new'):
            try:
                npath = Pathway.objects.get(name=hpath.name, amcf=hpath.amcf, info=hpath.info, comment=hpath.comment,
                            organism='mouse', database='primary_new')
                
            except:
                npath = Pathway(name=hpath.name, amcf=hpath.amcf, info=hpath.info, comment=hpath.comment,
                            organism='mouse', database='primary_new')
                
                #npath.save()
                
            
            
            for hgene in hpath.gene_set.all():
                try:
                    mmap = MouseMapping.objects.filter(human_gene_symbol=hgene.name)[0]
                    ngene = Gene(name=mmap.mouse_gene_symbol.upper(), arr=hgene.arr, comment=hgene.comment, pathway=npath)
                    ngene.save()
                except:
                    pass
            
        
        """
        """ 
        #human new
        
        pathh = settings.MEDIA_ROOT+'/biocarta/'
        
        i=0
        for ffile in os.listdir(pathh):
            i=i+1
            print ffile+" n="+str(i) 
            df_genes = read_excel(pathh+ffile, sheetname='genes', header=None).fillna('mazafaka')
            df_genes.columns = ['gene', 'arr']
            
            pathname = ffile.replace('.xls', '').replace(' ', '_')
            try:
                npath = Pathway.objects.get(name=pathname, organism='human', database='biocarta' )               
            except:                 
            
                npath = Pathway(name=pathname, amcf=0, organism='human', database='biocarta')
                npath.save()
                
            def add_gene(row, path):
                if row['arr']!='mazafaka':
                    g = Gene(name=row['gene'], arr=row['arr'], pathway=path)
                    g.save()                
           
            df_genes.apply(add_gene, axis=1, path=npath)
            
            
            def nnodes(row, path):
                
                nname = row[2]
                try:
                    nnode = Node.objects.get(name=nname, pathway=path)
                except:
                    nnode = Node(name=nname, pathway=path)
                    nnode.save()
                
                row.dropna(inplace=True)
                for el in row:
                    mcomp = Component(name=el, node=nnode)
                    mcomp.save()
            
                #raise Exception('from nnodes')
        
            def rrels(row, sNodes, path):
                fff = row['from']
                ttt = row['to']
            
                namefrom = sNodes[fff]
                nameto = sNodes[ttt]#unknown activation inhibition
                reltype = 2
                if row['reltype']=='activation':
                    reltype = 1
                if row['reltype']=='inhibition':
                    reltype = 0
                if row['reltype']=='unknown':
                    reltype = 2
                    
                dbfrom = Node.objects.get(name=namefrom, pathway=path)
                dbto = Node.objects.get(name=nameto, pathway=path)
                
                nrel = Relation(fromnode=dbfrom, tonode=dbto, reltype=reltype)
                nrel.save()
                     
            
                #raise Exception('from rrel')
            try:
                df_nodes = read_excel(pathh+ffile, sheetname='nodes', header=None, index_col=0)
                df_nodes.drop(1, axis=1, inplace=True)
                df_nodes_name = df_nodes[2]
                #raise Exception('kegg')
                df_nodes.apply(nnodes, axis=1, path=npath)
            except:
                pass
            try:
                df_rels = read_excel(pathh+ffile, sheetname='edges', header=None)
                df_rels.columns = ['from', 'to', 'reltype']
                df_rels.apply(rrels, axis=1, sNodes=df_nodes_name, path=npath)    
            except:
                pass
         
        raise Exception('Biocarta Done')       
        """
        #cytoskeleton MOUSE pathways
        """
        for hpath in Pathway.objects.filter(organism='human', database='cytoskeleton'):
            try:
                npath = Pathway.objects.get(name=hpath.name, amcf=hpath.amcf, info=hpath.info, comment=hpath.comment,
                            organism='mouse', database='cytoskeleton')
                
            except:
                npath = Pathway(name=hpath.name, amcf=hpath.amcf, info=hpath.info, comment=hpath.comment,
                            organism='mouse', database='cytoskeleton')
                
                npath.save()
                
            
            
            for hgene in hpath.gene_set.all():
                try:
                    mmap = MouseMapping.objects.filter(human_gene_symbol=hgene.name)[0]
                    ngene = Gene(name=mmap.mouse_gene_symbol.upper(), arr=hgene.arr, comment=hgene.comment, pathway=npath)
                    ngene.save()
                except:
                    pass
        
        raise Exception('mouse') 
        """
        #cytoskeleton pathways 
        """
        def convertCytoskeleton(row):
            path = oPath.objects.using('old').get(name=row['old'])
            
            npath = Pathway.objects.get(name=row['new'], amcf=path.amcf, info=path.info, comment=path.comment,
                            organism='human', database='cytoskeleton')
            
            for onode in path.node_set.all():
                nnode = Node(name=onode.name, comment=onode.comment, pathway=npath)
                nnode.save()
                
                for ocomp in onode.component_set.all():
                    ncomp = Component(name=ocomp.name, comment=ocomp.comment, node=nnode)
                    ncomp.save()
            
            for onode in path.node_set.all():
                for orel in onode.inrelations.all():
                    ofrom = orel.fromnode
                    oto = orel.tonode
                    
                    nfrom = Node.objects.get(name=ofrom.name, pathway=npath)
                    nto = Node.objects.get(name=oto.name, pathway=npath)
                    
                    nrel = Relation(fromnode=nfrom, tonode=nto, reltype=orel.reltype, comment=orel.comment)
                    nrel.save()
            
            
            
            
            #raise Exception('from inside function')
        
        
        df_p_names = read_excel(settings.MEDIA_ROOT+'/cytoskeleton_new_pathways_renamed.xlsx',
                                sheetname='cytoskeleton_new_pathways', header=None)
        df_p_names.columns = ['old', 'new']
        
        df_p_names.apply(convertCytoskeleton, axis=1)
        
        raise Exception('utils exp')
        
        """    
            
        """ COUNT DISTINCT GENES  
        lhuman =[]
        lmouse = []
        
        for pp in Pathway.objects.filter(organism='human'):
            for gg in pp.gene_set.all():
                lhuman.append(gg.name)
        
        for ppp in Pathway.objects.filter(organism='mouse'):
            for ggg in ppp.gene_set.all():
                lmouse.append(ggg.name)
        
        numhuman = len(set(lhuman))
        nummouse = len(set(lmouse))
        raise Exception('count') 
        """  
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        
        return context