import pytest

from medic.management.commands.medic_check import check_all_treatment_methods


@pytest.mark.xfail(reason='It needs RO access to EXISTING test DB from Django')
@pytest.mark.django_db
def test_treatment_methods_integrity():
    check_all_treatment_methods()
