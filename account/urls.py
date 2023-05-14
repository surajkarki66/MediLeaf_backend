from django.urls import include, path

from .views import SignUpAPIView, LoginAPIView, LogoutAPIView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('login/', LoginAPIView.as_view(), name='login-api'),
    path('logout/', LogoutAPIView.as_view(), name='logout-api')

]
