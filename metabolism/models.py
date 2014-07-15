from django.db import models

from database.utils import link_to_object

class MetabolismPathway(models.Model):
    name = models.CharField(verbose_name='Pathway name', max_length=250, blank=False, unique=True)
    pathway_id = models.CharField(verbose_name='Pathway ID', max_length=30, blank=True)
    link_to_picture = models.CharField(verbose_name='Link to picture', max_length=250, blank=True)
    amcf = models.DecimalField(verbose_name='AMCF', max_digits=2, decimal_places=1, default=0)
    info = models.TextField(verbose_name='Pathway information', blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    
    class Meta(object):
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MetabolismPathway, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
    def gene_list(self):
        return link_to_object(self.gene_set.all())
    gene_list.allow_tags = True
    
class MetabolismGene(models.Model):
    name = models.CharField(verbose_name='Gene name', max_length=250, blank=False)
    arr = models.DecimalField(verbose_name='ARR', max_digits=2, decimal_places=1, default=0)
    comment = models.TextField(verbose_name='Comment', blank=True)
    pathway = models.ForeignKey(MetabolismPathway, blank=True, null=True)
    
    class Meta(object):
        ordering = ['name',]
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(MetabolismGene, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
