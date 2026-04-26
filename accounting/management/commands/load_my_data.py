from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load data from data.json'

    def handle(self, *args, **options):
        dump_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'data.json'
        )

        if not os.path.exists(dump_path):
            self.stdout.write(self.style.ERROR('❌ data.json not found!'))
            return

        self.stdout.write('🔄 Loading data from data.json...')

        try:
            call_command('loaddata', dump_path, verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))