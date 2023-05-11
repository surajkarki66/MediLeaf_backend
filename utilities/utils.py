from django.utils.crypto import get_random_string


def unique_update_slugify(instance, created,slug):
    """
    If the object is created, check if the slug exists in the database, if it does, add a random string
    to the end of the slug. If the object is not created, check if the slug exists in the database, if
    it does, add a random string to the end of the slug
    
    :param instance: The instance of the model that is being saved
    :param created: True if the object is being created, False if it's being updated
    :param slug: The slug you want to use
    :return: A unique slug
    """
    model = instance.__class__
    unique_slug = slug
    if created:
        while model.objects.filter(slug=unique_slug).exists():
            unique_slug = slug +"-"+ get_random_string(length=4)
    else:
        while model.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
            unique_slug = slug +"-"+ get_random_string(length=4)
    return unique_slug