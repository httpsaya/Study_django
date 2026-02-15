# Django Modules
from django.contrib.admin import ModelAdmin, register

# Project Modules
from apps.users.models import CustomUser

@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """ Admin panel for our custom users """

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
