from django.core.management.base import BaseCommand
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Import SQL dump from warehouse_backup.sql'

    def handle(self, *args, **options):
        dump_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                                 'warehouse_backup.sql')

        if not os.path.exists(dump_path):
            self.stdout.write(self.style.ERROR(f'File not found: {dump_path}'))
            return

        self.stdout.write('Importing SQL dump...')

        with open(dump_path, 'r', encoding='utf-8') as f:
            sql = f.read()

        with connection.cursor() as cursor:
            # Разделяем на отдельные команды
            commands = sql.split(';')
            for command in commands:
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Skipped: {str(e)[:50]}'))

        self.stdout.write(self.style.SUCCESS('✅ SQL dump imported successfully!'))