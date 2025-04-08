from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import User, Task
from .serializers import UserSerializer, UserCreateSerializer, TaskSerializer, TaskUpdateSerializer
from .permissions import IsSuperAdmin, IsAdminUser, IsTaskOwner

# User views
class UserListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsSuperAdmin()]
        return [IsAdminUser()]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsSuperAdmin]
    
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Task views
class TaskListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get(self, request):
        user = request.user
        if user.is_admin():
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_object(self, pk, request):
        task = get_object_or_404(Task, pk=pk)
        if not request.user.is_admin() and task.assigned_to != request.user:
            self.permission_denied(request)
        return task
    
    def get(self, request, pk):
        task = self.get_object(pk, request)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_object(pk, request)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk, request)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserTaskUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTaskOwner]
    
    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        
        # Check if user can access this report
        user = request.user
        if not user.is_admin() and task.assigned_to != user:
            return Response({"detail": "You do not have permission to view this report."}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        if task.status != 'COMPLETED':
            return Response({"detail": "Report is only available for completed tasks."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'title': task.title,
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours,
            'completed_by': task.assigned_to.username
        })