from .views import VehicleViewSet, CollectionPointViewSet, GarbageViewSet, PickupViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vehicle', VehicleViewSet, base_name='vehicle')
router.register(r'collection_point', CollectionPointViewSet, base_name='collection_point')
router.register(r'garbage', GarbageViewSet, base_name='garbage')
router.register(r'pickup', PickupViewSet, base_name='pickup')

urlpatterns = router.urls
