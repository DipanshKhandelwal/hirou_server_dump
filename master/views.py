from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action

from .serializers import VehicleSerializer, CollectionPointSerializer, GarbageSerializer, CustomerSerializer, BaseRouteSerializer, BaseRouteListSerializer, TaskRouteSerializer, TaskCollectionPointSerializer, TaskCollectionSerializer, ReportTypeSerializer, TaskReportSerializer, TaskReportListSerializer, TaskAmountSerializer
from .models import Vehicle, CollectionPoint, Garbage, ReportType, Customer, BaseRoute, TaskRoute, TaskCollectionPoint, TaskCollection, TaskReport, TaskAmount
from rest_framework.response import Response


class VehicleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vehicle instances.
    """
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    # def perform_update(self, serializer):
    #     vehicle = self.get_object()
    #     users = list(vehicle.users.all())
    #     users = [str(x.id) for x in users]
    #     data_users = self.request.data.get('users')
    #     user_id = str(self.request.user.id)
    #     if data_users:
    #         if int(user_id) in data_users:
    #             if user_id not in users:
    #                 users.append(user_id)
    #         else:
    #             if user_id in users:
    #                 users.remove(user_id)
    #     serializer.save(users=users)


class CollectionPointViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing collection point instances.
    """
    serializer_class = CollectionPointSerializer
    queryset = CollectionPoint.objects.all()


class GarbageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing garbage instances.
    """
    serializer_class = GarbageSerializer
    queryset = Garbage.objects.all()


class ReportTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing report type instances.
    """
    serializer_class = ReportTypeSerializer
    queryset = ReportType.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class BaseRouteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing base route instances.
    """
    # serializer_class = BaseRouteSerializer
    queryset = BaseRoute.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseRouteListSerializer

        if self.action == 'retrieve':
            return BaseRouteListSerializer

        return BaseRouteSerializer


# 
class TaskRouteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task route instances.
    """
    serializer_class = TaskRouteSerializer
    queryset = TaskRoute.objects.all()

    def get_queryset(self):
        queryset = TaskRoute.objects.all()
        date = self.request.query_params.get('date', None)

        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def perform_create(self, serializer):
        base_route_id = self.request.data["id"]
        new_task_name = self.request.data["name"]
        route = BaseRoute.objects.get(id=base_route_id)
        new_task_route = TaskRoute(name=new_task_name)
        new_task_route.customer = route.customer

        new_task_route.save()

        garbages = route.garbage.all()
        new_task_route.garbage.add(*garbages)

        collection_points = route.collection_point.all()

        for cp in collection_points:
            new_task_collection_point = TaskCollectionPoint()
            new_task_collection_point.location = cp.location
            new_task_collection_point.route = new_task_route
            new_task_collection_point.name = cp.name
            new_task_collection_point.address = cp.address
            new_task_collection_point.memo = cp.memo
            new_task_collection_point.sequence = cp.sequence
            new_task_collection_point.image = cp.image
            new_task_collection_point.save()

            for garbage in garbages:
                new_collection = TaskCollection()
                new_collection.collection_point = new_task_collection_point
                new_collection.garbage = garbage
                new_collection.save()
                new_task_collection_point.task_collection.add(new_collection)

            new_task_route.task_collection_point.add(new_task_collection_point)

        new_task_route.save()


class TaskCollectionPointViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task collection point instances.
    """
    serializer_class = TaskCollectionPointSerializer
    queryset = TaskCollectionPoint.objects.all()

    @action(detail=True, methods=['patch'])
    def bulk_complete(self, request, pk=None):
        task_c_p = self.get_object()
        complete = True
        for tc in task_c_p.task_collection.all():
            if not tc.complete:
                complete = False
                break

        for tc in task_c_p.task_collection.all():
            if not complete:
                tc.complete = True
                tc.timestamp = timezone.now()
                tc.available = False
            else:
                tc.complete = False
                tc.timestamp = None
                tc.amount = 0

            tc.save()

        return Response(TaskCollectionSerializer(task_c_p.task_collection.all(), many=True).data)


class TaskCollectionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task collection instances.
    """
    serializer_class = TaskCollectionSerializer
    queryset = TaskCollection.objects.all()


class TaskReportViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task report instances.
    """
    queryset = TaskReport.objects.all()

    def get_queryset(self):
        queryset = TaskReport.objects.all()
        task_route = self.request.query_params.get('task_route', None)

        if task_route:
            queryset = queryset.filter(route=task_route)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskReportListSerializer

        return TaskReportSerializer


class TaskAmountViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task amount instances.
    """
    serializer_class = TaskAmountSerializer
    queryset = TaskAmount.objects.all()

    def get_queryset(self):
        queryset = TaskAmount.objects.all()
        task_route = self.request.query_params.get('task_route', None)

        if task_route:
            queryset = queryset.filter(route=task_route)

        return queryset
