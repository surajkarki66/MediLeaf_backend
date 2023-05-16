from django.contrib.auth import authenticate, get_user_model
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class SignUpSerializer(CountryFieldMixin, serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',
                  'confirm_password', 'contact', 'country',)
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
            'country': {'required': True},
            'contact': {'required': False}
        }

    def validate(self, attrs):
        """
        If the password and confirm_password fields don't match, raise a validation error

        :param attrs: The validated data from the serializer
        :return: The validated data.
        """
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({
                'password': ["The two password fields didn't match."]
            })
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ('email', 'password', 'is_verified')
        read_only_fields = ('is_verified', )

    def validate(self, attrs):
        """
        It checks if the user exists, if the user is active and verified, and if the password is correct

        :param attrs: The validated data from the serializer
        :return: The user object is being returned.
        """
        authenticate_kwargs = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        account = User.objects.filter(email=attrs.get('email'))
        if not account.exists():
            raise ValidationError(
                {'message': 'No account found with this email.'
                 })

        # user = account.first()
        # if not (user.is_active and user.is_verified):
        #     raise ValidationError({
        #         'is_verified': user.is_verified,
        #         'message': 'Please verify your email before login.'
        #     })

        user = authenticate(**authenticate_kwargs)
        if user is None:
            raise ValidationError({
                'message': 'Incorrect email or password.'
            })
        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(
        max_length=128, write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(
        max_length=128, write_only=True, required=True)

    class Meta:
        fields = ('old_password', 'new_password', 'confirm_new_password')

    def validate(self, attrs):
        """
        If the old password is correct, and the new password is not the same as the old password, and
        the new password and the confirm new password match, and the new password is valid, then return
        the attributes

        :param attrs: The validated data from the serializer
        :return: The validated data is being returned.
        """
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise ValidationError({
                'message': 'The old password you have entered is incorrect'
            })
        if attrs['old_password'] == attrs['new_password']:
            raise ValidationError({
                'message': ['You have entered the same password as old password']
            })

        if attrs['new_password'] != attrs['confirm_new_password']:
            raise ValidationError({
                'message': ["The two password fields didn't match."]
            })
        validate_password(attrs['new_password'], self.context['request'].user)
        return attrs

class UserUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'contact', 'country',)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False)
    class Meta:
        fields = ('email', )

    def validate_email(self, value):
        """
        If the email does not exist in the database, raise a validation error
        
        :param value: The value that is being validated
        :return: The value of the email address.
        """
        if not User.objects.filter(email=value).exists():
            raise ValidationError({
                'message': ['Email does not exist. Please try again with valid email address.']
            })
        return value

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    class Meta:
        fields = ('new_password', 'confirm_new_password')

    def validate(self, attrs):
        """
        If the new password and the confirm new password fields don't match, raise a validation error
        
        :param attrs: The validated data from the serializer
        :return: The attrs dictionary is being returned.
        """
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise ValidationError({
                'message': ["The two password fields didn't match."]
            })
        validate_password(attrs['new_password'])
        return attrs

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False)
    class Meta:
        fields = ['email']

    def validate_email(self, value):
        """
        If the email does not exist in the database, raise a validation error
        
        :param value: The value that is being validated
        :return: The value of the email address.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({
                'message': ['Email does not exist. Please try again with valid email address.']
            })
        return value
