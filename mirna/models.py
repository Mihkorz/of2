import os

from django.conf import settings
from django.db import models
from pandas import read_csv


class MirnaDb(object):
    MIRTARBASE_STRONG = 'MIRTARBASE_STRONG'
    MIRTARBASE_ALL = 'MIRTARBASE_ALL'

    ALL = (MIRTARBASE_STRONG, MIRTARBASE_ALL)

    CHOISES = (
        (MIRTARBASE_STRONG, 'miRTarBase strong'),
        (MIRTARBASE_ALL, 'miRTarBase all'),
    )
    assert len(CHOISES) == len(ALL)


def load_mirna_mapping(db, organism):
    if db == MirnaDb.MIRTARBASE_STRONG and organism == 'human':
        fname = 'human_miRNA_targets_strong.csv'

    elif db == MirnaDb.MIRTARBASE_STRONG and organism == 'mouse':
        fname = 'mouse_miRNA_targets_strong.csv'

    elif db == MirnaDb.MIRTARBASE_ALL and organism == 'human':
        fname = 'human_miRNA_targets_all.csv'

    elif db == MirnaDb.MIRTARBASE_ALL and organism == 'mouse':
        fname = 'mouse_miRNA_targets_all.csv'
    else:
        raise RuntimeError('Unknown database-organism combination: "{}-{}".'.format(db, organism))

    full_fname = os.path.join(settings.MEDIA_ROOT, 'mirna', fname)
    return read_csv(full_fname)


class MirnaMapping(models.Model):
    miRNA_ID = models.CharField(verbose_name='miRNA_ID', db_index=True, max_length=250, blank=False)
    miRBase_ID = models.CharField(verbose_name='miRBase_ID', max_length=250, blank=False)
    Gene = models.CharField(verbose_name='Gene', max_length=250, blank=False)
    Probability = models.DecimalField(verbose_name='Probability', max_digits=2, decimal_places=1, default=0)
    Sourse = models.CharField(verbose_name='Sourse', max_length=250, blank=False)
    Organism = models.CharField(verbose_name='Organism', max_length=250, blank=False)
