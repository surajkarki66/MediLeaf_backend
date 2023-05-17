from django.urls import include, path
from rest_framework.routers import DefaultRouter

from userprofile import views

router = DefaultRouter()

router.register(r'profile', views.ProfileViewSet, 'profile')

app = 'userprofile'

urlpatterns = [
    path('', include(router.urls)),
    path('user-profile/', views.UserProfileAPIView.as_view(), name='user-profile'),
]
