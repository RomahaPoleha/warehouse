from django.urls import path
from . import views


urlpatterns = [
    # path('createadmin/', views.create_superuser, name='createadmin'),
    path('ir_frames_list.html/',views.ir_frames, name='ir_frames_list'),
    path('front_and_connector_list', views.front_and_connector, name='front_and_connector_list'),
    path('', views.home, name='home'), # Домашняя страница
    path('board_android/', views.board_android, name='board_android_list'), # Страница с устройствами андроид
    path('board_windows/', views.board_windows, name='board_windows_list'), # Страница с устройствами Windows
    path('tcon_list/', views.tcon, name='tcon_list'), # Страница с платами т-кон
    path('cable_list/', views.cable, name='cable_list'), # Страница с кабелями
    path('request_item/<int:pk>/', views.request_item, name='request_item'), # Страница с вводом количества
    path('request_list/', views.request_list, name='request_list'), # Страница с запросами на выдачу
    path('requests/<int:request_id>/confirm/', views.confirm_request, name='confirm_request'), # создаёт маршрут (ссылку) для подтверждения заявки
    path('history_list/', views.history_list, name='history_list'), # Страница с выводом истории выдачи
    path('requests/<int:req_id>/reject/', views.reject_application, name='reject_application'), # создаёт маршрут (ссылку) для отклонения заявки
    path('login/', views.login_view, name='login'), # Страница входа
    path('logout/', views.logout_view, name='logout'), # Страница выхода
    path('my_requests/', views.history_user, name='history_user'), # История пользователя
    path('videowall/', views.videowall, name='videowall_list')
]