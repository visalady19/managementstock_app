from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect root URL ke login
    path('', lambda request: redirect('/accounts/login/')),

    # ROUTE LOGIN / REGISTER
    path('accounts/', include('accounts.urls')),

    # OTHER APPS
    path('dashboard/', include('dashboard.urls')),
    path('inventory/', include('inventory.urls')),
    path('masuk/', include('transaksi_masuk.urls')),
    path('keluar/', include('transaksi_keluar.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)