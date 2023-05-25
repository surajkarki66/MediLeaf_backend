from django.contrib import admin
from django.conf import settings
from django.conf.urls import static
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from .views import api_status


admin.site.site_header = _('MediLeaf administration')

urlpatterns = [
    path('', api_status, name='api_status'),

    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),

    path('api/v1/', include('account.urls')),
    path('api/v1/', include('userprofile.urls')),
]

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )
    urlpatterns = [
        *urlpatterns,
        # YOUR PATTERNS
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
        *static.static(settings.STATIC_URL,
                       document_root=settings.STATIC_ROOT),
        *static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
