from rest_framework import serializers

from .models import PlantSpecies

class PlantSpeciesSerializer(serializers.ModelSerializer):
   
    class Meta:
        fields = "__all__"
        model = PlantSpecies
        read_only_fields = ('created_at', 'updated_at', 'slug')