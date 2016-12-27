# -*- coding: utf-8 -*-
import os

from django.db import models, transaction
from pandas import read_excel

from .utils import link_to_object


def get_document_upload_path(instance, file_name):
    return os.path.join('Pathway_images', file_name)


PATHWAY_DATABASE = (
    ('primary_old', 'Primary (old)'),
    ('primary_new', 'Primary (new)'),
    ('metabolism', 'Metabolism'),
    ('cytoskeleton', 'Cytoskeleton'),
    ('kegg', 'KEGG'),
    ('nci', 'NCI'),
    ('biocarta', 'Biocarta'),
    ('reactome', 'Reactome'),
    ('kegg_adjusted', 'KEGG Adjusted'),
    ('kegg_10', 'KEGG 10+ genes'),
    ('kegg_adjusted_10', 'KEGG Adjusted 10+ genes'),
    ('aging', 'Aging related'),
    ('sandbox', 'Sandbox'),
)

PATHWAY_DATABASE_DEFAULT = 'primary_new'

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
                                choices = PATHWAY_DATABASE, default=PATHWAY_DATABASE_DEFAULT)
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
        unique_together = (
            ('name', 'pathway'),
        )

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


RELATION_INHIBITOR = '0'
RELATION_ACTIVATOR = '1'
RELATION_UNKNOWN = '2'
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


def _pathway_name_for_file(file_obj):
    file_name = os.path.basename(file_obj.name)
    pathway_name = file_name.replace('.xls', '').replace(' ', '_')  # get pathname from filename
    return pathway_name


def import_pathway(file_obj, organism, database):
    with transaction.atomic():
        _import_pathway_unsafe(file_obj, organism, database)


def _import_pathway_unsafe(file_obj, organism, database):
    # try to load objects from file to fail early
    file_obj.seek(0)
    df_genes = read_excel(file_obj, sheetname='genes', header=None).fillna('missing')
    file_obj.seek(0)
    df_nodes = read_excel(file_obj, sheetname='nodes', header=None, index_col=0)
    file_obj.seek(0)
    df_node_names = read_excel(file_obj, sheetname='node_names', header=None, index_col=0)
    file_obj.seek(0)
    df_rels = read_excel(file_obj, sheetname='edges', header=None)

    # create new pathway
    pathname = _pathway_name_for_file(file_obj)
    if Pathway.objects.filter(name=pathname, organism=organism, database=database).exists():
        raise RuntimeError('Pathway "{}" already exists.'.format(pathname))

    new_path = Pathway(name=pathname, amcf=0, organism=organism, database=database)
    new_path.save()

    ##############################################################################
    # Add Genes
    ##############################################################################

    def add_gene(row, path):
        if row['arr'] != 'missing':
            g = Gene(name=row['gene'], arr=row['arr'], pathway=path)
            g.save()

    df_genes.columns = ['gene', 'arr']
    df_genes.apply(add_gene, axis=1, path=new_path)

    ##############################################################################
    # Add Nodes and Components. Update Node names
    ##############################################################################

    def add_node_and_components(row, path):
        node_name = row.name

        if Node.objects.filter(name=node_name, pathway=path).exists():
            raise RuntimeError('Node "{}" already exists for pathway "{}".'.format(node_name, path))

        new_node = Node(name=node_name, pathway=path)
        new_node.save()

        row = row[row != 1]
        row.dropna(inplace=True)  # taking into account different row lengths for different nodes
        for component in row:
            new_component = Component(name=component, node=new_node)
            new_component.save()

    df_nodes.drop(1, axis=1, inplace=True)
    df_nodes_name = df_nodes[2]

    # Node name = name of the first component in row
    # see file for more details

    df_nodes.apply(add_node_and_components, axis=1, path=new_path)

    # Update Node names

    # TODO: why do we need it?
    def update_node_name(row, path):
        name = row.name
        normal_name = row['new name']

        node = Node.objects.get(name=name, pathway=path)
        node.name = normal_name
        node.save()

    df_node_names.columns = ['new name']
    df_node_names.apply(update_node_name, axis=1, path=new_path)

    ##############################################################################
    # Add Relations
    ##############################################################################

    def add_relation(row, sNodes, path):
        from_node_name = row['from']
        to_node_name = row['to']

        if row['reltype'] == 'activation':
            reltype = RELATION_ACTIVATOR
        elif row['reltype'] == 'inhibition':
            reltype = RELATION_INHIBITOR
        else:
            reltype = RELATION_UNKNOWN  # to draw black arrows

        db_node_from = Node.objects.get(name=from_node_name, pathway=path)
        db_node_to = Node.objects.get(name=to_node_name, pathway=path)

        nrel = Relation(fromnode=db_node_from, tonode=db_node_to, reltype=reltype)
        nrel.save()

    df_rels.columns = ['from', 'to', 'reltype']
    df_rels.apply(add_relation, axis=1, sNodes=df_nodes_name, path=new_path)
