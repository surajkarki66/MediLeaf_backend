from django.urls import path

from .views import SignUpAPIView, LoginAPIView, LogoutAPIView, PasswordChangeAPIView, me, ForgotPasswordAPIView, ResetPasswordTokenCheckAPIView, VerifyAccountAPIView, ResendVerificationAPIView, UserUpdateAPIView, GetCSRFTokenView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('login/', LoginAPIView.as_view(), name='login-api'),
    path('logout/', LogoutAPIView.as_view(), name='logout-api'),
    path('me/', me, name='me'),
    path('verify/<slug:uid>/<slug:token>/',
         VerifyAccountAPIView.as_view(), name="account-verify"),
    path('resend/verification/email/', ResendVerificationAPIView.as_view(),
         name='resend-verification-email-api'),
    path('password/change/', PasswordChangeAPIView.as_view(),
         name='password-change-api'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(),
         name='forgot-password-api'),
    path('reset-password/<slug:uidb64>/<slug:token>/',
         ResetPasswordTokenCheckAPIView.as_view(), name='reset-password-api'),
    path('user-update/<int:pk>/',
         UserUpdateAPIView.as_view(), name='user-update-api'),
    path('csrf/', GetCSRFTokenView.as_view(), name='csrf-api'),

]
