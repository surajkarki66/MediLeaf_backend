from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.models import TimeStamp
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStamp):
    first_name = models.CharField('first name', max_length=64)
    last_name = models.CharField('last name', max_length=64)
    email = models.EmailField('email address', unique=True)
    contact = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^\+?[1-9][0-9]{7,14}$',
                message="The contact number can have + sign in the beginning and max 15 digits without delimiters")
        ]
    )
    country = CountryField(blank_label="(select country)")
    verification_link_expiration = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    is_active = models.BooleanField('active', default=True,
                                    help_text=_(
                                        "Designates whether this user should be treated as active. "
                                        "Unselect this instead of deleting accounts."
                                    ),)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text=_(
                                       "Designates whether the user can log into this admin site."),
                                   )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country',]

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-id',)
        indexes = [
            models.Index(fields=['email', 'first_name', 'last_name',]),
        ]

    def get_fullname(self):
        """
        return the first name and last name, with extra spaces removed.
        :return: The full name of the person.
        """
        return f'{self.first_name} {self.last_name}'.strip()

    def send_email(self, subject, html_message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, html_message, from_email, [
                  self.email], html_message=html_message, **kwargs)

    def __str__(self):
        return self.get_fullname()


class UserStamp(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name='%(class)s_creator')
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_updater')

    class Meta:
        abstract = True
