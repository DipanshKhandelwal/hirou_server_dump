from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, User


def deactivate_selected_users(request, queryset):
    queryset.update(is_active=False)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_login', 'email', 'phone_number', 'first_name', 'last_name']
    ordering = ['last_login', 'username', 'first_name']
    actions = [deactivate_selected_users]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'gender']
    ordering = ['user', 'dob', 'gender']
    actions = [deactivate_selected_users]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
