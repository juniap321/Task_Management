from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_ROLES = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def is_superadmin(self):
        return self.role == 'superadmin'
    
    def is_admin(self):
        return self.role == 'admin' or self.role == 'superadmin'
    
    def is_normal_user(self):
        return self.role == 'user'

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title