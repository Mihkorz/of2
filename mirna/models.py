from django.db import models

class MirnaMapping(models.Model):
    miRNA_ID = models.CharField(verbose_name='miRNA_ID', db_index=True, max_length=250, blank=False)
    miRBase_ID = models.CharField(verbose_name='miRBase_ID', max_length=250, blank=False)
    Gene = models.CharField(verbose_name='Gene', max_length=250, blank=False)
    Probability = models.DecimalField(verbose_name='Probability', max_digits=2, decimal_places=1, default=0)
    Sourse = models.CharField(verbose_name='Sourse', max_length=250, blank=False)
