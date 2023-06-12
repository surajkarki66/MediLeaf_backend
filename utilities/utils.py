import numpy as np

from django.utils.crypto import get_random_string
from PIL import Image as PILImage


def unique_update_slugify(instance, created, slug):
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
            unique_slug = slug + "-" + get_random_string(length=4)
    else:
        while model.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
            unique_slug = slug + "-" + get_random_string(length=4)
    return unique_slug


def image_to_array(image_instance):
    image = PILImage.open(image_instance)
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


def map_predictions_to_species_with_proba(predictions):
    class_indices = {
        0: 'Amaranthus Viridis',
        1: 'Basella Alba',
        2: 'Piper Betle',
        3: 'Tabernaemontana Divaricata',
        4: 'Murraya Koenigii',
        5: 'Moringa Oleifera',
        6: 'Trigonella Foenum-graecum',
        7: 'Psidium Guajava',
        8: 'Hibiscus Rosa-sinensis',
        9: 'Pongamia Pinnata',
        10: 'Brassica Juncea',
        11: 'Artocarpus Heterophyllus',
        12: 'Muntingia Calabura',
        13: 'Syzygium Cumini',
        14: 'Jasminum',
        15: 'Carissa Carandas',
        16: 'Citrus Limon',
        17: 'Mangifera Indica',
        18: 'Plectranthus Amboinicus',
        19: 'Mentha',
        20: 'Azadirachta Indica',
        21: 'Nerium Oleander',
        22: 'Nyctanthes Arbor-tristis',
        23: 'Ficus Religiosa',
        24: 'Punica Granatum',
        25: 'Alpinia Galanga',
        26: 'Syzygium Jambos',
        27: 'Ficus Auriculata',
        28: 'Santalum Album',
        29: 'Ocimum Tenuiflorum'
    }
    predictions = predictions[0]
    predicted_class_indices = np.argsort(predictions)[::-1][:3]
    predicted_classes_with_probs = [
        {"species": class_indices[i], "probability": float(predictions[i])}
        for i in predicted_class_indices
    ]

    return predicted_classes_with_probs
