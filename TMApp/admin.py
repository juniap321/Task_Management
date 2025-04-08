from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status', 'worked_hours')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superadmin():
            return qs
        elif request.user.is_admin():
            return qs
        return qs.filter(assigned_to=request.user)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_admin():
            return True
        if obj is not None and obj.assigned_to == request.user:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin()

admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)