import os

from django.conf import settings
from django.core.management import BaseCommand
import pandas as pd


class Command(BaseCommand):

    help = 'Dump miRNA IDs for given genes'

    def handle(self, *args, **options):
        gene_pathway_fname = 'gene_pathway_report.csv'
        gene_mirna_fname = 'gene_to_mirna_id_all.csv'

        df = pd.read_csv(gene_pathway_fname)
        genes = list(df['Unnamed: 0'])
        # print len(genes)

        fname = os.path.join(settings.MEDIA_ROOT, 'mirna', 'human_miRNA_targets_all.csv')
        df = pd.read_csv(fname)

        df = df.loc[df['Gene'].isin(genes)]

        df.drop(['miRTarBase.ID', 'Probability', 'Source'], axis=1, inplace=True)

        # reorder columns
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]

        df.sort_values('Gene', inplace=True)
        df.to_csv(gene_mirna_fname, index=False)
