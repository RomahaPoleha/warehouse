# clean_dump.py — очищает SQL дамп от старых владельцев
import re

with open('warehouse_backup.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Удаляем все строки с "OWNER TO warehouse_bt3x_user"
content = re.sub(r'ALTER TABLE [^\n]+ OWNER TO warehouse_bt3x_user;?\n', '', content)
content = re.sub(r'ALTER SCHEMA [^\n]+ OWNER TO warehouse_bt3x_user;?\n', '', content)
content = re.sub(r'ALTER DEFAULT PRIVILEGES [^\n]+ warehouse_bt3x_user;?\n', '', content)

# 2. Заменяем владельца в CREATE TABLE (опционально)
content = re.sub(r'Owner: warehouse_bt3x_user', 'Owner: warehouse_user', content)

# 3. Удаляем мусор в конце файла (если есть)
if '\\unrestrict' in content:
    content = content.split('\\unrestrict')[0]

with open('warehouse_backup_clean.sql', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Файл очищен: warehouse_backup_clean.sql")