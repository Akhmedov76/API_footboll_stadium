from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom user admin for stadium booking application.
    """
    list_display = ('username', 'email', 'role', 'phone', 'address', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (_('User info'), {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'latitude', 'longitude',)}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = (_('username'), _('email'), _('phone'))
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

admin.site.site_header = _("Football Stadium")
admin.site.site_title = _("My Admin")
admin.site.index_title = _("Welcome Stadium Admin")
