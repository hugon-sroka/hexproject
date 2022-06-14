from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import UserProfile, Img
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'full_name']
    fieldsets = (
        (   None,          {'fields':   ('email', 'password')}),
        (_('Permissions'), {'fields':   ('is_active','is_staff','is_premium','is_enterprise','is_superuser')}),
        (_('Events'),      {'fields':   ('last_login',)}),
        (_('Image'),       {'fields': ('image', )}),
                )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'full_name', 'is_active', 'is_staff',
                           'is_premium', 'is_enterprise','is_superuser')}),
    )

admin.site.register(UserProfile, UserAdmin)
admin.site.register(Img)