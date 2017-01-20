# -*- coding: utf-8 -*-
import os
import itertools


from django.db import models

REPORT_TEMPLATE = (
    ('Original', 'Original'),
    ('S1Report', 'S1Report'),
    ('S2Report', 'S2Report'),
    ('S3Report', 'S3Report'),
    ('Extended', 'Extended')
)

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
    
    report_template = models.CharField(verbose_name=u'Report template', max_length=15, blank=False,
                                choices = REPORT_TEMPLATE, default='Original') 
    
    header_data_text = models.TextField(verbose_name='Text for the beginning of the report', blank=True)
    input_data_text = models.TextField(verbose_name='Text for Input Data section', blank=True)
    methods_text = models.TextField(verbose_name='Text for Methods section', blank=True)
    gene_text = models.TextField(verbose_name='Text for Gene Level Analysis section', blank=True)
    sim_text = models.TextField(verbose_name='Text for Similarity Analysis section', blank=True)
    path_text = models.TextField(verbose_name='Text for Pathway Level Analysis section', blank=True)
    corr_text = models.TextField(verbose_name='Text for Public domain section', blank=True)
    targets_text = models.TextField(verbose_name='Text for Potential Targets section', blank=True)
    tf_text = models.TextField(verbose_name='Text for Transcriptional factor section', blank=True)
    kinetic_text = models.TextField(verbose_name='Text for Kinetic pathway modeling section', blank=True)
    conclusion_text = models.TextField(verbose_name='Text for Conclusion section', blank=True)
    references_text = models.TextField(verbose_name='Text for References section', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    """ Gene level """
    pval_theshold_plot = models.FloatField(verbose_name='p-val plot', help_text='Treshold in volcano and scatter plots',
                                           blank=False, default=0.05)
    logcf_theshold_plot = models.FloatField(verbose_name='|logFC| plot', help_text='Treshold in volcano and scatter plots', 
                                            blank=False, default=0.2)
    
    pval_theshold_compare = models.FloatField(verbose_name='p-val comparison', help_text='Treshold in Gene level Comparison',
                                           blank=False, default=0.05)
    logcf_theshold_compare = models.FloatField(verbose_name='|logFC| comparison', help_text='Treshold in Gene level Comparison', 
                                            blank=False, default=0.2)
    
    pas_theshold = models.FloatField(verbose_name='|PAS| comparison', help_text='Treshold in Pathway level Comparison', 
                                            blank=False, default=0)
    
    notable_genes = models.CharField(help_text='List of notable genes, separated by comma', max_length=250, blank=True)
    
    norm_name = models.CharField(verbose_name='Normal title', max_length=250, blank=False)
    
    
    compare_groups = models.TextField(verbose_name='Comparison groups', blank=True, null=True,
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
        #lgroups = [self.norm_name]
        lgroups =[]
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
    
    
    def get_all_gene_groups_as_list(self):
        lgroups = []
        for group in self.genegroup_set.all():
                lgroups.append(group.name.split('vs')[0])
        
        return lgroups
    
    def get_all_gene_groups_norm_as_list(self):
        #lgroups = [self.norm_name]
        lgroups = []
        for group in self.genegroup_set.all():
                lgroups.append(group.name.split('vs')[0])
        
        return lgroups
    
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
                combinations= list(itertools.combinations(group_list, 4)) # get all triplets of items
        
            else:            
                combinations= list(itertools.combinations(group_list, 3)) # get all pairs of items
        
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
                combinations= list(itertools.combinations(group_list, 4)) # get all triplets of items
        
            else:            
                combinations= list(itertools.combinations(group_list, 3)) # get all pairs of items
        
            l_combination_names = []
            for tlong in combinations:
                lname =[]            
                for tshort in tlong:
                    lname.append(tshort[0])
                l_combination_names.append("vs".join(lname))
        else:
            l_combination_names = [x.strip() for x in self.compare_groups.split(',')]
        
        return l_combination_names
    
    def count_ds_groups(self):
        return self.drugscoregroup_set.all().count()
    
    

def get_document_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, file_name)
def get_doclogfc_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, 'logfc', 'logfc_'+instance.name+'.csv')#file_name)
def get_docboxplot_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, 'boxplot', file_name)

class GeneGroup(models.Model):
    name = models.CharField(verbose_name='Gene group name', max_length=250, blank=False)
    document = models.FileField(verbose_name='Gene expression', upload_to=get_document_upload_path, max_length=300,
                                help_text='CSV file with columns: SYMBOL, Tumour, Normal')
    doc_logfc =  models.FileField(verbose_name='LogFC and p-val', upload_to=get_doclogfc_upload_path, max_length=300, blank=True)
    doc_boxplot = models.FileField(upload_to=get_docboxplot_upload_path, max_length=300, blank=True)
    
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')
    
    def henkel_norm_name(self):
        return self.name.replace('w', '')

class PathwayGroup(models.Model):
    name = models.CharField(verbose_name='Pathway group name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='OncoFinder2 output file')
    doc_proc =  models.FileField(upload_to=get_document_upload_path, max_length=300, blank=True)
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')

class TfGroup(models.Model):
    name = models.CharField(verbose_name='Transcription Factor group name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='Transcription Factor file')
    trrust = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='Trrust file', blank=True, null=True)
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')
    
class DeepLearning(models.Model):
    name = models.CharField(verbose_name='Deep learning name', max_length=250, blank=False)
    farmclass = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='Farm classes file')
    sideeff = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='Side Effects file', blank=True)
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')
    
class CorrelationGroup(models.Model):
    name = models.CharField(verbose_name='Correlation group name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='Correlation file')
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')
    
class DrugScoreGroup(models.Model):
    name = models.CharField(verbose_name='Drug Scoring name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='Drug Scoring file')
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')   