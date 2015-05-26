# -*- coding: utf-8 -*-
import os
from pandas import read_excel

from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Pathway, Gene, Node, Component, Relation
from database.models import Pathway as oPath, Gene as oGene, Node as oNode, Component as oComp, Relation as oREl
from metabolism.models import MetabolismPathway
from mouse.models import MouseMetabolismPathway, MousePathway, MouseMapping

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
        #raise Exception('just stop exception. Check view!')
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
           
        #human new
        """
        pathh = settings.MEDIA_ROOT+'/microPaths/'
        
        
        for ffile in os.listdir(pathh):
            df_genes = read_excel(pathh+ffile, sheetname='genes', header=None).fillna('mazafaka')
            df_genes.columns = ['gene', 'arr']
            
            pathname = ffile.replace('.xls', '')
            try:
                npath = Pathway.objects.get(name=pathname, organism='human', database='primary_new' )               
            except:                 
            
                npath = Pathway(name=pathname, amcf=0, organism='human', database='primary_new')
                #path.save()
                
            def add_gene(row, path):
                if row['arr']!='mazafaka':
                    g = Gene(name=row['gene'], arr=row['arr'], pathway=path)
                    g.save()                
            
            #df_genes.apply(add_gene, axis=1, path=path)
            def nnodes(row, path):
                
                nname = row[1]
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
            
            df_nodes = read_excel(pathh+ffile, sheetname='nodes', header=None, index_col=0)
            df_nodes_name = df_nodes[1]
            df_nodes.apply(nnodes, axis=1, path=npath)
            
            df_rels = read_excel(pathh+ffile, sheetname='edges', header=None)
            df_rels.columns = ['from', 'to', 'reltype']
            df_rels.apply(rrels, axis=1, sNodes=df_nodes_name, path=npath)    
            
            
            #raise Exception('human new')       
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