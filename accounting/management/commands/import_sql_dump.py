from django.core.management.base import BaseCommand
from django.db import connection
import os
import re


class Command(BaseCommand):
    help = 'Import SQL dump with COPY support'

    def handle(self, *args, **options):
        dump_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'warehouse_backup.sql'  # ← Имя твоего файла
        )

        if not os.path.exists(dump_path):
            self.stdout.write(self.style.ERROR(f'❌ File not found: {dump_path}'))
            return

        self.stdout.write('🔄 Starting SQL import...')

        with open(dump_path, 'r', encoding='utf-8') as f:
            sql = f.read()

        # Разделяем на команды по ;
        commands = sql.split(';')

        with connection.cursor() as cursor:
            in_copy = False
            copy_buffer = []

            for cmd in commands:
                cmd = cmd.strip()
                if not cmd or cmd.startswith('--'):
                    continue

                # Начинается COPY
                if cmd.startswith('COPY ') and 'FROM stdin' in cmd:
                    in_copy = True
                    copy_buffer = [cmd]  # Сохраняем заголовок COPY
                    continue

                # Конец COPY
                if in_copy:
                    copy_buffer.append(cmd)
                    if cmd == '\\.':  # Конец данных COPY
                        in_copy = False
                        full_copy = ';'.join(copy_buffer) + ';'
                        try:
                            cursor.copy_expert(full_copy, cursor)
                            self.stdout.write(self.style.SUCCESS('✅ COPY executed'))
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'⚠️ COPY error: {str(e)[:60]}'))
                        copy_buffer = []
                    continue

                # Обычный SQL
                try:
                    # Пропускаем мета-команды
                    if re.match(r'^(SET|SELECT|ALTER DEFAULT|OWNER TO|ALTER SCHEMA)', cmd, re.IGNORECASE):
                        continue
                    if cmd.startswith('\\'):
                        continue

                    cursor.execute(cmd)
                except Exception as e:
                    err = str(e).lower()
                    if 'already exists' not in err and 'must be owner' not in err:
                        self.stdout.write(self.style.WARNING(f'⚠️ {str(e)[:60]}'))

        self.stdout.write(self.style.SUCCESS('✅ Import finished!'))