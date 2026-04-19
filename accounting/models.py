from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class EquipmentType(models.TextChoices):
    """Типы оборудования"""
    ANDROID_BOARD = 'android_board', _('Плата Android')
    WINDOWS_BOARD = 'windows_board', _('Платы Windows')
    TCON = 'tcon', _('T-Con плата')
    CABLE = 'cable', _('Шлейф')
    VIDEOWALL = 'videowall', _('Видеостена')

class Equipment(models.Model):
    """Основная информация о всех типах оборудования"""
    name = models.CharField(max_length=100, verbose_name="Наименование")
    equip_type = models.CharField(
        max_length=20,
        choices=EquipmentType.choices,
        verbose_name="Тип оборудования"
    )
    model = models.CharField(max_length=100, verbose_name="Модель")

    # Поля которые есть не у всех и могут быть пустыми
    modification = models.CharField(max_length=100, blank=True, verbose_name="Модификация")
    length_cm = models.PositiveIntegerField(verbose_name="Длина (см)", null=True, blank=True)
    cpu = models.CharField(max_length=10, verbose_name="Процессор", blank=True)
    # Поля с количеством и место хранения
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=0)
    cells = models.CharField(max_length=100, verbose_name="Место хранения", blank=True)

    # Медиа и описание
    image = models.URLField(max_length=500, blank=True, verbose_name='Ссылка на фото', default='')
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Единица оборудования"
        verbose_name_plural = "Оборудование"
        ordering = ["name"]

    def __str__(self):
        return f"{self.get_equip_type_display()}: {self.name} ({self.model})"


class RepairRequest(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,  # Исправлено: one_delete -> on_delete
        verbose_name="Запчасть для ремонта"
    )

    requesting_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Исправлено: one_delete и Cascade
        null=True,
        related_name='repair_requests_created', # Уникальное имя, без него будет ошибка
        verbose_name="Запросил"
    )

    quantity_requested = models.PositiveIntegerField(verbose_name="Запрошено кол-во")

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Ожидает"),
            ("confirmed", "Подтверждено"),
            ("rejected", "Отклонено")
        ],
        default="pending",
        verbose_name="Статус"
    )

    # Исправлено: auto_noe_add -> auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    approved_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Исправлено: one_delete
        null=True,
        blank=True,
        related_name='repair_requests_approved', # Уникальное имя, без него будет ошибка
        verbose_name="Подтвердил"
    )

    def __str__(self):
        # Исправлено: используем __str__ модели Equipment
        return f"Заявка #{self.id} на {self.equipment}"
