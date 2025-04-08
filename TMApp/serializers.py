from rest_framework import serializers
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name')
        
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'first_name', 'last_name')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status', 'completion_report', 'worked_hours')
        
    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError("Completion report is required when marking a task as completed.")
            if not data.get('worked_hours'):
                raise serializers.ValidationError("Worked hours must be provided when marking a task as completed.")
        return data
    