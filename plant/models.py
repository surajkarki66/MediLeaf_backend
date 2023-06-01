import re

from django.db import models
from utilities.models import TimeStamp
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_delete, pre_save
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.conf import settings

from utilities.utils import unique_update_slugify
from utilities.validators import ImageValidator


def get_upload_to(instance,  filename):
    scientific_name = slugify(instance.plant.get_scientific_name())
    plant_part = slugify(instance.part)
    new_filename = scientific_name + '_' + plant_part + "_"
    image_path = f"plants/{scientific_name}/{new_filename}"

    return image_path


def validate_array_length(value):
    if len(value) > 5:
        raise ValidationError("Array must contain  5 or less than 5 elements")


def validate_link(value):
    url_validator = URLValidator()

    if not value.startswith('http://') and not value.startswith('https://'):
        value = 'http://' + value

    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError('Invalid link.')


class PlantFamily(TimeStamp):
    title = models.CharField('title', max_length=100, unique=True)
    slug = models.SlugField('slug', max_length=255,
                            unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Plant Family"
        verbose_name_plural = "Plant Families"
        ordering = ('id', )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """
        If the object is being added, slugify the title and save it. If the object is being updated,
        slugify the title and check if it's unique. If it's not unique, append a number to the end of
        the slug and check again. If it's still not unique, increment the number and check again. Repeat
        until the slug is unique
        """
        self.slug = unique_update_slugify(
            self, self._state.adding, slugify(self.title))
        super(PlantFamily, self).save(*args, **kwargs)

    @property
    def no_of_plants(self):
        return self.plants.all().count()


class PlantGenus(TimeStamp):
    title = models.CharField('title', max_length=100, unique=True)
    slug = models.SlugField('slug', max_length=255,
                            unique=True, null=True, blank=True)
    family = models.ForeignKey(
        PlantFamily, on_delete=models.CASCADE, related_name='genuses')

    class Meta:
        verbose_name = "Plant Genus"
        verbose_name_plural = "Plant Genuses"
        ordering = ('id', )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """
        If the object is being added, slugify the title and save it. If the object is being updated,
        slugify the title and check if it's unique. If it's not unique, append a number to the end of
        the slug and check again. If it's still not unique, increment the number and check again. Repeat
        until the slug is unique
        """
        self.slug = unique_update_slugify(
            self, self._state.adding, slugify(self.title))
        super(PlantGenus, self).save(*args, **kwargs)

    @property
    def no_of_species(self):
        return self.genus.all().count()


class PlantSpecies(TimeStamp):
    title = models.CharField('title', max_length=100, unique=True)
    slug = models.SlugField('slug', max_length=255,
                            unique=True, null=True, blank=True)
    genus = models.ForeignKey(
        PlantGenus, on_delete=models.CASCADE, related_name='species')

    class Meta:
        verbose_name = "Plant Species"
        verbose_name_plural = "Plant Species"
        ordering = ('id', )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """
        If the object is being added, slugify the title and save it. If the object is being updated,
        slugify the title and check if it's unique. If it's not unique, append a number to the end of
        the slug and check again. If it's still not unique, increment the number and check again. Repeat
        until the slug is unique
        """
        self.slug = unique_update_slugify(
            self, self._state.adding, slugify(self.title))
        super(PlantSpecies, self).save(*args, **kwargs)


class Plant(TimeStamp):
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

    common_name = ArrayField(models.CharField(
        max_length=255, unique=True), size=5, unique=True, validators=[validate_array_length])
    common_name_ne = ArrayField(models.CharField(
        max_length=255, unique=True), size=5, unique=True, validators=[validate_array_length])
    description = CKEditor5Field()
    description_ne = CKEditor5Field()
    medicinal_properties = CKEditor5Field()
    medicinal_properties_ne = CKEditor5Field()
    duration = models.CharField(max_length=10, choices=Duration)
    growth_habit = models.CharField(max_length=10, choices=Growth)
    wikipedia_link = models.CharField(
        'wikipedia_link', max_length=500, null=True, blank=True, default=None, validators=[validate_link])
    other_resources_links = ArrayField(models.CharField(validators=[
                                       validate_link]), size=5, null=True, blank=True, validators=[validate_array_length])
    no_of_observations = models.PositiveIntegerField(default=0, editable=False)
    family = models.ForeignKey(
        PlantFamily, related_name='plants', on_delete=models.PROTECT)
    genus = models.ForeignKey(
        PlantGenus, related_name='genus', on_delete=models.PROTECT)
    species = models.ForeignKey(PlantSpecies, related_name='species',
                                null=True, blank=True, default=None, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Plant'
        verbose_name_plural = 'Plants'
        ordering = ('-id',)

    def get_scientific_name(self):
        return f'{self.genus} {self.species}'.strip()

    def __str__(self):
        return f'{self.genus} {self.species}'.strip()

    def default_image_tag(self):
        default_image = self.images.get(default=True)
        if default_image:
            return mark_safe(
                '<a href="%s" target = "_blank"><img src ="%s" style="width: 50px; height:50px;"/></a>' %
                ("https://res.cloudinary.com/deek0shwx/image/upload/v1/" + str(default_image),
                 "https://res.cloudinary.com/deek0shwx/image/upload/v1/"+str(default_image))
            )
        else:
            return 'No Image Found'

    default_image_tag.short_description = 'Default Image'


class PlantImage(TimeStamp):
    Flower = 'flower'
    Leaf = 'leaf'
    Fruit = 'fruit'
    Bark = 'bark'
    Other = 'other'

    Part = (
        (Flower, 'Flower'),
        (Leaf, 'Leaf'),
        (Fruit, 'Fruit'),
        (Bark, 'Bark'),
        (Other, 'Other')
    )

    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name='images')
    part = models.CharField(max_length=7, choices=Part)
    image = models.ImageField(upload_to=get_upload_to, validators=[
        ImageValidator(size=1000*1024)])
    default = models.BooleanField(default=False)

    def image_tag(self):
        if self.image:
            return mark_safe(
                '<a href="%s" target = "_blank"><img src ="%s" style="width: 50px; height:50px;"/></a.' %
                (self.image.url, self.image.url)
            )
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = 'Plant Image'
        verbose_name_plural = 'Plant Images'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.image}'
