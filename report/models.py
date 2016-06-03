# -*- coding: utf-8 -*-
import os
import itertools


from django.db import models

PATHWAY_ORGANISM = (
    ('human', 'Human'),
    ('mouse', 'Mouse'),
)

GENE_PLOT = (
    ('vulcano', 'Vulcano Plot'),
    ('scatter', 'Scatter Plot'),
)  

class Report(models.Model):
    """ Text data """
    title = models.CharField(verbose_name='Report title', max_length=250, blank=False)
    title_short = models.CharField(verbose_name='Short title', max_length=250, blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=50, blank=False,
                             help_text='url for /report-portal/report/%url%/')    
    organism = models.CharField(verbose_name=u'Organism', max_length=5, blank=False,
                                choices = PATHWAY_ORGANISM, default='human') 
    organization = models.CharField(max_length=250, blank=True)
    input_data_text = models.TextField(verbose_name='Text for Input Data section', blank=True)
    methods_text = models.TextField(verbose_name='Text for Methods section', blank=True)
    gene_text = models.TextField(verbose_name='Text for Gene Level Analysis section', blank=True)
    path_text = models.TextField(verbose_name='Text for Pathway Level Analysis section', blank=True)
    conclusion_text = models.TextField(verbose_name='Text for Conclusion section', blank=True)
    references_text = models.TextField(verbose_name='Text for References section', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    """ Gene level """
    notable_genes = models.CharField(help_text='List of notable genes, separated by comma', max_length=250, blank=True)
    
    norm_name = models.CharField(verbose_name='Normal title', max_length=250, blank=False)
    
    
    compare_groups = models.CharField(verbose_name='Comparison groups', max_length=250, blank=True, null=True,
                                      help_text="""List of group names separated by "vs". 
                                      If several groups are required separate them by comma (G1vsG2vsG3, G4vsG5vsG6).  
                                      Leave empty for permutations of all groups""") 
    gene_plot = models.CharField(verbose_name=u'Gene plot type', max_length=15, blank=False,
                                choices = GENE_PLOT, default='vulcano') 
    
    class Meta(object):
        ordering = ['created_at',]
        
    def get_notable_genes_list(self):
        return [x.strip() for x in self.notable_genes.split(',')]
    
    
    
    def get_gene_groups(self):
        lgroups = [self.norm_name]
        if not self.compare_groups:
            for group in self.genegroup_set.all():
                lgroups.append(group.name.split('vs')[0])
            joined = ','.join(lgroups)
        else:
            l_combination_names = [x.strip() for x in self.compare_groups.split(',')]
            l_names = []
            for com in l_combination_names:
                l_names+=com.split('vs')
            l_names = list(set(l_names))
            joined = lgroups+l_names  # delete duplicates
            
        return joined
    
    def get_gene_groups_as_list(self):
        if not self.compare_groups:
            return self.get_gene_groups().split(',')
        else:
            return self.get_gene_groups()
    
    def get_gene_permutations(self):
        group_num = self.genegroup_set.all().count()
        group_list = self.genegroup_set.all().values_list('name')
        
        if not self.compare_groups:
            if group_num>3:
                combinations= list(itertools.combinations(group_list, 3)) # get all triplets of items
        
            else:            
                combinations= list(itertools.combinations(group_list, 2)) # get all pairs of items
        
            l_combination_names = []
            for tlong in combinations:
                lname =[]            
                for tshort in tlong:
                    lname.append(tshort[0])
                l_combination_names.append("vs".join(lname))
        else:
            l_combination_names = [x.strip() for x in self.compare_groups.split(',')]
        
        return l_combination_names
    
    def get_path_permutations(self):
        group_num = self.pathwaygroup_set.all().count()
        group_list = self.pathwaygroup_set.all().values_list('name')
        
        if not self.compare_groups:
            if group_num>3:
                combinations= list(itertools.combinations(group_list, 3)) # get all triplets of items
        
            else:            
                combinations= list(itertools.combinations(group_list, 2)) # get all pairs of items
        
            l_combination_names = []
            for tlong in combinations:
                lname =[]            
                for tshort in tlong:
                    lname.append(tshort[0])
                l_combination_names.append("vs".join(lname))
        else:
            l_combination_names = [x.strip() for x in self.compare_groups.split(',')]
        
        return l_combination_names
    
    

def get_document_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, file_name)
def get_doclogfc_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, 'logfc', file_name)
def get_docboxplot_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, 'boxplot', file_name)

class GeneGroup(models.Model):
    name = models.CharField(verbose_name='Gene group name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='CSV file with columns: SYMBOL, Tumour, Normal')
    doc_logfc =  models.FileField(upload_to=get_doclogfc_upload_path, max_length=300, blank=True)
    doc_boxplot = models.FileField(upload_to=get_docboxplot_upload_path, max_length=300, blank=True)
    
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')

class PathwayGroup(models.Model):
    name = models.CharField(verbose_name='Pathway group name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='OncoFinder2 output file')
    doc_proc =  models.FileField(upload_to=get_document_upload_path, max_length=300, blank=True)
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')
    
    