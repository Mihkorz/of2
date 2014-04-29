import os

from django.db import models
from django.contrib.auth.models import User

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
            return "/media/images/noPicture.jpg"
    
    class Meta:
        ordering = ('user',)

PROJECT_PUBLIC = 1
PROJECT_PRIVATE = 2
PROJECT_STATUSES = (
    (PROJECT_PUBLIC, 'Public'),
    (PROJECT_PRIVATE, 'Private'),
)
        
class Project(models.Model):
    name = models.CharField(verbose_name="Project name", max_length=100, blank=False, unique=True,
                            help_text="This will be the name")
    owner = models.ForeignKey(User, related_name="owner")
    members =  models.ManyToManyField(User, related_name="members")
    description = models.TextField(verbose_name="Description(optional)", blank=True)
    status = models.IntegerField(choices = PROJECT_STATUSES, default=PROJECT_PUBLIC)
    created_at = models.DateTimeField(auto_now=True)
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
          
class Document(models.Model):
    document = models.FileField(upload_to=get_document_upload_path)
    doc_type = models.IntegerField(verbose_name="Document type", choices=DOC_TYPES, default=DOCUMENT_INPUT)
    structure = JSONField(verbose_name = "Document structure")
    description = models.TextField(verbose_name="Description", blank=True)
    parameters = JSONField(verbose_name="Calculation parameters", blank=True)
    sample_num = models.IntegerField(verbose_name="Sample ammount", blank=True, default=0)
    norm_num = models.IntegerField(verbose_name="Norm ammount", blank=True, default=0)
    row_num = models.IntegerField(verbose_name="Number of rows", blank=True, default=0)
    project = models.ForeignKey(Project)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='created_by')
    created_at = models.DateTimeField(auto_now=True)
    calculated_by = models.ForeignKey(User, blank=True, null=True, related_name='calculated_by')
    calculated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __unicode__(self):
        return self.document.name
    
    def get_filename(self):
        return os.path.basename(self.document.name)
    
class ProcessDocument(models.Model):
    document = models.FileField(upload_to=get_process_document_upload_path)
    parameters = JSONField(verbose_name="Calculation parameters", blank=True)
    input_doc = models.ForeignKey(Document, related_name="input_doc")
    output_doc = models.ForeignKey(Document, related_name="output_doc")
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='created')
    created_at = models.DateTimeField(auto_now=True)
    