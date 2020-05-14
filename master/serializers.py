from rest_framework import serializers
from .models import Vehicle, CollectionPoint, Garbage, Collection, Customer, BaseRoute, TaskRoute, TaskCollectionPoint, TaskCollection


class GarbageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garbage
        fields = ['id', 'name', 'description', 'route']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    # pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = Vehicle
        fields = ['id', 'registration_number', 'model', 'location']
        # fields = ['id', 'registration_number', 'model', 'location', 'pickup']


class CollectionPointSerializer(serializers.ModelSerializer):
    # pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'location', 'address', 'route', 'sequence', 'image']
        # fields = ['id', 'name', 'location', 'address', 'pickup']


class CollectionSerializer(serializers.ModelSerializer):
    collection_point = CollectionPointSerializer()
    # garbage = GarbageSerializer(many=True)
    # vehicle = VehicleSerializer()

    class Meta:
        model = Collection
        # read_only_fields = ['id', 'timestamp', 'vehicle', 'users']
        fields = ['id', 'collection_point', 'available']


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

    class Meta:
        model = TaskCollection
        fields = ['id', 'collection_point', 'timestamp', 'complete', 'amount', 'image', 'users', 'vehicle', 'garbage', 'available']


class TaskCollectionListSerializer(serializers.ModelSerializer):
    garbage = GarbageSerializer(read_only=True)

    class Meta:
        model = TaskCollection
        fields = ['id', 'collection_point', 'timestamp', 'complete', 'amount', 'image', 'users', 'vehicle', 'garbage', 'available']


class TaskCollectionPointSerializer(serializers.ModelSerializer):
    task_collection = TaskCollectionListSerializer(read_only=True, many=True)

    class Meta:
        model = TaskCollectionPoint
        fields = ['id', 'name', 'location', 'address', 'route', 'sequence', 'image', 'task_collection']


class TaskRouteSerializer(serializers.ModelSerializer):
    task_collection_point = TaskCollectionPointSerializer(read_only=True, many=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = TaskRoute
        fields = ['id', 'name', 'customer', 'date', 'task_collection_point']
