from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user_id', 'title', 'description', 'category', 'category_name', 'due_date', 'created_at', 'updated_at', 'is_completed']
        read_only_fields = ['id', 'created_at', 'updated_at']