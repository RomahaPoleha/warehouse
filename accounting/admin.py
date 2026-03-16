from django.contrib import admin
from .models import Equipment


# Регистрация в админке таблицы Equipment
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equip_type', 'model', 'quantity']
    list_filter = ['equip_type']
