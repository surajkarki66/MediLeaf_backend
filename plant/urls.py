from django.urls import include, path
from rest_framework.routers import DefaultRouter

from plant import views

router = DefaultRouter()

router.register(r'plants/plant-species', views.PlantSpeciesViewset, 'plant-species')

app = 'plant'

urlpatterns = [
    path('', include(router.urls)),
]
