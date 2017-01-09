from django.core.management import BaseCommand
from pandas import DataFrame

from core.models import Pathway, Gene


def _encode(u):
    return u.encode('utf-8')  # to deal with incorrect names  # TODO: remove once data validations is ready
    # return str(u)


def _create_gene_names(pathways):
    res = set()
    for pathway in pathways:
        for g in Gene.objects.filter(pathway_id=pathway.id):
            res.add(_encode(g.name))

    return sorted(list(res))


# def dump_gene_pathway(ostream, pathway_names):
def dump_gene_pathway(ostream):
    pathways = Pathway.objects.filter(organism='human', database='primary_new').order_by('name')
    gene_names = _create_gene_names(pathways)

    df = DataFrame(
        columns=[pw.name for pw in pathways],
        index=gene_names,
        # dtype=bool
    )
    df.fillna(value=0, inplace=True)

    for pw in pathways:
        for gene in Gene.objects.filter(pathway_id=pw.id):
            df.set_value(_encode(gene.name), _encode(pw.name), 1)

    df.to_csv(ostream)


class Command(BaseCommand):

    help = 'Dump gene-pathway table'
    # option_list = BaseCommand.option_list + (make_option('--pathways-file', help='File containing...', type=int), )

    def handle(self, *args, **options):
        # ostream = self.stdout
        ostream = 'gene_pathway_report.csv'

        pathway_names = [
            '2-amino-3-carboxymuconate_semialdehyde_degradation_to_glutaryl-CoA',
            '4-hydroxybenzoate_biosynthesis',
            'glutathione_redox_reactions_I',
            'alpha-tocopherol_degradation',
            'STAT3_Pathway_G1_to_S_Cell_Cycle_Progression',
            'JAK-STAT_Pathway_Gene_Expression_via_MYC',
            'STAT3_Pathway_Anti-Apoptosis',
            'Glucocorticoid_Receptor_Signaling_Pathway_Cell_Cycle_Arrest',
            'IL-10_Pathway_Stability_Determination',
            'acetone_degradation_I_to_methylglyoxal',
            'ILK_Signaling_Pathway_Tissue_Morphogenesis',
            'BRCA1_Pathway_Growth_Promoting_Genes_hTert_S100A7',
            'Akt_Signaling_Pathway_Glucose_Uptake',
            'Erythropoietin_Pathway_Gene_Expression_Neuroprotection_via_NFKB2',
            'Circadian_Pathway',
            'aspirin-triggered_lipoxin_biosynthesis',
            'thio-molybdenum_cofactor_biosynthesis',
            'tyrosine_degradation',
            'EGF_Pathway_IP3_Signaling',
            'UTP_and_CTP_dephosphorylation_I',
            'zymosterol_biosynthesis',
            'urea_cycle',
            'uracil_degradation',
            'UDP-D-xylose_and_UDP-D-glucuronate_biosynthesis',
            'resolvin_D_biosynthesis',
            'EGF_Pathway_Rab5_Regulation_Pathway',
            'ILK_Signaling_Pathway_MMP2_MMP9_Gene_Expression_Tissue_Invasion_via_FOS',
            'aspirin_triggered_resolvin_D_biosynthesis',
            'L-serine_degradation',
            'tetrapyrrole_biosynthesis',
            'thymine_degradation',
            'asparagine_biosynthesis',
            'tetrahydrobiopterin_ide_novoi_biosynthesis',
            'mineralocorticoid_biosynthesis',
            'aspirin_triggered_resolvin_D_biosynthesis',
            'bile_acid_biosynthesis_neutral_pathway',
            'heme_biosynthesis',
            'imyoi-inositol_ide_novoi_biosynthesis',
            'glucocorticoid_biosynthesis',
            'epoxysqualene_biosynthesis',
        ]

        dump_gene_pathway(ostream)
