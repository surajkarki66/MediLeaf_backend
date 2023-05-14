from django.urls import include, path

from .views import SignUpAPIView, LoginAPIView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('login/', LoginAPIView.as_view(), name='login-api'),

]
