from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Task
from .serializers import *

User = get_user_model()

class IsSuperAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_superadmin()

class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin()

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            })
        return Response({'error': 'Invalid credentials'})

class UserListCreateView(APIView):
    permission_classes = [IsSuperAdmin]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

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
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({"error": "error"})

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_superadmin():
            tasks = Task.objects.all()
        elif request.user.is_admin():
            tasks = Task.objects.filter(created_by=request.user)
        else:
            tasks = Task.objects.filter(assigned_to=request.user)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_admin():
            return Response({"error": "You don't have permission to create tasks"})
        
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        task = get_object_or_404(Task, pk=pk)
        
        if not task.created_by == self.request.user and not task.assigned_to == self.request.user and not self.request.user.is_superadmin():
            self.permission_denied(self.request)
            
        return task
    
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_object(pk)
        
        if request.user.is_normal_user():
            if task.assigned_to != request.user:
                return Response({"error": "You can only update tasks assigned to you"})
            
            serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        else:
            serializer = TaskSerializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not request.user.is_admin():
            return Response({"error": "You don't have permission to delete tasks"})
            
        task = self.get_object(pk)
        task.delete()
        return Response({"error": "error"})

class TaskReportView(APIView):
    permission_classes = [IsAdmin]  
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        
        if not request.user.is_superadmin() and task.created_by != request.user:
            return Response({"error": "You don't have permission to view this report"})
            
        if task.status != 'completed':
            return Response({"error": "Task is not completed yet"})
            
        serializer = TaskReportSerializer(task)
        return Response(serializer.data)
