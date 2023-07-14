from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters



from account.permissions import  IsVerifiedUser
from .models import ContactUs, Feedback
from contact_us.serializers import ContactUsSerializer, FeedbackSerializer, FeedbackListSerializer

@extend_schema(summary='ContactUs viewset', tags=['Contact us'])
class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter,]

    search_fields = ["id", "first_name", "last_name", "subject", "email"]
    ordering_fields = ["id", "first_name", "last_name", "created_at", "updated_at"]

@extend_schema(summary='Feedback Viewset', tags=['Feedbacks'])
class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated, IsVerifiedUser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter,]

    search_fields = ["id", "family", "common_names", "genus", "species",]
    ordering_fields = ["id", "common_names", "family", "genus", "species",
                        "created_at", "updated_at",]
    
    filterset_fields = {
        "id": ["exact"],
        "created_at": ["gte", "lte", "exact", "gt", "lt"],
        "updated_at": ["gte", "lte", "exact", "gt", "lt"],
        "is_verified": ["exact"],
        "user": ["exact"],
        "growth_habit": ["exact"],
        "duration": ["exact"],
    }
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]

        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackListSerializer

        return super().get_serializer_class()
    
