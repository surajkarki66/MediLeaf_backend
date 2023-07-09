from django.urls import include, path
from rest_framework.routers import DefaultRouter

from plant import views

router = DefaultRouter()

router.register(r'plants', views.PlantViewset, 'plant')
router.register(r'plants/plant-species',
                views.PlantSpeciesViewset, 'plant-species')
router.register(r'plants/plant-genus', views.PlantGenusViewset, 'plant-genus')
router.register(r'plants/plant-family',
                views.PlantFamilyViewset, 'plant-family')
router.register(r'plants/plant-images',
                views.PlantImageViewset, 'plant-images')

app = 'plant'

urlpatterns = [
    path('', include(router.urls)),
    path('plant/details/',
         views.PlantDetailsAPIView.as_view(), name='plant-detail')
]
