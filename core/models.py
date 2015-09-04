# -*- coding: utf-8 -*-
import os

from django.db import models

from .utils import link_to_object

def get_document_upload_path(instance, file_name):
    return os.path.join('Pathway_images', file_name)


PATHWAY_DATABASE = (
    ('primary_old', 'Primary Pathway Database (old)'),
    ('primary_new', 'Primary Pathway Database (new)'),
    ('metabolism', 'Metabolism Pathway Database'),
    ('cytoskeleton', 'Cytoskeleton Pathway Database'),
    ('kegg', 'KEGG Pathway Database'),
    ('nci', 'NCI Pathway Database'),
    ('kegg_adjusted', 'KEGG Adjusted Pathway Database'),
    ('kegg_10', 'KEGG 10'),
    ('kegg_adjusted_10', 'KEGG Adjusted 10'), 
) 

PATHWAY_ORGANISM = (
    ('human', 'Human'),
    ('mouse', 'Mouse'),
) 

class Pathway(models.Model):
    pathway_id = models.CharField(verbose_name='ID', max_length=30, blank=True)
    name = models.CharField(verbose_name='Pathway name', max_length=250, blank=False)
    organism = models.CharField(verbose_name=u'Organism', max_length=5, blank=False,
                                choices = PATHWAY_ORGANISM, default='human')
    database = models.CharField(verbose_name=u'Database', max_length=20, blank=False,
                                choices = PATHWAY_DATABASE, default='primary_old')
    amcf = models.DecimalField(verbose_name='AMCF', max_digits=2, decimal_places=1, default=0)
    info = models.TextField(verbose_name='Pathway information', blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    image = models.ImageField(verbose_name="Picture", 
                              upload_to=get_document_upload_path, max_length=350,
                              blank=True, null=True)
    
    class Meta(object):
        ordering = ['name',]
        unique_together = ('name', 'database', 'organism')
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Pathway, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "_")
    
    def gene_list(self):
        return link_to_object(self.gene_set.all())
    gene_list.allow_tags = True
    
    def node_list(self):
        return link_to_object(self.node_set.all())
    node_list.allow_tags = True


class Gene(models.Model):
    name = models.CharField(verbose_name='Gene name', max_length=250, blank=False)
    arr = models.DecimalField(verbose_name='ARR', max_digits=2, decimal_places=1, default=0)
    comment = models.TextField(verbose_name='Comment', blank=True)
    pathway = models.ForeignKey(Pathway, blank=False)
    
    class Meta(object):
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Gene, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "_")
 
class Node(models.Model):
    name = models.CharField(verbose_name='Node name', max_length=250, blank=False)
    comment =  models.TextField(blank=True)
    pathway = models.ForeignKey(Pathway, blank=False)
    
    class Meta(object):
        ordering = ['pathway',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Node, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "_")
    
    def component_list(self):
        return link_to_object(self.component_set.all())
    component_list.allow_tags = True
    
    def in_rel(self):
        return link_to_object(self.inrelations.all())
    in_rel.allow_tags = True
    def out_rel(self):
        return link_to_object(self.outrelations.all())
    out_rel.allow_tags = True

class Component(models.Model):
    name = models.CharField(verbose_name='Component name', max_length=250, blank=False)
    comment =  models.TextField(blank=True)
    node = models.ForeignKey(Node, blank=False)
    
    def pathway(self):
        return self.node.pathway
    
    class Meta(object):
        ordering = ['node',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Component, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "_")
        
RELATION_INHIBITOR = 0
RELATION_ACTIVATOR = 1
RELATION_UNKNOWN = 2
RELATION_TYPES = (
    (RELATION_INHIBITOR, 'inhibition'),
    (RELATION_ACTIVATOR, 'activation'),
    (RELATION_UNKNOWN, 'unknown'),
   
)
    
class Relation(models.Model):
    reltype = models.CharField(max_length=250, blank=False, choices=RELATION_TYPES, default=1)
    comment = models.TextField(blank=True)
    fromnode = models.ForeignKey(Node, related_name='outrelations', blank=False)
    tonode = models.ForeignKey(Node, related_name='inrelations', blank=False)
    
    class Meta(object):
        pass
        
    def __unicode__(self):
        return '%s -> %s' %(self.fromnode, self.tonode)
    
    def pathway(self):
        return self.fromnode.pathway