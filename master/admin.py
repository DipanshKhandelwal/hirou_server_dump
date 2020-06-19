from django.contrib import admin
from .models import Vehicle, Garbage, CollectionPoint, Customer, BaseRoute, TaskRoute, TaskCollectionPoint, TaskCollection


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'model']
    ordering = ['registration_number', 'model']
    fields = ['registration_number', 'location', 'model']


class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ['route', 'sequence', 'name', 'memo', 'address']
    ordering = ['route', 'sequence', 'name', 'memo', 'address']


class GarbageAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


class BaseRouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer']
    ordering = ['name', 'customer']


#
class TaskCollectionAdmin(admin.ModelAdmin):
    list_display = ['collection_point', 'garbage', 'complete', 'amount']
    ordering = ['collection_point', 'garbage', 'complete', 'amount']


class TaskCollectionPointAdmin(admin.ModelAdmin):
    list_display = ['route', 'sequence', 'name', 'memo', 'address']
    ordering = ['route', 'sequence', 'name', 'memo', 'address']


class TaskRouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer', 'date']
    ordering = ['name', 'customer', 'date']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CollectionPoint, CollectionPointAdmin)
admin.site.register(Garbage, GarbageAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(BaseRoute, BaseRouteAdmin)

admin.site.register(TaskCollection, TaskCollectionAdmin)
admin.site.register(TaskCollectionPoint, TaskCollectionPointAdmin)
admin.site.register(TaskRoute, TaskRouteAdmin)
