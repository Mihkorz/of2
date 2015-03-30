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
    num_of_patients = models.IntegerField(verbose_name='Number of patients', blank=True, null=True)
    histological_type = models.TextField(verbose_name="Histological type",  blank=True) 
    grade = models.CharField(verbose_name="Grade", max_length=250, blank=True)
    hormone_receptor_status = models.CharField(verbose_name="Hormone receptor status",
                                                max_length=250, blank=True)
    her2_status = models.CharField(verbose_name="HER2 status", max_length=250, blank=True)
    stage =  models.CharField(verbose_name="Stage status", max_length=250, blank=True)
    treatment = models.TextField(verbose_name="Treatment",  blank=True)
    citation = models.TextField(verbose_name="Citation(s)",  blank=True)
    organization_name =  models.CharField(verbose_name="Organization name", 
                                          max_length=250, blank=True)
    file_pms1 = models.FileField(verbose_name="PAS1 file", 
                                 upload_to=get_document_upload_path, max_length=350,
                                 blank=True, null=True)
    file_probability = models.FileField(verbose_name="Probability file", 
                                        upload_to=get_document_upload_path, max_length=350,
                                        blank=True, null=True)
    accuracy = models.FloatField(verbose_name="Accuracy",  blank=True, null=True)
    percentage_response = models.FloatField(verbose_name="Percentage of patients achieving response",
                                            blank=True, null=True)
    ref_clinical_trial = models.TextField(verbose_name="Reference for the clinical trial", 
                                          blank=True)
    
    file_res = models.FileField(verbose_name="Responders file",
                                upload_to=get_document_upload_path, max_length=350)
    file_nres = models.FileField(verbose_name="Non-responders file",
                                 upload_to=get_document_upload_path, max_length=350)
    
    
    class Meta:
        ordering = ('nosology',)
        
    def __unicode__(self):
        return self.name


#NORMS
def get_norms_upload_path(instance, file_name):
    return os.path.join('medic', instance.nosology.name, 'norms', instance.name, file_name)

class TreatmentNorms(models.Model):
    name = models.CharField(verbose_name="Name", max_length=250, blank=False, unique=True)
    nosology = models.ForeignKey(Nosology, blank=False, related_name='norms')
    num_of_norms = models.IntegerField(verbose_name='Number of norms', blank=True, null=True)
    file_norms = models.FileField(upload_to=get_document_upload_path, max_length=350)
    file_norms_processed = models.FileField(upload_to=get_document_upload_path, 
                                            max_length=350, blank=True, null=True)
    class Meta:
        ordering = ('nosology',)
        
    def __unicode__(self):
        return self.name
    
    
    
    
    
    