import os

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login
from email.mime.image import MIMEImage
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import get_template

from .serializers import SignUpSerializer, LoginSerializer
from MediLeaf_backend.email_thread import EmailThread


User = get_user_model()


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
