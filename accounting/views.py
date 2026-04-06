from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import EquipmentType, Equipment, RepairRequest
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate


# Домашняя страница
@login_required
def home(request):
    return render(request, 'accounting/home.html')

@login_required
# Список устройст на базе андроид
def board_android(request):
    board_androids = Equipment.objects.filter(equip_type=EquipmentType.ANDROID_BOARD)
    return render(request, 'accounting/board_android_list.html', {'board_androids': board_androids})

@login_required
# Список устройст на базе Windows
def board_windows(request):
    board_windows = Equipment.objects.filter(equip_type=EquipmentType.WINDOWS_BOARD)
    return render(request, 'accounting/board_windows_list.html', {'board_windows': board_windows})

@login_required
# Список плат T-con
def tcon(request):
    tcons = Equipment.objects.filter(equip_type=EquipmentType.TCON)
    return render(request, 'accounting/tcon_list.html', {'tcons': tcons})

@login_required
# Список кабелей
def cable(request):
    cables= Equipment.objects.filter(equip_type=EquipmentType.CABLE)
    return render(request, 'accounting/cable_list.html', {'cables': cables})

@staff_member_required
# Вывод всех запросов
def request_list(request):
    req_pending =  RepairRequest.objects.filter(status='pending')
    return render(request, 'accounting/request_list.html', {'req_pending': req_pending})

@staff_member_required
# Вывод истории выдачи
def history_list(request):
    req_history = RepairRequest.objects.filter(status__in=['confirmed', 'rejected'])  # Фильтр для 2х условий
    return render(request, 'accounting/history_list.html', {'req_history': req_history})

@login_required
# Логика оформления заявки для запроса оборудования
def request_item(request, pk):
    # 1. Находим оборудование
    req_item = get_object_or_404(Equipment, pk=pk)

    # Получение страницы возврата
    next_page = request.GET.get('next', "home")
    # 2. Если нажата кнопка запросить
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 0))
        except ValueError:
            messages.error(request, 'Некорректное количество')
            return redirect('board_android_list')

        # ✅ Проверка: количество больше 0
        if quantity <= 0:
            messages.error(request, 'Количество должно быть больше 0')
            return redirect('request_item', pk=pk)

        # ✅ Проверка: хватает ли на складе
        if quantity > req_item.quantity:
            messages.error(request, f"На складе только {req_item.quantity} шт.")
            return redirect('request_item', pk=pk)

        # 3. Создание заявки
        RepairRequest.objects.create(
            equipment=req_item,
            requesting_user=request.user,
            quantity_requested=quantity,
            status="pending"
        )

        messages.success(request, 'Заявка создана!')
        return redirect(next_page)

    return render(request, 'accounting/request_item.html', {
        'req_item': req_item,
        'next_page': next_page
    })

@staff_member_required
# Логика выдачи оборудования
def confirm_request(request, request_id):
    # Находим заявку
    req_item = get_object_or_404(RepairRequest, id=request_id)

    # Проверяем статус
    if req_item.status != "pending":
        messages.error(request,'Заявку уже обработали')
        return redirect('request_list')

    # Находим оборудование
    equipment = req_item.equipment

    # Проверяем остаток
    if equipment.quantity < req_item.quantity_requested:
        messages.error(request, f"Недостаточное количество. Осталось: {equipment.quantity}")
        return redirect ("request_list")

    # Списываем со склада
    equipment.quantity -= req_item.quantity_requested
    equipment.save()

    # Присваиваем статус
    req_item.status = 'confirmed'

    # Фиксируем время и дату выдачи
    req_item.confirmed_at = timezone.now()
    req_item.approved_user = request.user
    req_item.save()

    messages.success(request, f"Количество {req_item.quantity_requested} успешно выдано")
    return redirect ("request_list")

@staff_member_required
# Логика отказа о выдаче
def reject_application(request, req_id):
    reject = get_object_or_404(RepairRequest, id=req_id)

    # Проверка: заявку можно отклонить, только если она в статусе "Ожидает"
    if reject.status != "pending":
        messages.error(request, 'Заявку уже обработали')
        return redirect("request_list")

    # Заполняем данные об отклонении
    reject.status = "rejected"
    reject.approved_user = request.user      # ← Кто отклонил
    reject.confirmed_at = timezone.now()     # ← Когда отклонил
    reject.save()

    messages.success(request, f"Заявка #{reject.id} успешно отклонена")  # ← Добавлен request
    return redirect("request_list")


# Страница входа
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounting/login.html', {'form': form})

# Страница выхода
def logout_view(request):
    logout(request)
    messages.info(request,'Вы успешно вышли из системы')
    return redirect('login')

# Логика вывода заявок для пользователя
@login_required  # ← Только для авторизованных
def history_user(request):
    # Фильтруем заявки: только для текущего пользователя
    user_requests = RepairRequest.objects.filter(
        requesting_user=request.user
    ).select_related('equipment')  # ← Оптимизация: сразу подгружаем оборудование

    return render(request, "accounting/my_request.html", {"user_requests": user_requests})