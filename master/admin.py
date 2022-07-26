import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Vehicle, Garbage, ReportType, CollectionPoint, Customer, BaseRoute, TaskRoute, TaskCollectionPoint,\
    TaskCollection, TaskReport, TaskAmount, TaskAmountItem


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'model']
    ordering = ['registration_number', 'model']
    fields = ['registration_number', 'model']


class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ['route', 'sequence', 'name', 'memo', 'address', 'image']
    ordering = ['route', 'sequence', 'name', 'memo', 'address', 'image']


class GarbageAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ['name', 'description']


class ReportTypeAdmin(admin.ModelAdmin):
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
    list_display = ['collection_point', 'garbage', 'complete', 'timestamp', 'amount']
    ordering = ['collection_point', 'garbage', 'complete', 'timestamp', 'amount']

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.xls'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class TaskCollectionPointAdmin(admin.ModelAdmin):
    list_display = ['route', 'sequence', 'name', 'memo', 'address']
    ordering = ['route', 'sequence', 'name', 'memo', 'address']


class TaskRouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer', 'date', 'base_route_name']
    ordering = ['name', 'customer', 'date', 'base_route_name']


class TaskReportAdmin(admin.ModelAdmin):

    def get_google_link(self, obj):
        if obj.task_collection_point:
            tcp = obj.task_collection_point
            link = f"http://www.google.com/maps/place/{tcp.location}"
            if tcp:
                return link
        return 'N/A'

    get_google_link.short_description = 'Map link'

    list_display = ['timestamp', 'report_type', 'task_collection_point', 'route', 'image', 'description', 'get_google_link']
    ordering = ['timestamp', 'report_type', 'task_collection_point', 'route', 'image', 'description']


class TaskAmountAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'route', 'vehicle']
    ordering = ['timestamp', 'route', 'vehicle']


class TaskAmountItemAdmin(admin.ModelAdmin):
    readonly_fields = ['net_weight']
    list_display = ['task_amount', 'net_weight', 'gross_weight', 'vehicle_weight', 'garbage']
    ordering = ['task_amount', 'gross_weight', 'vehicle_weight', 'garbage']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(CollectionPoint, CollectionPointAdmin)
admin.site.register(Garbage, GarbageAdmin)
admin.site.register(ReportType, ReportTypeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(BaseRoute, BaseRouteAdmin)
admin.site.register(TaskCollection, TaskCollectionAdmin)
admin.site.register(TaskCollectionPoint, TaskCollectionPointAdmin)
admin.site.register(TaskRoute, TaskRouteAdmin)
admin.site.register(TaskReport, TaskReportAdmin)
admin.site.register(TaskAmount, TaskAmountAdmin)
admin.site.register(TaskAmountItem, TaskAmountItemAdmin)
