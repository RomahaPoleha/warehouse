from django.core.management.base import BaseCommand
from django.db import connection, transaction
import os


class Command(BaseCommand):
    help = 'Import cleaned SQL dump'

    def handle(self, *args, **options):
        dump_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'warehouse_backup_clean.sql'
        )

        if not os.path.exists(dump_path):
            self.stdout.write(self.style.ERROR(f'❌ File not found: {dump_path}'))
            return

        self.stdout.write('🔄 Starting import...')

        try:
            with open(dump_path, 'r', encoding='utf-8') as f:
                sql = f.read()

            with connection.cursor() as cursor:
                # Разделяем на команды по ;
                commands = [cmd.strip() for cmd in sql.split(';') if cmd.strip() and not cmd.strip().startswith('--')]

                for i, command in enumerate(commands):
                    if command and not command.startswith('\\'):  # Пропускаем \COPY, \unrestrict и т.д.
                        try:
                            with transaction.atomic():
                                cursor.execute(command)
                        except Exception as e:
                            # Пропускаем ошибки существующих таблиц/последовательностей
                            if 'already exists' not in str(e).lower():
                                self.stdout.write(self.style.WARNING(f'⚠️ [{i + 1}] {str(e)[:60]}'))

            self.stdout.write(self.style.SUCCESS('✅ Import completed successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Import failed: {e}'))