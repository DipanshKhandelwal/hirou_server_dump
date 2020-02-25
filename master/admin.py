from django.contrib import admin
from .models import Vehicle, Garbage, CollectionPoint, Pickup, Customer


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'model']
    ordering = ['registration_number', 'model']
    fields = ['registration_number', 'users', 'location', 'model']


class PickupAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'vehicle']
    ordering = ['timestamp', 'vehicle']


class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    ordering = ['name', 'address']


class GarbageAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Pickup, PickupAdmin)
admin.site.register(CollectionPoint, CollectionPointAdmin)
admin.site.register(Garbage, GarbageAdmin)
admin.site.register(Customer, CustomerAdmin)
