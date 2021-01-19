from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import *


class UserAdmin(UserAdmin):
    """
        Переопределения пользователя в django admin
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('firstname', 'lastname', 'middlename', 'phone', 'info')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'status', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'status')
    search_fields = ('firstname', 'lastname', 'email')
    ordering = ('email',)


admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(Image)
admin.site.register(Region)
admin.site.register(City)

