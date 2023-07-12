from django.urls import include, path
from rest_framework.routers import DefaultRouter

from contact_us import views

router = DefaultRouter()

router.register(r'contact_us', views.ContactUsViewSet, 'contact_us')


app = 'contact_us'

urlpatterns = [
    path('', include(router.urls)),
]
