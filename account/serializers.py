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