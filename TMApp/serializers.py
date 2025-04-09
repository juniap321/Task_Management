from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'user'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'assigned_to', 'assigned_to_username', 
                 'created_by', 'created_by_username', 'due_date', 'status', 
                 'completion_report', 'worked_hours', 'created_at', 'updated_at')
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'status', 'completion_report', 'worked_hours')
        
    def validate(self, attrs):
        if 'status' in attrs and attrs['status'] == 'completed':
            if not attrs.get('completion_report'):
                raise serializers.ValidationError("Completion report is required when marking a task as completed")
            if not attrs.get('worked_hours'):
                raise serializers.ValidationError("Worked hours is required when marking a task as completed")
        return attrs

class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'assigned_to_username', 'completion_report', 'worked_hours', 'updated_at')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)