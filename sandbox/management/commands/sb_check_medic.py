import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from medic.models import TreatmentMethod


class Command(BaseCommand):

    help = 'Check medical module'

    def handle(self, *args, **options):

        i = 0
        for i, obj in enumerate(TreatmentMethod.objects.all().order_by('name')):
            chunks = []

            for attr in ['file_pms1', 'file_probability', 'file_res', 'file_nres']:
                value = getattr(obj, attr)
                fname = os.path.join(settings.MEDIA_ROOT, str(value))
                if not os.path.isfile(fname):
                    chunks.append('%s: missing file: %s' % (attr, fname))

            if chunks:
                print obj.name
                for chunk in chunks:
                    print '  ' + chunk

        print 'Total objects:', i
