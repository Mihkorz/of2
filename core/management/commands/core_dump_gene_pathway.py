from django.core.management import BaseCommand
from pandas import DataFrame

from core.models import Pathway, Gene


def encode(u):
    # return u.encode('utf-8')  # to deal with incorrect names
    return str(u)


def create_gene_names(pathways):
    res = set()
    for pathway in pathways:
        for g in Gene.objects.filter(pathway_id=pathway.id):
            res.add(encode(g.name))

    return sorted(list(res))


class Command(BaseCommand):

    help = 'Dump gene-pathway table'

    def handle(self, *args, **options):
        pathways = Pathway.objects.filter(organism='human', database='primary_new').order_by('name')
        gene_names = create_gene_names(pathways)

        df = DataFrame(
            columns=[pw.name for pw in pathways],
            index=gene_names,
            # dtype=bool
        )
        df.fillna(value=0, inplace=True)

        for pw in pathways:
            for gene in Gene.objects.filter(pathway_id=pw.id):
                df.set_value(encode(gene.name), encode(pw.name), 1)

        df.to_csv('gene_pathway_report.csv')
