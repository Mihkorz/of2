import os

from django.db import models
from django.contrib.auth.models import User
from medic.models import Nosology

from jsonfield.fields import JSONField


def get_profile_image_path(instance, filename):
    return os.path.join('users', str(instance.user.username), 'avatar', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    picture = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True, 
                                verbose_name = 'Profile picture')
    url = models.CharField(verbose_name = 'URL',  max_length = 100, blank=True)
    company = models.CharField(verbose_name = 'Company',  max_length = 100, blank=True)
    location = models.CharField(verbose_name = 'Location',  max_length = 100, blank=True)
    
    def get_picture(self):
        if self.picture:
            return "/media/"+str(self.picture)
        else:
            return "/static/images/noPicture.jpg"
    
    class Meta:
        ordering = ('user',)

PROJECT_PUBLIC = 1
PROJECT_PRIVATE = 2
PROJECT_STATUSES = (
    (PROJECT_PUBLIC, 'Public'),
    (PROJECT_PRIVATE, 'Private'),
)

PROJECT_FIELDS = (
    ('sci', 'Scientific'),
    ('rna', 'miRNA'),
    ('med', 'Medical'),
    
)
        
class Project(models.Model):
    name = models.CharField(verbose_name="Project name", max_length=100, blank=False, unique=True,
                            help_text="This will be the name")
    owner = models.ForeignKey(User, related_name="owner")
    members =  models.ManyToManyField(User, related_name="members")
    description = models.TextField(verbose_name="Description(optional)", blank=True)
    status = models.IntegerField(choices = PROJECT_STATUSES, default=PROJECT_PUBLIC)
    field = models.CharField(verbose_name="Project type", max_length=3, choices = PROJECT_FIELDS, default='sci')
    nosology = models.ForeignKey(Nosology, verbose_name="Cancer type", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(verbose_name="Last viewed at", blank=True, null=True,)
    viewed_by = models.ForeignKey(User, blank=True, null=True, related_name='viewed')
    
    class Meta:
        ordering = ('-created_at',)
        
    def __unicode__(self):
        return self.name
    
    def clean(self):
        super(Project, self).clean()
        self.name = self.name.strip(" \t").replace(" ", "-")
    
    def get_documents_number(self):
        return self.document_set.count()


def get_document_upload_path(instance, file_name):
    return os.path.join('users', str(instance.created_by.username), instance.project.name ,'input', file_name)

def get_process_document_upload_path(instance, file_name):
    return os.path.join('users', str(instance.created_by.username), instance.project.name ,'process', file_name)

DOCUMENT_INPUT = 1
DOCUMENT_OUTPUT = 2
DOC_TYPES = (
    (DOCUMENT_INPUT, 'input'),
    (DOCUMENT_OUTPUT, 'output'),
)

DOC_FORMATS = (
    ('OF_gene', 'OncoFinder gene expression file'),
    ('OF_cnr', 'OncoFinder CNR file'),
    ('OF_cnr_stat', 'OncoFinder CNR file with statistics (p-value and q-value)'),
    ('Illumina', 'Illumina file (with marked Tumour and Normal columns)'),
    ('CustomArray', 'CustomArray file'),
)
          
class Document(models.Model):
    document = models.FileField(upload_to=get_document_upload_path, max_length=300)
    doc_type = models.IntegerField(verbose_name="Document type", choices=DOC_TYPES, 
                                   default=DOCUMENT_INPUT)
    doc_format = models.CharField(verbose_name="Document format", max_length=100, 
                                  choices=DOC_FORMATS, blank=True, default='')
    structure = JSONField(verbose_name = "Document structure")
    description = models.TextField(verbose_name="Description", blank=True)
    parameters = JSONField(verbose_name="Calculation parameters", blank=True)
    sample_num = models.IntegerField(verbose_name="Sample ammount", blank=True, default=0)
    norm_num = models.IntegerField(verbose_name="Norm ammount", blank=True, default=0)
    row_num = models.IntegerField(verbose_name="Number of rows", blank=True, default=0)
    project = models.ForeignKey(Project)
    related_doc = models.ForeignKey('self', related_name="process_doc", blank=True, null=True, default=None)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    calculated_by = models.ForeignKey(User, blank=True, null=True, related_name='calculated_by')
    calculated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __unicode__(self):
        return self.document.name
    
    def get_filename(self):
        return os.path.basename(self.document.name)
    
class ProcessDocument(models.Model):
    document = models.FileField(upload_to=get_process_document_upload_path, max_length=300)
    parameters = JSONField(verbose_name="Calculation parameters", blank=True)
    input_doc = models.OneToOneField(Document, related_name="input_doc", blank=True, null=True)
    output_doc = models.ForeignKey(Document, related_name="output_doc", blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='created')
    created_at = models.DateTimeField(auto_now_add=True)

def get_shambala_document_upload_path(instance, file_name):
    return os.path.join('Shambala', str(instance.created_by.username), file_name)

AUXILIARY_CHOICES = (('illumina', 'Illumina'),
                         ('customar', 'CustomArray'),
                         ('test', 'test'))

class ShambalaDocument(models.Model):
    document = models.FileField(upload_to=get_shambala_document_upload_path, max_length=300)
    doc_type = models.IntegerField(verbose_name="Document type", choices=DOC_TYPES, 
                                   default=DOCUMENT_INPUT)
    auxiliary = models.CharField(verbose_name="Auxiliary (calibration) dataset", max_length=100, 
                                  choices=AUXILIARY_CHOICES, blank=False, default='illumina')
    log_scale = models.BooleanField(verbose_name="Apply logarithm", default=True, blank=False)
    sample_num = models.IntegerField(verbose_name="Sample ammount", blank=True, default=0)
    row_num = models.IntegerField(verbose_name="Number of rows", blank=True, default=0)
    related_doc = models.ForeignKey('self', related_name="bound_doc", blank=True, null=True, default=None)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='shambala_doc')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.document.name
    
    def get_filename(self):
        return os.path.basename(self.document.name)
    

class IlluminaProbeTarget(models.Model):
    PROBE_ID = models.CharField(max_length=250, db_index=True, verbose_name=u'Probe ID', blank=False)
    TargetID = models.CharField(max_length=250, verbose_name=u'Target ID', blank=False)
    PROBE_SEQUENCE = models.CharField(max_length=250, verbose_name=u'Probe Sequance')    