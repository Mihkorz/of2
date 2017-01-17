from optparse import make_option

from django.core.management import BaseCommand


class Command(BaseCommand):

    help = 'A demo command.'
    option_list = BaseCommand.option_list + (make_option('-n', help='number', type=int), )

    def handle(self, *args, **options):
        if options['n'] is None:
            self.stdout.write('Missing option -n\n')
            return

        self.stdout.write('** command')

        print 'It is "print" output; it is better to use self.stdout'

        self.stdout.write('args: {}\n'.format(args))
        self.stdout.write('options: {}\n'.format(options))
