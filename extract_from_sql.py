# extract_from_sql.py
import re
import json

print("🔄 Parsing warehouse_backup.sql...")

with open('warehouse_backup.sql', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

all_data = []

# === 1. Извлекаем пользователей (auth_user) ===
print("  - Extracting users...")
user_pattern = r"COPY public\.auth_user .*? FROM stdin;([\s\S]*?)\\\."
user_match = re.search(user_pattern, content)
if user_match:
    lines = user_match.group(1).strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 10:
            all_data.append({
                "model": "auth.user",
                "pk": int(parts[0]),
                "fields": {
                    "password": parts[1],
                    "last_login": parts[2] if parts[2] != '\\N' else None,
                    "is_superuser": parts[3] == 't',
                    "username": parts[4],
                    "first_name": parts[5],
                    "last_name": parts[6],
                    "email": parts[7],
                    "is_staff": parts[8] == 't',
                    "is_active": parts[9] == 't',
                    "date_joined": parts[10] if len(parts) > 10 else "2026-01-01T00:00:00Z",
                    "groups": [],
                    "user_permissions": []
                }
            })

# === 2. Извлекаем оборудование (accounting_equipment) ===
print("  - Extracting equipment...")
equip_pattern = r"COPY public\.accounting_equipment .*? FROM stdin;([\s\S]*?)\\\."
equip_match = re.search(equip_pattern, content)
if equip_match:
    lines = equip_match.group(1).strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 11:
            all_data.append({
                "model": "accounting.equipment",
                "pk": int(parts[0]),
                "fields": {
                    "name": parts[1],
                    "equip_type": parts[2],
                    "model": parts[3],
                    "modification": parts[4],
                    "length_cm": int(parts[5]) if parts[5] != '\\N' else None,
                    "cpu": parts[10] if len(parts) > 10 else "",
                    "quantity": int(parts[6]),
                    "cells": parts[7],
                    "image": parts[8],
                    "description": parts[9]
                }
            })

print(f"✅ Extracted {len(all_data)} objects")
print(f"   Equipment count: {len([x for x in all_data if x['model'] == 'accounting.equipment'])}")

# Сохраняем
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("✅ Saved to data.json")