from django.contrib import admin
from .models import Vehicle, Item, User, Area, CollectionPoint, Pickup


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'model']
    ordering = ['registration_number', 'model']
    fields = ['registration_number', 'model', ('x', 'y')]


class PickupAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'area', 'vehicle']
    ordering = ['timestamp', 'area', 'vehicle']


class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    ordering = ['name', 'address']


admin.site.register(
    [Item, User, Area],
)

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Pickup, PickupAdmin)
admin.site.register(CollectionPoint, CollectionPointAdmin)
