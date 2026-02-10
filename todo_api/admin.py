from django.contrib import admin
from .models import Task, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'title', 'category', 'due_date', 'created_at', 'is_completed']
    list_filter = ['is_completed', 'category', 'created_at']
    search_fields = ['title', 'description']