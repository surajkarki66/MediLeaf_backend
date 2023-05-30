from rest_framework import permissions, viewsets, filters
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .models import PlantSpecies
from .serializers import PlantSpeciesSerializer


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
    ordering_fields = ["id", "title", "created_at", "updated_at", "genus"]

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


