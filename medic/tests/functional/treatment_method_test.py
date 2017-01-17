from cStringIO import StringIO

import pytest

from medic.management.commands import check_all_treatment_methods


@pytest.mark.xfail(reason='There are inconsistent racords/files at the moment; should be fixed.')
@pytest.mark.django_db
def test_treatment_methods_integrity():
    stream = StringIO()
    check_all_treatment_methods(stream)
    stream.seek(0)
    report = stream.read()
    assert len(report) == 0, 'Should be no errors.'
