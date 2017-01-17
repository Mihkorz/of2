import os
import sys

from django.conf import settings
from django.core.management import BaseCommand

from medic.models import TreatmentMethod


def check_treatment_method(treatment_method):
    """
    Returns: errors: Sequence[str]
    """
    assert isinstance(treatment_method, TreatmentMethod)

    errors = []
    for attr in ['file_pms1', 'file_probability', 'file_res', 'file_nres']:
        value = getattr(treatment_method, attr)
        fname = os.path.join(settings.MEDIA_ROOT, str(value))
        if not os.path.isfile(fname):
            errors.append('%s: missing file: %s' % (attr, fname))

    return errors


def check_all_treatment_methods(stream=sys.stdout):
    treatments = TreatmentMethod.objects.all().order_by('name')

    for treatment in treatments:
        errors = check_treatment_method(treatment)
        if errors:
            stream.write(treatment.name + '\n')
            for chunk in errors:
                stream.write('  %s\n' % chunk)

    stream.write('Total treatment methods: %s\n' % treatments.count())


class Command(BaseCommand):

    help = 'Check medical module'

    def handle(self, *args, **options):
        check_all_treatment_methods()
