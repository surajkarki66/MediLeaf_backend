from rest_framework import permissions, viewsets, filters
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .models import PlantSpecies, PlantGenus, PlantFamily
from .serializers import PlantSpeciesSerializer, PlantGenusSerializer, PlantGenusListSerializer, PlantFamilyListSerializer


@extend_schema(summary='Plant Species Viewset', tags=['Plant Species'])
class PlantSpeciesViewset(viewsets.ModelViewSet):
    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer
    permission_classes = (permissions.IsAdminUser, )
    lookup_field = 'slug'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "id": ["exact"],
        "created_at": ["gte", "lte", "exact", "gt", "lt"],
        "updated_at": ["gte", "lte", "exact", "gt", "lt"],
    }
    search_fields = ["id", "title", "genus__title"]
    ordering_fields = ["id", "title", "created_at", "updated_at",]

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
        if self.action in ["create",]:
            return [permissions.IsAuthenticated(),]

        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny(),]

        return super().get_permissions()

@extend_schema(summary='Plant Genus Viewset', tags=['Plant Genus'])
class PlantGenusViewset(viewsets.ModelViewSet):
    queryset = PlantGenus.objects.all()
    serializer_class = PlantGenusSerializer
    permission_classes = (permissions.IsAdminUser, )
    lookup_field = 'slug'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "id": ["exact"],
        "created_at": ["gte", "lte", "exact", "gt", "lt"],
        "updated_at": ["gte", "lte", "exact", "gt", "lt"],
    }
    search_fields = ["id", "title", "family__title"]
    ordering_fields = ["id", "title", "created_at", "updated_at",]

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
        if self.action in ["create",]:
            return [permissions.IsAuthenticated(),]

        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny(),]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantGenusListSerializer

        return super().get_serializer_class()
            

@extend_schema(summary='Plant Family Viewset', tags=['Plant Family'])
class PlantFamilyViewset(viewsets.ModelViewSet):
    queryset = PlantFamily.objects.all()
    serializer_class = PlantFamilyListSerializer
    permission_classes = (permissions.IsAdminUser, )
    lookup_field = 'slug'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "id": ["exact"],
        "created_at": ["gte", "lte", "exact", "gt", "lt"],
        "updated_at": ["gte", "lte", "exact", "gt", "lt"],
    }
    search_fields = ["id", "title",]
    ordering_fields = ["id", "title", "created_at", "updated_at",]

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
        if self.action in ["create",]:
            return [permissions.IsAuthenticated(),]

        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny(),]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantFamilyListSerializer

        return super().get_serializer_class()
            
        


