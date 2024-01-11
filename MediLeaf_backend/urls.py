from django.contrib import admin
from django.conf import settings
from django.conf.urls import static
from django.urls import path, include
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )
from django.contrib.auth import logout


from .views import api_status


admin.site.site_header = _('MediLeaf administration')
def logout_view(request):
    logout(request)
    return redirect('admin:login')

urlpatterns = [
    path('', api_status, name='api_status'),
    path("admin/logout/", logout_view, name="logout"),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),

    path('api/v1/', include('account.urls')),
    path('api/v1/', include('userprofile.urls')),
    path('api/v1/', include('plant.urls')),
    path('api/v1/', include('contact_us.urls')),

    # Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    *static.static(settings.STATIC_URL,
                       document_root=settings.STATIC_ROOT),
    *static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]