import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from medic.models import TreatmentMethod


INVALID = '--'


def _num_tumour(fname, marker):
    with open(fname) as f:
        reader = csv.reader(f)
        row = reader.next()

    return len([s for s in row if marker.lower() in s.lower()])


def _num_tumour_safe(fname, marker):
    try:
        return _num_tumour(fname, marker)
    except IOError:
        print 'IOError "%s"' % fname
    except csv.Error:
        print 'csv.Error "%s"' % fname

    return INVALID


class Command(BaseCommand):

    help = 'Create threatment report.'

    def handle(self, *args, **options):
        out_fname = 'treatment_report.csv'

        with open(out_fname, 'w') as fout:
            writer = csv.writer(fout)

            writer.writerow([
                'Name',
                'Number of patients',
                'Number of responders',
                'Number of nonresponders',
                'Therapy',
            ])

            for obj in TreatmentMethod.objects.all().order_by('name'):
                row = [
                    obj.name,
                    obj.num_of_patients
                ]

                # TODO: invalid data?
                # GSE22093_GSE9574_ERN: total 45, resp: 18, non-resp: 37. ?!

                # fname = os.path.join(settings.MEDIA_ROOT, str(obj.file_res))
                # row.append(_num_tumour_safe(fname))

                # fname = os.path.join(settings.MEDIA_ROOT, str(obj.file_nres))
                # row.append(_num_tumour_safe(fname))

                fname = os.path.join(settings.MEDIA_ROOT, str(obj.file_nres))
                num_non_resp = _num_tumour_safe(fname, 'NRES')

                if num_non_resp != INVALID:
                    num_resp = int(obj.num_of_patients) - num_non_resp
                else:
                    num_resp = INVALID

                row.append(num_resp)
                row.append(num_non_resp)

                row.append(unicode(obj.treatment).encode('utf-8'))

                writer.writerow(row)
