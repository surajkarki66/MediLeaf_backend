from rest_framework import serializers

from .models import PlantSpecies, PlantGenus, PlantFamily, PlantImage, Plant
from utilities.utils import image_to_array


class PlantSpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = PlantSpecies
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug')


class PlantGenusSerializer(serializers.ModelSerializer):
    species = PlantSpeciesSerializer(many=True, read_only=True)

    class Meta:
        fields = ("id", "title", "slug", "family",
                  "species", "created_at", "updated_at")
        model = PlantGenus
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug', )


class PlantGenusListSerializer(serializers.ModelSerializer):
    no_of_species = serializers.ReadOnlyField()

    class Meta:
        fields = "__all__"
        model = PlantGenus
        read_only_fields = ('id', 'created_at', 'updated_at',
                            'slug', 'no_of_species')


class PlantFamilyListSerializer(serializers.ModelSerializer):
    no_of_plants = serializers.ReadOnlyField()

    class Meta:
        fields = "__all__"
        model = PlantFamily
        read_only_fields = ('id', 'created_at',
                            'updated_at', 'slug', 'no_of_plants')


class PlantFamilySerializer(serializers.ModelSerializer):
    genuses = PlantGenusSerializer(many=True, read_only=True)

    class Meta:
        fields = ("id", "title", "slug", "genuses", "created_at", "updated_at")
        model = PlantFamily
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug', )


class PlantImageSerializer(serializers.ModelSerializer):
    plant = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "plant", "part", "image",
                  "default", "created_at", "updated_at")
        model = PlantImage
        read_only_fields = ('id', 'created_at', 'updated_at', )


class PlantListSerializer(serializers.ModelSerializer):
    family = serializers.StringRelatedField(read_only=True)
    genus = serializers.StringRelatedField(read_only=True)
    species = serializers.StringRelatedField(read_only=True)
    images = PlantImageSerializer(read_only=True, many=True)

    class Meta:
        fields = ("id", "common_names", "common_names_ne", "family",
                  "genus", "species", "images", "created_at", "updated_at")
        model = Plant
        read_only_fields = ("id", "common_names", "common_names_ne", "family",
                            "genus", "species", "images", "created_at", "updated_at")


class PlantDetailsSerializer(serializers.ModelSerializer):
    family = serializers.StringRelatedField(read_only=True)
    genus = serializers.StringRelatedField(read_only=True)
    species = serializers.StringRelatedField(read_only=True)
    images = PlantImageSerializer(read_only=True, many=True)

    class Meta:
        fields = ("id", "common_names", "common_names_ne", "description", "description_ne", "medicinal_properties",
                  "medicinal_properties_ne", "duration", "growth_habit", "wikipedia_link",
                  "other_resources_links", "no_of_observations", "family", "genus",
                  "species", "images", "created_at", "updated_at")
        model = Plant


class PlantPredictionSerializer(serializers.Serializer):
    image_file = serializers.ImageField(required=True)

    def to_representation(self, instance):
        image_array = image_to_array(instance)
        return image_array.tolist()

    def validate_image_file(self, value):
        # TODO: image must have 3 channels(rgb)
        return value
