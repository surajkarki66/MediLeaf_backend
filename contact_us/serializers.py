from rest_framework import serializers
from .models import ContactUs, Feedback


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    common_names = serializers.ListField(
        child=serializers.CharField(), required=True)

    class Meta:
        model = Feedback
        fields = ("id", "common_names", "description", "medicinal_properties", "duration", "growth_habit", "family",
                  "genus", "species", "image", "user", "created_at", "updated_at")


class FeedbackListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ("id", "common_names", "family",
                  "genus", "species", "image", "user", "created_at", "updated_at")
        model = Feedback
        read_only_fields = ("id", "common_names", "family", "genus",
                            "species", "image", "user", "created_at", "updated_at")
