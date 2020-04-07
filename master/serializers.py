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


class BaseRouteSerializer(serializers.ModelSerializer):
    # collection_point = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='collection_point-detail')
    # collection_point = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    collection_point = CollectionPointSerializer(read_only=True, many=True)
    garbage = GarbageSerializer(read_only=True, many=True)
    # customer = CustomerSerializer()
    # garbage = GarbageSerializer(many=True)

    class Meta:
        model = BaseRoute
        fields = ['id', 'name', 'customer', 'collection_point', 'garbage']


# class BaseRouteListSerializer(serializers.ModelSerializer):
#     collection_point = CollectionPointSerializer(read_only=True, many=True)
#     customer = CustomerSerializer()
#
#     class Meta:
#         model = BaseRoute
#         fields = ['id', 'name', 'customer', 'collection_point']


class TaskRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskRoute
        fields = ['id', 'name', 'customer', 'date']


class TaskCollectionPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskCollectionPoint
        fields = ['id', 'name', 'location', 'address', 'route', 'sequence', 'image']


class TaskCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskCollection
        fields = ['id', 'collection_point', 'timestamp', 'complete', 'amount', 'image', 'users', 'vehicle', 'garbage', 'available']
