# -*- coding: utf-8 -*-

from django.db import models

from .utils import link_to_object


class MouseMapping(models.Model):
    human_gene_symbol = models.CharField(verbose_name='Human gene symbol ', max_length=250, blank=False)
    mouse_gene_symbol = models.CharField(verbose_name='Mouse gene symbol ', max_length=250, blank=False)

class MousePathway(models.Model):
    name = models.CharField(verbose_name='Pathway name', max_length=250, blank=False, unique=True)
    amcf = models.DecimalField(verbose_name='AMCF', max_digits=2, decimal_places=1, default=0)
    info = models.TextField(verbose_name='Pathway information', blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    
    class Meta(object):
        
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MousePathway, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
    def gene_list(self):
        return link_to_object(self.mousegene_set.all())
    gene_list.allow_tags = True
    
    def node_list(self):
        return link_to_object(self.node_set.all())
    node_list.allow_tags = True
    
class MouseGene(models.Model):
    name = models.CharField(verbose_name='Gene name', max_length=250, blank=False)
    arr = models.DecimalField(verbose_name='ARR', max_digits=2, decimal_places=1, default=0)
    comment = models.TextField(verbose_name='Comment', blank=True)
    pathway = models.ForeignKey(MousePathway, blank=False)
    
    class Meta(object):
        
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MouseGene, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
 
class MouseNode(models.Model):
    name = models.CharField(verbose_name='Node name', max_length=250, blank=False)
    comment =  models.TextField(blank=True)
    pathway = models.ForeignKey(MousePathway, blank=False)
    
    class Meta(object):
       
        ordering = ['pathway',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MouseNode, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
    def component_list(self):
        return link_to_object(self.component_set.all())
    component_list.allow_tags = True
    
    def in_rel(self):
        return link_to_object(self.inrelations.all())
    in_rel.allow_tags = True
    def out_rel(self):
        return link_to_object(self.outrelations.all())
    out_rel.allow_tags = True

class MouseComponent(models.Model):
    name = models.CharField(verbose_name='Component name', max_length=250, blank=False)
    comment =  models.TextField(blank=True)
    node = models.ForeignKey(MouseNode, blank=False)
    
    def pathway(self):
        return self.node.pathway
    
    class Meta(object):
       
        ordering = ['node',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MouseComponent, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")

RELATION_INHIBITOR = 0
RELATION_ACTIVATOR = 1
RELATION_TYPES = (
    (RELATION_INHIBITOR, 'inhibition'),
    (RELATION_ACTIVATOR, 'activation'),
   
)
    
class MouseRelation(models.Model):
    reltype = models.CharField(max_length=250, blank=False, choices=RELATION_TYPES, default=1)
    comment = models.TextField(blank=True)
    fromnode = models.ForeignKey(MouseNode, related_name='outrelations', blank=False)
    tonode = models.ForeignKey(MouseNode, related_name='inrelations', blank=False)
    

        
    def __unicode__(self):
        return '%s -> %s' %(self.fromnode, self.tonode)
    
    def pathway(self):
        return self.fromnode.pathway
    
class MouseMetabolismPathway(models.Model):
    name = models.CharField(verbose_name='Pathway name', max_length=250, blank=False, unique=True)
    amcf = models.DecimalField(verbose_name='AMCF', max_digits=2, decimal_places=1, default=0)
    info = models.TextField(verbose_name='Pathway information', blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    
    class Meta(object):
        
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MouseMetabolismPathway, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
    def gene_list(self):
        return link_to_object(self.mousemetabolismgene_set.all())
    gene_list.allow_tags = True
    
    
class MouseMetabolismGene(models.Model):
    name = models.CharField(verbose_name='Gene name', max_length=250, blank=False)
    arr = models.DecimalField(verbose_name='ARR', max_digits=2, decimal_places=1, default=0)
    comment = models.TextField(verbose_name='Comment', blank=True)
    pathway = models.ForeignKey(MouseMetabolismPathway, blank=False)
    
    class Meta(object):
        
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MouseMetabolismGene, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")