import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from medic.models import TreatmentMethod


def _num_tumour(fname):
    with open(fname) as f:
        dialect = csv.Sniffer().sniff(f.read(1024), delimiters=",\t")
        f.seek(0)

        reader = csv.reader(f, dialect)
        row = reader.next()

    return len([s for s in row if 'tumour' in s.lower()])


def _num_tumour_safe(fname):
    try:
        return _num_tumour(fname)
    except IOError:
        print 'IOError "%s"' % fname
    except csv.Error:
        print 'csv.Error "%s"' % fname

    return -1


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

                fname = os.path.join(settings.MEDIA_ROOT, str(obj.file_res))
                row.append(_num_tumour_safe(fname))

                fname = os.path.join(settings.MEDIA_ROOT, str(obj.file_nres))
                row.append(_num_tumour_safe(fname))

                # row.append(unicode(obj.treatment).encode('utf-8'))
                # row.append('--')

                writer.writerow(row)


