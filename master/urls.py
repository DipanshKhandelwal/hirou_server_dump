from .views import VehicleViewSet, CollectionPointViewSet, GarbageViewSet, ReportTypeViewSet, CustomerViewSet,\
    BaseRouteViewSet, TaskRouteViewSet, TaskCollectionPointViewSet, TaskCollectionViewSet, TaskReportViewSet, TaskAmountViewSet, TaskAmountItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vehicle', VehicleViewSet, basename='vehicle')
router.register(r'collection_point', CollectionPointViewSet, basename='collection_point')
router.register(r'garbage', GarbageViewSet, basename='garbage')
router.register(r'report_type', ReportTypeViewSet, basename='report_type')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'base_route', BaseRouteViewSet, basename='base_route')
#
router.register(r'task_route', TaskRouteViewSet, basename='task_route')
router.register(r'task_collection_point', TaskCollectionPointViewSet, basename='task_collection_point')
router.register(r'task_collection', TaskCollectionViewSet, basename='task_collection')
router.register(r'task_report', TaskReportViewSet, basename='task_report')
router.register(r'task_amount', TaskAmountViewSet, basename='task_amount')
router.register(r'task_amount_item', TaskAmountItemViewSet, basename='task_amount_item')


urlpatterns = router.urls
