from django.urls import include, path

from .views import SignUpAPIView, LoginAPIView, LogoutAPIView, PasswordChangeAPIView, me, ForgotPasswordAPIView, ResetPasswordTokenCheckAPIView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('login/', LoginAPIView.as_view(), name='login-api'),
    path('logout/', LogoutAPIView.as_view(), name='logout-api'),
    path('me/', me, name='me'),
    path('password/change/', PasswordChangeAPIView.as_view(),
         name='password-change-api'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(),
         name='forgot-password-api'),
    path('reset-password/<slug:uidb64>/<slug:token>/',
         ResetPasswordTokenCheckAPIView.as_view(), name='reset-password-api'),

]
