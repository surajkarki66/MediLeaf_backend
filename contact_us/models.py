import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from utilities.models import TimeStamp
from utilities.validators import ImageValidator


class ContactUs(TimeStamp):
    first_name = models.CharField('first name', max_length=64)
    last_name = models.CharField('last name', max_length=64)
    email = models.EmailField('email address', unique=True)
    subject = models.CharField(
        'subject', max_length=255, null=True, blank=True, default=None)
    message = CKEditor5Field()
   
    class Meta:
        verbose_name = 'ContactUs'
        verbose_name_plural = 'ContactUs'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.subject}'


User = get_user_model()

def validate_array_length(value):
    if len(value) > 5:
        raise ValidationError("Array must contain  5 or less than 5 elements")

def get_upload_to(instance, filename):
    scientific_name = slugify(instance.get_scientific_name())
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    new_filename = f"{scientific_name}_{current_datetime}_"
    image_path = f"feedback-plants/{scientific_name}/{new_filename}"

    return image_path

class Feedback(TimeStamp):
    Annual = 'annual'
    Biennial = 'biennial'
    Perennial = 'perennial'
    Ephemeral = 'ephemeral'
    Deciduous = 'deciduous'
    Evergreen = 'evergreen'

    Duration = (
        (Annual, 'Annual'),
        (Biennial, 'Biennial'),
        (Perennial, 'Perennial'),
        (Ephemeral, 'Ephemeral'),
        (Deciduous, 'Deciduous'),
        (Evergreen, 'Evergreen')
    )
    Herb = 'herb'
    Shrub = 'shrub'
    Tree = 'tree'
    Graminoid = 'graminoid'
    Subshrub = 'subshrub'
    Vine = 'vine'

    Growth = (
        (Herb, 'Herb'),
        (Shrub, 'Shrub'),
        (Tree, 'Tree'),
        (Graminoid, 'Graminoid'),
        (Subshrub, 'Subshrub'),
        (Vine, 'Vine')
    )

    common_name = models.CharField(max_length=255)
    description = CKEditor5Field()
    medicinal_properties = CKEditor5Field()
    duration = models.CharField(max_length=10, choices=Duration)
    growth_habit = models.CharField(max_length=10, choices=Growth)

    family = models.CharField('family', max_length=255)
    genus = models.CharField('genus', max_length=255)
    species = models.CharField(
        'species', max_length=255, null=True, blank=True, default=None)
    
    image = models.ImageField(upload_to=get_upload_to, validators=[
        ImageValidator(size=1000*1024)])
    
    is_verified = models.BooleanField(default=False, verbose_name='Verified')

    user = models.ForeignKey(
        User, related_name='feedback', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ('-id',)

    def get_scientific_name(self):
        if self.species is not None:
            return f'{self.genus} {self.species}'.strip()
        else:
            return f'{self.genus}'

    def __str__(self):
        if self.species is not None:
            return f'{self.genus} {self.species}'.strip()
        else:
            return f'{self.genus}'

    def image_tag(self):
        image = self.image
        if image:
            return mark_safe(
                '<a href="%s" target = "_blank"><img src ="%s" style="width: 50px; height:50px;"/></a>' %
                ("https://res.cloudinary.com/deek0shwx/image/upload/v1/" + str(image),
                 "https://res.cloudinary.com/deek0shwx/image/upload/v1/"+str(image))
            )
        else:
            return 'No Image Found'

    image.short_description = 'Image'