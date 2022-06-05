from rest_framework import serializers
from .models import Vehicle, CollectionPoint, Garbage, ReportType, Customer, BaseRoute, TaskRoute, TaskCollectionPoint,\
    TaskCollection, TaskReport, TaskAmount, TaskAmountItem
from users.serializers import UserSerializer
from django.utils import timezone


class GarbageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garbage
        fields = ['id', 'name', 'description']


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ['id', 'name', 'description']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    # pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = Vehicle
        fields = ['id', 'registration_number', 'model']


class CollectionPointSerializer(serializers.ModelSerializer):
    # pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'location', 'address', 'memo', 'route', 'sequence', 'image']


class BaseRouteListSerializer(serializers.ModelSerializer):
    # collection_point = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='collection_point-detail')
    # collection_point = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    collection_point = CollectionPointSerializer(read_only=True, many=True)
    garbage = GarbageSerializer(read_only=True, many=True)
    customer = CustomerSerializer()
    # garbage = GarbageSerializer(many=True)

    class Meta:
        model = BaseRoute
        fields = ['id', 'name', 'customer', 'collection_point', 'garbage']


class BaseRouteNameListSerializer(serializers.ModelSerializer):
    garbage = GarbageSerializer(read_only=True, many=True)
    customer = CustomerSerializer(read_only=True)
    collection_point = serializers.SerializerMethodField('get_empty_tcp_list')

    @staticmethod
    def get_empty_tcp_list(obj):
        return []

    class Meta:
        model = BaseRoute
        fields = ['id', 'name', 'customer', 'collection_point', 'garbage']


class BaseRouteSerializer(serializers.ModelSerializer):
    # collection_point = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='collection_point-detail')
    # collection_point = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    collection_point = CollectionPointSerializer(read_only=True, many=True)
    # garbage = GarbageSerializer(read_only=True, many=True)
    # customer = CustomerSerializer()
    # garbage = GarbageSerializer(many=True)

    class Meta:
        model = BaseRoute
        fields = ['id', 'name', 'customer', 'collection_point', 'garbage']


class TaskCollectionSerializer(serializers.ModelSerializer):
    garbage = GarbageSerializer(read_only=True)
    timestamp = serializers.SerializerMethodField()
    users = UserSerializer(read_only=True)

    @staticmethod
    def get_timestamp(obj):
        if obj.timestamp is None:
            return None
        return obj.timestamp.ctime()

    class Meta:
        model = TaskCollection
        read_only_fields = ['id', 'users', 'timestamp']
        fields = ['id', 'collection_point', 'timestamp', 'complete', 'amount', 'image', 'users', 'vehicle', 'garbage', 'available']

    def update(self, instance, validated_data):
        super(TaskCollectionSerializer, self).update(instance, validated_data)

        if validated_data.get('complete', None) is not None:
            if validated_data.get('complete'):
                instance.complete = True
                instance.timestamp = timezone.now()
                instance.available = False
            else:
                instance.complete = False
                instance.timestamp = None
                instance.amount = 0
        instance.save()
        return instance


class TaskCollectionListSerializer(serializers.ModelSerializer):
    garbage = GarbageSerializer(read_only=True)
    timestamp = serializers.SerializerMethodField()

    @staticmethod
    def get_timestamp(obj):
        if obj.timestamp is None:
            return None
        return obj.timestamp.ctime()

    class Meta:
        model = TaskCollection
        fields = ['id', 'collection_point', 'timestamp', 'complete', 'amount', 'image', 'users', 'vehicle', 'garbage', 'available']


class TaskCollectionPointSerializer(serializers.ModelSerializer):
    task_collection = TaskCollectionListSerializer(read_only=True, many=True)

    class Meta:
        model = TaskCollectionPoint
        fields = ['id', 'name', 'location', 'address', 'memo', 'route', 'sequence', 'image', 'task_collection']


class TaskRouteSerializer(serializers.ModelSerializer):
    task_collection_point = TaskCollectionPointSerializer(read_only=True, many=True)
    customer = CustomerSerializer(read_only=True)
    garbage = GarbageSerializer(read_only=True, many=True)

    class Meta:
        model = TaskRoute
        fields = ['id', 'name', 'customer', 'garbage', 'date', 'task_collection_point', 'base_route_name']


class TaskRouteListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    garbage = GarbageSerializer(read_only=True, many=True)
    task_collection_point = serializers.SerializerMethodField('get_empty_tcp_list')

    @staticmethod
    def get_empty_tcp_list(obj):
        return []

    class Meta:
        model = TaskRoute
        fields = ['id', 'name', 'customer', 'garbage', 'date', 'task_collection_point', 'base_route_name']


class TaskReportSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    @staticmethod
    def get_timestamp(obj):
        if obj.timestamp is None:
            return None
        return obj.timestamp.ctime()

    class Meta:
        model = TaskReport
        fields = ['id', 'route', 'timestamp', 'task_collection_point', 'report_type', 'image', 'description']


class TaskReportListSerializer(serializers.ModelSerializer):
    report_type = ReportTypeSerializer()
    timestamp = serializers.SerializerMethodField()

    @staticmethod
    def get_timestamp(obj):
        if obj.timestamp is None:
            return None
        return obj.timestamp.ctime()

    class Meta:
        model = TaskReport
        fields = ['id', 'route', 'timestamp', 'task_collection_point', 'report_type', 'image', 'description']


class TaskAmountItemListSerializer(serializers.ModelSerializer):
    garbage = GarbageSerializer(read_only=True)

    class Meta:
        model = TaskAmountItem
        read_only_fields = ['id']
        fields = ['id', 'task_amount', 'gross_weight', 'vehicle_weight', 'garbage', 'net_weight']


class TaskAmountItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskAmountItem
        read_only_fields = ['id', 'net_weight']
        fields = ['id', 'task_amount', 'gross_weight', 'vehicle_weight', 'garbage', 'net_weight']


class TaskAmountListSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    timestamp = serializers.SerializerMethodField()
    amount_item = TaskAmountItemListSerializer(read_only=True, many=True)

    @staticmethod
    def get_timestamp(obj):
        if obj.timestamp is None:
            return None
        return obj.timestamp.ctime()

    class Meta:
        model = TaskAmount
        read_only_fields = ['id', 'user', 'timestamp']
        fields = ['id', 'route', 'user', 'amount_item', 'timestamp', 'memo', 'vehicle', 'work_type', 'deal_type']


class TaskAmountSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    @staticmethod
    def get_timestamp(obj):
        if obj.timestamp is None:
            return None
        return obj.timestamp.ctime()

    class Meta:
        model = TaskAmount
        read_only_fields = ['id', 'user', 'timestamp']
        fields = ['id', 'route', 'user', 'timestamp', 'memo', 'vehicle', 'work_type', 'deal_type']
