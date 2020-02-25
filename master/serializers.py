from rest_framework import serializers
from .models import Vehicle, CollectionPoint, Garbage, Collection, Customer


class GarbageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garbage
        fields = ['id', 'name', 'description']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = Vehicle
        fields = ['id', 'registration_number', 'model', 'location', 'users', 'pickup']


class CollectionPointSerializer(serializers.ModelSerializer):
    pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'location', 'address', 'pickup']


class CollectionSerializer(serializers.ModelSerializer):
    collection_point = CollectionPointSerializer()
    garbages = GarbageSerializer(many=True)
    vehicle = VehicleSerializer()

    class Meta:
        model = Collection
        read_only_fields = ['id', 'timestamp', 'vehicle', 'users']
        fields = ['id', 'collection_point', 'timestamp', 'garbages', 'vehicle', 'users', 'image', 'route']
