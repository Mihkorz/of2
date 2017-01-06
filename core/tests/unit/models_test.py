import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import TransactionManagementError
from mixer.backend.django import mixer
import pytest

from core.models import Gene, Component, Node, Pathway, Relation, import_pathway


def resource_file(fname):
    return os.path.join(settings.APP_RESUORCES_ROOT, 'tests', 'unit', 'core', fname)


@pytest.mark.django_db
class TestModels(object):

    def test_pathway(self):
        pathway = mixer.blend(Pathway)
        pathway.clean()
        assert ' ' not in pathway.name
        assert '\t' not in pathway.name

        assert len(pathway.gene_list()) == 0

    def test_gene(self):
        gene = mixer.blend(Gene)
        gene.clean()
        assert ' ' not in gene.name
        assert '\t' not in gene.name

    def test_component(self):
        c = mixer.blend(Component)
        c.clean()
        assert ' ' not in c.name
        assert '\t' not in c.name

    def test_node(self):
        n = mixer.blend(Component)
        n.clean()
        assert ' ' not in n.name
        assert '\t' not in n.name

    def test_node_component(self):
        n = mixer.blend(Node)
        assert n.component_list() == ''

        _ = mixer.blend(Component, node=n)
        assert 'href' in n.component_list()

    def test_node_relation(self):
        n1 = mixer.blend(Node)
        n2 = mixer.blend(Node)
        _ = mixer.blend(Relation, fromnode=n1, tonode=n2)

        assert n1.in_rel() == ''
        assert 'href' in n1.out_rel()

        assert 'href' in n2.in_rel()
        assert n2.out_rel() == ''

    def test_relation(self):
        p = mixer.blend(Pathway, name='P')
        n = mixer.blend(Node, name='A', pathway=p)
        r = mixer.blend(Relation, fromnode=n)
        assert r.pathway().name == 'P'


def _check_db_empty():
    assert len(Pathway.objects.all()) == 0
    assert len(Node.objects.all()) == 0
    assert len(Component.objects.all()) == 0
    assert len(Relation.objects.all()) == 0


@pytest.mark.django_db
class TestImportPathway(object):

    def test_basic(self):
        fname = resource_file('mycn_Response_final_test.xls')
        with open(fname, 'rb') as f:
            import_pathway(f, 'alien', 'deep space')

        pathways = list(Pathway.objects.all())
        assert len(pathways) == 1

        pw = pathways[0]
        assert pw.name == 'mycn_Response_final_test'
        # assert pw.name == 'reactome_Viral_mRNA_Translation_Main_Pathway'
        assert pw.organism == 'alien'
        assert pw.database == 'deep space'

        # see data file
        assert len(Node.objects.all()) == 131
        assert len(Component.objects.all()) == 131
        assert len(Relation.objects.all()) == 132

    @pytest.mark.xfail(reason='bug; confirmed by Mikhail')
    def test_component_names(self):
        fname = resource_file('reactome Viral mRNA Translation Main Pathway.xls')
        with open(fname, 'rb') as f:
            import_pathway(f, 'alien', 'deep space')

        pathways = list(Pathway.objects.all())
        assert len(pathways) == 1

        pw = pathways[0]
        assert pw.name == 'mycn_Response_final_test'
        assert pw.organism == 'alien'
        assert pw.database == 'deep space'

        # see data file
        assert False, 'This test is failing'
        assert len(Node.objects.all()) == -1
        assert len(Component.objects.all()) == -1
        assert len(Relation.objects.all()) == -1

    def test_import_more_than_once(self):
        fname = resource_file('mycn_Response_final_test.xls')
        with open(fname, 'rb') as f:
            import_pathway(f, 'alien', 'deep space')

        with open(fname, 'rb') as f:
            import_pathway(f, 'stranger', 'deep space')

        with pytest.raises(RuntimeError) as excinfo:
            with open(fname, 'rb') as f:
                import_pathway(f, 'alien', 'deep space')

        assert 'exists' in excinfo.value.message

    def test_invalid_gene(self):
        fname = resource_file('invalid_gene.xls')
        with pytest.raises(TransactionManagementError):
            with open(fname, 'rb') as f:
                import_pathway(f, 'alien', 'deep space')

        _check_db_empty()

    def test_invalid_edge(self):
        fname = resource_file('invalid_edge.xls')
        with pytest.raises(ObjectDoesNotExist) as excinfo:
            with open(fname, 'rb') as f:
                import_pathway(f, 'alien', 'deep space')

        assert excinfo.value.message == 'Node matching query does not exist.'

        _check_db_empty()

    def test_invalid_node(self):
        fname = resource_file('invalid_node.xls')
        with pytest.raises(ObjectDoesNotExist) as excinfo:
            with open(fname, 'rb') as f:
                import_pathway(f, 'alien', 'deep space')

        assert excinfo.value.message == 'Node matching query does not exist.'

        _check_db_empty()
