from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class ImageValidator:
    messages = {
        "dimensions": 'Image dimensions must be equal to %(width)s width x %(height)s height.',
        "size": "Image must be less than %(size)s kB."
    }

    def __init__(self, size=None, width=None, height=None):
        self.size = size
        self.width = width
        self.height = height

    def __call__(self, value):
        if self.size is not None and value.size >= self.size:
            raise ValidationError(
                self.messages['size'],
                params={
                    'size': float(self.size) / 1024,
                    'value': value,
                }
            )

        width = value.image.width if hasattr(value, 'image') else value.width
        height = value.image.height if hasattr(
            value, 'image') else value.height
        if (self.width is not None and self.height is not None
                and (width != self.width or height != self.height)):
            raise ValidationError(
                self.messages['dimensions'],
                params={
                    'width': self.width,
                    'height': self.height,
                    'value': value,
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.size == other.size
            and self.width == other.width
            and self.height == other.height
        )
