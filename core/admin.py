from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = [
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff'
        ]
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    list_editable = ['is_active', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name',
                       'last_name',
                       'email',
                       'password1',
                       'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
