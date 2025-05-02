from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', include('core.urls')),
    path('wms/', include('warehouse.urls')),
    path('rent/', include('rent.urls')),
    path('manager/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = 'Gestão Lirasoft'
admin.site.site_title = 'Gestão Lirasoft'
admin.site.index_title = 'Área Administrativa'
