import pytest
from mixer.backend.django import mixer

from core import models


@pytest.mark.django_db
class TestModels(object):

    def test_pathway(self):
        pathway = mixer.blend(models.Pathway)
        pathway.clean()
        assert ' ' not in pathway.name
        assert '\t' not in pathway.name

        assert len(pathway.gene_list()) == 0

    def test_gene(self):
        gene = mixer.blend(models.Gene)
        gene.clean()
        assert ' ' not in gene.name
        assert '\t' not in gene.name

    def test_component(self):
        c = mixer.blend(models.Component)
        c.clean()
        assert ' ' not in c.name
        assert '\t' not in c.name

    def test_node(self):
        n = mixer.blend(models.Component)
        n.clean()
        assert ' ' not in n.name
        assert '\t' not in n.name

    def test_node_component(self):
        n = mixer.blend(models.Node)
        assert n.component_list() == ''

        _ = mixer.blend(models.Component, node=n)
        assert 'href' in n.component_list()

    def test_node_relation(self):
        n1 = mixer.blend(models.Node)
        n2 = mixer.blend(models.Node)
        _ = mixer.blend(models.Relation, fromnode=n1, tonode=n2)

        assert n1.in_rel() == ''
        assert 'href' in n1.out_rel()

        assert 'href' in n2.in_rel()
        assert n2.out_rel() == ''

    def test_relation(self):
        p = mixer.blend(models.Pathway, name='P')
        n = mixer.blend(models.Node, name='A', pathway=p)
        r = mixer.blend(models.Relation, fromnode=n)
        assert r.pathway().name == 'P'
