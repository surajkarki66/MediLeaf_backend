import os

from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.contrib.auth import get_user_model, login, logout, authenticate
from email.mime.image import MIMEImage
from django.db import transaction
from django.utils import timezone, encoding
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.timezone import get_current_timezone
from rest_framework.decorators import api_view, permission_classes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import get_template
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist

from .permissions import IsOwnerOrReadOnly, IsVerifiedUser
from .serializers import SignUpSerializer, LoginSerializer, PasswordChangeSerializer, UserUpdateSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, ResendVerificationEmailSerializer
from userprofile.serializers import ProfileUpdateSerializer, UserProfileSerializer
from MediLeaf_backend.email_thread import EmailThread


User = get_user_model()
tz = get_current_timezone()


@extend_schema(summary='Get CSRF Token', tags=['CSRF'])
def get_csrf(request):
    csrf_token = get_token(request)
    response = JsonResponse({"csrfToken": csrf_token})
    return response


@extend_schema(summary='User signup', tags=['Account'])
class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def send_email(self, user):
        """
        It sends an email to the user with a link to verify their account

        :param user: The user object that is being sent the email
        """
        mail_subject = 'Verify your MediLeaf Account'
        email_from = settings.EMAIL_HOST_USER

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user=user)

        img_path = os.path.join(settings.MEDIA_ROOT, 'logo/MediLeafLogo.png')

        if not os.path.exists(img_path):
            raise ParseError({
                'message': 'Image not found'
            })

        with open(img_path, 'rb') as image_file:
            image_data = image_file.read()

        template = get_template('account/signupVerification.html')

        app_domain = settings.SITE_DOMAIN

        context = {
            'user': user,
            'app_domain': app_domain,
            'link': f"{app_domain}/verify/{uid}/{token}"
        }
        html_message = template.render(context)
        msg = EmailMultiAlternatives(
            mail_subject, html_message, email_from, [user.email]
        )
        msg.attach_alternative(html_message, 'text/html')
        img = MIMEImage(image_data, 'png')
        img.add_header('Content-Id', '<medileaf_logo>')
        img.add_header('Content-Disposition', 'inline')
        msg.attach(img)
        EmailThread(msg).start()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        It creates a user and sends a verification email to the user

        :param request: The request object
        :return: A response object is being returned.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.verification_link_expiration = timezone.now() + timezone.timedelta(hours=24)
        user.save()

        x, y = Group.objects.get_or_create(name='user')
        user.groups.add(x)
        self.send_email(user,)

        return Response({
            'message': "We have sent a verification link to your email address. Please verify your account."
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    @extend_schema(summary="User Login", tags=["Account"])
    def post(self, request):
        """
        The function takes in a request, validates the request, logs the user in, and returns a response

        :param request: The request object
        :return: The response is returning a message and the expiration date of the session.
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        expired_date = str(request.session.get_expiry_date())
        return Response({
            'message': 'Login Successful',
            'expired_date': expired_date,
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(summary="User Logout", tags=["Account"])
    def post(self, request):
        """
        It logs out the user and flushes the session

        :param request: The request object
        :return: A response object with a message and a status code.
        """
        logout(request)
        return Response({
            'message': 'User logged out successfully'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
@extend_schema(summary="User password change", tags=["Account"])
class PasswordChangeAPIView(generics.CreateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        """
        It takes the user's new password, sets it as the user's password, logs the user out, and then
        logs the user back in with the new password

        :param request: The request object
        :return: A response object with a message and a status code.
        """
        user = request.user
        if not user.is_verified:
            return Response({
                'message': 'Please verify your account.'
            }, status=status.HTTP_400_BAD_REQUEST)
        context = {'request': request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        logout(request)
        user = authenticate(username=user.email,
                            password=serializer.validated_data['new_password'])
        if user is not None:
            login(request, user)

        return Response({
            'message': 'password successfully changed'
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def me(request):
    """
    Return the full name of the authenticated user if the request is authenticated,
    or an error response if not.

    Request parameters:
    - request: the HTTP request object.

    Response:
    - 200 OK: the full name of the authenticated user.
    - 401 UNAUTHORIZED: if the request is not authenticated.

    Notes:
    - This view requires authentication to access the user information.
    """

    if request.user.is_authenticated:
        try:
            avatar = "https://res.cloudinary.com/deek0shwx/image/upload/v1/" + \
                str(request.user.profile.avatar)
            return Response({"status": "success", "fullName": request.user.get_fullname(), "avatar": avatar}, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"status": "success", "fullName": request.user.get_fullname()}, status.HTTP_200_OK)

    else:
        return Response({"status": "fail"}, status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_protect, name='dispatch')
@extend_schema(summary="Forgot password", tags=["Account"])
class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def send_email(self, uidb64: str, token: str, user):
        """
        It sends an email to the user with a link to reset their password

        :param uidb64: The base64 encoded user id
        :type uidb64: str
        :param token: The token generated by the django.contrib.auth.tokens.PasswordResetTokenGenerator
        :type token: str
        :param user: The user object
        """
        subject = 'MediLeaf Account password reset instructions.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        img_path = os.path.join(settings.MEDIA_ROOT, 'logo/MediLeafLogo.png')

        if not os.path.exists(img_path):
            raise ParseError({
                'message': 'Image not found'
            })

        with open(img_path, 'rb') as image_file:
            image_data = image_file.read()

        template = get_template('account/forget_password_email.html')

        app_domain = settings.SITE_DOMAIN
        absurl = f"{app_domain}/reset-password/{uidb64}/{token}"
        context = {
            'user': user,
            'link': absurl,
            'app_domain': app_domain
        }
        html_message = template.render(context)
        msg = EmailMultiAlternatives(
            subject, html_message, email_from, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        img = MIMEImage(image_data, 'png')
        img.add_header('Content-Id', '<medileaf_logo>')
        img.add_header('Content-Disposition', 'inline')
        msg.attach(img)
        EmailThread(msg).start()

    def post(self, request):
        """
        It takes the email address of the user, creates a token and sends an email to the user with a
        link to reset their password

        :param request: The request object
        :return: A response object with a message and a status code.
        """
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.get(email=email)

        if not user.is_verified:
            return Response({
                'message': 'Please verify your account.'
            }, status=status.HTTP_400_BAD_REQUEST)

        uidb64 = urlsafe_base64_encode(encoding.force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        self.send_email(uidb64, token, user)

        return Response({
            'message': 'We have sent password reset link to email, Please check your email address.'
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordTokenCheckAPIView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    @extend_schema(summary="Verify user token and uuid", tags=["Account"])
    def get(self, request, uidb64, token):
        """
        It checks if the user exists, if the token is valid, and if the token is expired

        :param request: The request object
        :param uidb64: The base64-encoded integer representation of the user's primary key
        :param token: The token generated by the PasswordResetTokenGenerator
        """
        try:
            id = encoding.smart_str(urlsafe_base64_decode(uidb64))
            if User.objects.filter(id=id).exists():
                user = User.objects.get(id=id)
            else:
                return Response({
                    'message': 'User is not found.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message': 'token is not valid, please create the new one',
                    'result': {
                        'is_valid': False,
                        'email': user.email, 'is_expired': True
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Credential valid',
                'result': {
                    'is_valid': True,
                    'email': user.email,
                    'is_expired': False,
                    'uidb64': uidb64,
                    'token': token
                }
            }, status=status.HTTP_200_OK)

        except encoding.DjangoUnicodeDecodeError as identifier:
            return Response({
                'message': 'token is invalid, please create the new one',
                'result': {
                    'is_valid': False,
                    'is_expired': False
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Reset user password", tags=["Account"])
    def post(self, request, *args, **kwargs):
        """
        The function takes in a request, checks if the request is valid, if it is, it checks if the
        token is valid, if it is, it sets the password and sends an email to the user

        :param request: The request object
        :return: A response object is being returned.

        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = self.kwargs.get('token')
            uidb64 = self.kwargs.get('uidb64')
            uid = encoding.smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            if user is not None and PasswordResetTokenGenerator().check_token(user, token):
                confirm_password = serializer.validated_data.get(
                    'confirm_new_password')
                user.set_password(confirm_password)
                user.save()

        except:
            return Response({
                'message': 'Password reset failed.'
            }, status=status.HTTP_400_BAD_REQUEST)

        subject = 'Your password has been successfully reset/set.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        img_path = os.path.join(settings.MEDIA_ROOT, 'logo/MediLeafLogo.png')

        if not os.path.exists(img_path):
            raise ParseError({
                'message': 'Image not found'
            })

        with open(img_path, 'rb') as image_file:
            image_data = image_file.read()

        template = get_template('account/password_reset_success.html')

        app_domain = settings.SITE_DOMAIN
        absurl = f"{app_domain}/login/"
        context = {
            'user': user,
            'link': absurl,
            'app_domain': app_domain
        }
        content = template.render(context)
        msg = EmailMultiAlternatives(
            subject, content, email_from, recipient_list)
        msg.attach_alternative(content, "text/html")
        img = MIMEImage(image_data, 'png')
        img.add_header('Content-Id', '<medileaf_logo>')
        img.add_header('Content-Disposition', 'inline')
        msg.attach(img)
        EmailThread(msg).start()

        return Response({
            'message': 'Your password has been successfully reset/set.'
        }, status=status.HTTP_201_CREATED)


class VerifyAccountAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    @extend_schema(summary="User account verify", tags=["Account"])
    def get(self, request, uid, token, *args, **kwargs):
        """
        It checks if the user exists, if the token is valid, if the user is already verified, and if
        not, it sets the user to active and verified

        :param request: The request object
        :param uid: The user id of the user who is trying to verify their account
        :param token: The token that was sent to the user's email
        :return: A response object with a message and a status code.
        """
        try:
            user = User.objects.get(id=urlsafe_base64_decode(uid).decode())
            valid = PasswordResetTokenGenerator().check_token(user, token)
            if not valid:
                raise User.DoesNotExist

            context = {
                'success': True,
                'message': 'User verification successfully. Thank you for verifying.'
            }

        except User.DoesNotExist:
            context = {
                'success': False,
                'message': 'User verification unsuccessful, please check if you clicked the correct link.'
            }
        except UnicodeDecodeError:
            context = {
                'success': False,
                'message': 'User verification unsuccessful, invalid uid'
            }

        else:
            if (user.is_active and user.is_verified):
                context = {
                    'success': False,
                    'message': f'The account has already been verified.'
                }
            else:
                user.is_active = True
                user.is_verified = True
                user.save()
        return Response(context, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
@extend_schema(summary='Resend verification email', tags=['Account'])
class ResendVerificationAPIView(APIView):
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = (permissions.AllowAny,)

    def send_email(self, uidb64: str, token: str, user):
        """
        It sends an email to the user with a link to verify their account

        :param uidb64: The base64 encoded user id
        :type uidb64: str
        :param token: The token generated by the django.contrib.auth.tokens.PasswordResetTokenGenerator
        :type token: str
        :param user: The user object
        """
        subject = 'MediLeaf Account verification instructions.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        # Get image path from mediafiles
        img_path = os.path.join(settings.MEDIA_ROOT, 'logo/MediLeafLogo.png')

        # Check if the image exists
        if not os.path.exists(img_path):
            raise Http404('Image not found')

        # Open the image file as binary
        with open(img_path, 'rb') as image_file:
            image_data = image_file.read()

        template = get_template('account/signupVerification.html')
        app_domain = settings.SITE_DOMAIN
        absurl = f"{app_domain}/verify/{uidb64}/{token}"

        context = {
            'user': user,
            'link': absurl,
            'app_domain': app_domain
        }
        html_message = template.render(context)
        msg = EmailMultiAlternatives(
            subject, html_message, email_from, recipient_list)
        msg.attach_alternative(html_message, "text/html")
        img = MIMEImage(image_data, 'png')
        img.add_header('Content-Id', '<medileaf_logo>')
        img.add_header('Content-Disposition', 'inline')
        msg.attach(img)
        msg.send()
        EmailThread(msg).start()

    def post(self, request, *args, **kwargs):
        """
        We are creating a serializer object with the data that we received from the request. 

        We are validating the data and raising an exception if the data is not valid. 

        We are getting the email from the validated data. 

        We are getting the user object from the email. 

        We are encoding the user id and creating a token. 

        We are sending the email to the user. 

        We are returning a response to the user.

        :param request: The request object
        :return: A response with a message and a status code of 200.
        """
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.get(email=email)

        uidb64 = urlsafe_base64_encode(encoding.force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        self.send_email(uidb64, token, user)

        return Response({
            'message': 'We have sent verification link to your email. Please check your email address.'
        }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name='dispatch')
@extend_schema(summary="User Update", tags=["Account"])
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly, IsVerifiedUser,)
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        """
        :param request: The request object
        :return: The serializer.data is being returned.
        """
        """
        :param request: The request object
        :return: The serializer.data is being returned.
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.serializer_class(
            instance, data=request.data, partial=partial)

        if serializer.is_valid():
            user = serializer.save(updated_at=datetime.now(tz=tz))
        else:
            raise ParseError({
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        if hasattr(user, 'profile'):
            profile_instance = user.profile
            profile_serializer = ProfileUpdateSerializer(
                profile_instance, data=request.data, partial=partial)
        else:
            data = request.data
            if hasattr(data, '_mutable'):
                data._mutable = True

            data['user'] = instance.id
            profile_serializer = ProfileUpdateSerializer(data=data)

        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            raise ParseError({
                'message': profile_serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        serializer = UserProfileSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
