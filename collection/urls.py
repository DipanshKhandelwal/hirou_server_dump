from .views import VehicleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, base_name='vehicles')
urlpatterns = router.urls

