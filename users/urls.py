from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, base_name='profiles')
router.register(r'', UserViewSet, base_name='users')
urlpatterns = router.urls
