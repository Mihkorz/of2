from cStringIO import StringIO

import pytest

from core.management.commands import dump_gene_pathway


@pytest.mark.django_db
def test():
    # pathways = ['Akt_Signaling_Pathway_Glucose_Uptake']

    stream = StringIO()

    dump_gene_pathway(stream)
    stream.seek(0)
    lines = stream.readlines()
    assert len(lines) > 1, 'Should contain at least header and a data row'

    stream.close()
