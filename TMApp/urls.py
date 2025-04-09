from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('api/login/', UserLoginView.as_view(), name='login'),
    
    # User (SuperAdmin only)
    path('api/users/', UserListCreateView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Task management
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
]