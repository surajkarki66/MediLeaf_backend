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
