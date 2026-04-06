from django.contrib import admin
from .models import Equipment, RepairRequest


# Регистрация в админке таблицы Equipment
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equip_type', 'model', 'quantity']
    list_filter = ['equip_type']

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment', 'requesting_user', 'status', 'created_at']
    list_filter = ['status', 'created_at']