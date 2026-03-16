from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class EquipmentType(models.TextChoices):
    """Типы оборудования"""
    ANDROID_BOARD = 'android_board',_('Плата Android')
    WINDOWS_BOARD = 'windows_board',_('Платы Windows')
    TCON = 'tcon',_('T-Con плата')
    CABLE = 'cable',_('Шлейф')

class Equipment(models.Model):
    """Основная информация о всех типах оборудования"""
    name = models.CharField(max_length=100, verbose_name="Наименование")
    equip_type = models.CharField(
        max_length=20,
        choices=EquipmentType.choices,
        verbose_name="Тип оборудования"
    )
    model = models.CharField(
        max_length=100, verbose_name="Модель"
    )
    # Поля которые есть не у всех и могут быть пустыми
    modification = models.CharField(max_length=100, blank=True, verbose_name="Модификация")
    length_cm = models.PositiveIntegerField(verbose_name="Длина (см)", null=True, blank=True)

    # Поля с количеством и место хранения
    quantity = models.PositiveIntegerField(verbose_name="Количество",default=0)
    cells = models.CharField(max_length=100, verbose_name="Место хранения", blank=True)

    # Медиа и описание
    image = models.ImageField(upload_to='images/equipment/', verbose_name="Картинка",blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    # Дата
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Единица оборудования"
        verbose_name_plural = "Оборудование"
        ordering = ["name"]

    def __str__(self):
        return f"{self.get_equip_type_display()}: {self.name} ({self.model})"