from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserListCreateView, UserDetailView,
    TaskListCreateView, TaskDetailView,
    UserTaskUpdateView, TaskReportView
)

urlpatterns = [
    # Auth endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Task endpoints
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', UserTaskUpdateView.as_view(), name='user-task-update'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
]