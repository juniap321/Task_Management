from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)
