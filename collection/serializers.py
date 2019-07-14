from rest_framework import serializers
from .models import Vehicle, CollectionPoint, Item, Area, Pickup


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = Vehicle
        fields = ['id', 'registration_number', 'model', 'location', 'users', 'pickup']


class AreaSerializer(serializers.ModelSerializer):
    collection_point = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='collection_point-detail')

    class Meta:
        model = Area
        fields = ['url', 'id', 'name', 'description', 'collection_point']


class CollectionPointSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    pickup = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='pickup-detail')

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'location', 'address', 'area', 'pickup']


class PickupSerializer(serializers.ModelSerializer):
    collection_point = CollectionPointSerializer()
    items = ItemSerializer(many=True)
    vehicle = VehicleSerializer()

    class Meta:
        model = Pickup
        read_only_fields = ['id', 'timestamp', 'vehicle', 'users']
        fields = ['id', 'collection_point', 'timestamp', 'items', 'vehicle', 'users', 'image', 'route']
