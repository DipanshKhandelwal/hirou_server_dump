from django.contrib import admin
from .models import Vehicle, Item, Area, CollectionPoint, Pickup


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'model']
    ordering = ['registration_number', 'model']
    fields = ['registration_number', 'users', 'location', 'model']


class PickupAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'vehicle']
    ordering = ['timestamp', 'vehicle']


class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'address']
    ordering = ['name', 'area', 'address']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Pickup, PickupAdmin)
admin.site.register(CollectionPoint, CollectionPointAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Item, ItemAdmin)
