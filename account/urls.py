from django.urls import include, path

from .views import SignUpAPIView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup-api'),

]
