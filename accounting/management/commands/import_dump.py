from django.core.management.base import BaseCommand
from django.db import connection, transaction
import os
import re
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Import cleaned SQL dump and reset admin password'

    def handle(self, *args, **options):
        dump_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'warehouse_backup_clean.sql'
        )

        if not os.path.exists(dump_path):
            self.stdout.write(self.style.WARNING('⚠️ Dump file not found, skipping import'))
        else:
            self.stdout.write('🔄 Starting import...')

            try:
                with open(dump_path, 'r', encoding='utf-8') as f:
                    sql = f.read()

                with connection.cursor() as cursor:
                    # Разделяем на команды по ;
                    commands = sql.split(';')

                    for i, command in enumerate(commands):
                        cmd = command.strip()

                        # Пропускаем пустые и комментарии
                        if not cmd or cmd.startswith('--'):
                            continue

                        # Пропускаем мета-информацию из pg_dump
                        if re.match(r'^(Owner:|Schema:|Type:|Name:|Data for Name:|SEQUENCE SET|DEFAULT PRIVILEGES)',
                                    cmd, re.IGNORECASE):
                            continue

                        # Пропускаем команды psql (\COPY, \connect, \unrestrict и т.д.)
                        if cmd.startswith('\\'):
                            continue

                        # Пропускаем только комментарии в середине строки
                        if 'Owner:' in cmd and 'ALTER' not in cmd.upper():
                            continue

                        try:
                            with transaction.atomic():
                                cursor.execute(cmd)
                        except Exception as e:
                            err = str(e).lower()
                            # Пропускаем "уже существует" и пустые ошибки
                            if 'already exists' not in err and 'must be owner of' not in err and err.strip():
                                self.stdout.write(self.style.WARNING(f'⚠️ [{i + 1}] {str(e)[:80]}'))

                self.stdout.write(self.style.SUCCESS('✅ Import completed successfully!'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Import failed: {e}'))

        # === СБРОС ПАРОЛЯ ДЛЯ ADMIN ===
        try:
            # Проверяем, существует ли таблица auth_user
            with connection.cursor() as cursor:
                cursor.execute("""
                               SELECT EXISTS (SELECT
                                              FROM information_schema.tables
                                              WHERE table_name = 'auth_user');
                               """)
                table_exists = cursor.fetchone()[0]

            if table_exists:
                admin = User.objects.filter(username='admin').first()
                if admin:
                    admin.set_password('NewPass2024!')
                    admin.save()
                    self.stdout.write(self.style.SUCCESS('🔑 Admin password reset to: NewPass2024!'))
                else:
                    User.objects.create_superuser('admin', 'admin@example.com', 'NewPass2024!')
                    self.stdout.write(self.style.SUCCESS('🔑 New admin created with password: NewPass2024!'))
            else:
                self.stdout.write(self.style.WARNING('⚠️ Table auth_user not found, skipping password reset'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to reset admin password: {e}'))