from django.contrib import admin


def logout_selected_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


admin.site.add_action(logout_selected_users, 'logout_selected_users')
