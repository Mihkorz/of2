# -*- coding: utf-8 -*-

from django.db import models

from .utils import link_to_object


class Pathway(models.Model):
    name = models.CharField(verbose_name='Pathway name', max_length=250, blank=False, unique=True)
    amcf = models.DecimalField(verbose_name='AMCF', max_digits=2, decimal_places=1, default=0)
    info = models.TextField(verbose_name='Pathway information', blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    
    class Meta(object):
        db_table = 'pathway'
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Pathway, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
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
        db_table = 'gene'
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Gene, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
 
class Node(models.Model):
    name = models.CharField(verbose_name='Node name', max_length=250, blank=False)
    comment =  models.TextField(blank=True)
    pathway = models.ForeignKey(Pathway, blank=False)
    
    class Meta(object):
        db_table = 'node'
        ordering = ['pathway',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Node, self).clean()
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

class Component(models.Model):
    name = models.CharField(verbose_name='Component name', max_length=250, blank=False)
    comment =  models.TextField(blank=True)
    node = models.ForeignKey(Node, blank=False)
    
    def pathway(self):
        return self.node.pathway
    
    class Meta(object):
        db_table = 'component'
        ordering = ['node',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Component, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")

RELATION_INHIBITOR = 0
RELATION_ACTIVATOR = 1
RELATION_TYPES = (
    (RELATION_INHIBITOR, 'inhibition'),
    (RELATION_ACTIVATOR, 'activation'),
   
)
    
class Relation(models.Model):
    reltype = models.CharField(max_length=250, blank=False, choices=RELATION_TYPES, default=1)
    comment = models.TextField(blank=True)
    fromnode = models.ForeignKey(Node, related_name='outrelations', blank=False)
    tonode = models.ForeignKey(Node, related_name='inrelations', blank=False)
    
    class Meta(object):
        db_table = 'relation'
        
    def __unicode__(self):
        return '%s -> %s' %(self.fromnode, self.tonode)
    
    def pathway(self):
        return self.fromnode.pathway
    
DRUG_TYPES = (
    ('inhibitor', 'inhibitor'),
    ('activator', 'activator'),
    ('mab', 'mab'),
    ('killermab', 'killermab'),
    ('multivalent', 'multivalent'),
   
)
DRUG_DATABASE = (
    ('genego', 'genego'),
    ('drugbank', 'drugbank'),
)        
class Drug(models.Model):
    name = models.CharField(verbose_name='Drug name', max_length=250, blank=False)
    tip  = models.CharField(max_length=250, verbose_name=u'Drug type', blank=True, choices=DRUG_TYPES)
    db = models.CharField(max_length=250, verbose_name=u'Database', blank=True, choices = DRUG_DATABASE)
    substance = models.CharField(max_length=250, blank=True)
    targets = models.CharField(max_length=350, blank=True)
    morphology = models.CharField(max_length=250, blank=True)
    price = models.TextField(blank=True)
    sideEffect = models.TextField(blank=True)
    contraindication = models.TextField(blank=True)
    compatibility = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    isInRussia = models.BooleanField(default=True)
    info = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Drug, self).clean()
        self.name = self.name.strip(" \t")
    
    class Meta(object):
        db_table = 'drug'
        ordering = ['name',]

#_NOTFOUND = object()

TARGET_INHIBITOR = 0
TARGET_ACTIVATOR = 1
TARGET_TYPES = (
    (TARGET_INHIBITOR, 'inhibitor'),
    (TARGET_ACTIVATOR, 'activator'),
   
)

class Target(models.Model):
    name = models.CharField(verbose_name='Target name', max_length=250, blank=False)
    tip = models.IntegerField(choices = TARGET_TYPES, default=0)
    drug = models.ForeignKey(Drug)
    
    class Meta(object):
        db_table = 'target'
        ordering = ['drug',]
        
    def  __unicode__(self):
        return self.name
    
    def clean(self):
        super(Target, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
    


