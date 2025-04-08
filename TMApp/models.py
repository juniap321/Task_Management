from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
    ('SUPERADMIN', 'Super Admin'),
    ('ADMIN', 'Admin'),
    ('USER', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')

    def is_superadmin(self):
        return self.role == 'SUPERADMIN'
    
    def is_admin(self):
        return self.role == 'ADMIN' or self.role == 'SUPERADMIN'



class Task(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    due_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)