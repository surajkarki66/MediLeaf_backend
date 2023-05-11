from django.contrib import admin
from django.conf import settings
from django.conf.urls import static
from django.urls import path, include
from django.utils.translation import gettext_lazy as _


admin.site.site_header = _('MediLeaf administration')

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)