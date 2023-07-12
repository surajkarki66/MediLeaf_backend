from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters


from .models import ContactUs
from contact_us.serializers import ContactUsSerializer

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter,]

    search_fields = ["id", "first_name", "last_name", "subject", "email"]
    ordering_fields = ["id", "first_name", "last_name", "created_at", "updated_at"]

