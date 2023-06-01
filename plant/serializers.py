from rest_framework import serializers

from .models import PlantSpecies, PlantGenus, PlantFamily


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
