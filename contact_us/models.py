from django.db import models

from django_ckeditor_5.fields import CKEditor5Field
from utilities.models import TimeStamp


class ContactUs(TimeStamp):
    first_name = models.CharField('first name', max_length=64)
    last_name = models.CharField('last name', max_length=64)
    email = models.EmailField('email address', unique=True)
    subject = models.CharField(
        'subject', max_length=255, null=True, blank=True, default=None)
    description = CKEditor5Field()
   
    class Meta:
        verbose_name = 'ContactUs'
        verbose_name_plural = 'ContactUs'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.subject}'


