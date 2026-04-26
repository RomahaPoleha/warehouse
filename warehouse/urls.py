# """
# URL configuration for warehouse project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/6.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#
# from django.http import HttpResponse
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('accounting.urls')),
# ]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#

from django.http import HttpResponse
from django.contrib import admin

# Тестовые视图 — без зависимости от accounting
def test_root(request):
    return HttpResponse('<h1>✅ ROOT WORKS!</h1>')

def test_admin(request):
    return HttpResponse('<h1>✅ ADMIN URL REACHED!</h1>')

urlpatterns = [
    path('', test_root),
    path('admin/', admin.site.urls),
    path('test-admin/', test_admin),
    # accounting отключен для теста
    # path('', include('accounting.urls')),
]