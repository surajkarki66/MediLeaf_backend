import os
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

from utilities.validators import ImageValidator
from utilities.models import TimeStamp
from utilities.utils import unique_update_slugify

User = get_user_model()


def get_upload_to(instance,  filename):
    """
    The function accepts a model instance and filename and generates
    a slugified path to the file based on Profile User Fullname. 

    :param instance: The instance of the model where the ImageField is being defined. In this case, since
    Profile is a model, instance will be an instance of that model (an object)
    :param filename: The name of the file that was uploaded
    :return: The path to the file.
    """
    _, image_extension = os.path.splitext(instance.avatar.path)
    image_path = 'avatars/'
    username = slugify(instance.user.get_fullname())
    new_filename = username + '_300x300' + image_extension
    return os.path.join(image_path, new_filename)


class Profile(TimeStamp):
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=get_upload_to,
        null=True, blank=True,
        validators=[ImageValidator(width=300, height=300, size=500*1024)],
    )
    facebook = models.CharField(
        'facebook', max_length=255, null=True, blank=True, default=None)
    instagram = models.CharField(
        'instagram', max_length=255, null=True, blank=True, default=None)
    linkedIn = models.CharField(
        'linkedIn', max_length=500, null=True, blank=True, default=None)
    twitter = models.CharField(
        'twitter', max_length=500, null=True, blank=True, default=None)

    def image_tag(self):
        if self.avatar:
            return mark_safe(
                '<a href="%s" target = "_blank"><img src ="%s" style="width: 50px; height:50px;"/></a.' %
                (self.avatar.url, self.avatar.url)
            )
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.email}'

    def save(self, *args, **kwargs):
        """
        If the object is being added to the database, then slugify the user field and save it to the
        slug field. If the object is being updated, then slugify the user field and check if the slug is
        unique. If it is, then save it to the slug field. If it isn't, then append a random string to
        the end of the slug and check if that is unique. If it is, then save it to the slug field. If it
        isn't, then repeat the process until a unique slug is found
        """
        self.slug = unique_update_slugify(
            self, self._state.adding, slugify(self.user.get_fullname()))
        super(Profile, self).save(*args, **kwargs)
