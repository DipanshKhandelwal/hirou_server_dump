from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile


def deactivate_selected_users(request, queryset):
    queryset.update(is_active=False)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'phone_number']
    ordering = ['user', 'date_of_birth', 'gender']
    actions = [deactivate_selected_users]


admin.site.unregister(Group)
admin.site.register(Profile, ProfileAdmin)
