# -*- coding: utf-8 -*-
import os

from django.db import models

class Report(models.Model):
    """ Text data """
    title = models.CharField(verbose_name='Report title', max_length=250, blank=False)
    title_short = models.CharField(verbose_name='Short title', max_length=250, blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=50, blank=False,
                             help_text='url for /report-portal/report/%url%/')    
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
    
    class Meta(object):
        ordering = ['created_at',]

def get_document_upload_path(instance, file_name):
    return os.path.join('report-portal', instance.report.slug, file_name)


class GeneGroup(models.Model):
    name = models.CharField(verbose_name='Gene group name', max_length=250, blank=False)
    document = models.FileField(upload_to=get_document_upload_path, max_length=300,
                                help_text='CSV file with columns: SYMBOL, logFC, adj.P.Val')
    report = models.ForeignKey(Report)
    
    def get_slug(self):
        return self.name.replace(' ', '_')
    