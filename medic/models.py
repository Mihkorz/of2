import os

from django.db import models

class Nosology(models.Model):
    name = models.CharField(verbose_name="Nosology", max_length=250, blank=False, unique=True)
    
    class Meta:
        ordering = ('name',)
        
    def __unicode__(self):
        return self.name


def get_document_upload_path(instance, file_name):
    return os.path.join('medic', instance.nosology.name, instance.name, file_name)
    
class TreatmentMethod(models.Model):
    name = models.CharField(verbose_name="Name", max_length=250, blank=False, unique=True)
    nosology = models.ForeignKey(Nosology, blank=False, related_name='treatment')
    file_pms1 = models.FileField(upload_to=get_document_upload_path, max_length=350)
    file_probability = models.FileField(upload_to=get_document_upload_path, max_length=350)
    
    class Meta:
        ordering = ('nosology',)
        
    def __unicode__(self):
        return self.name
