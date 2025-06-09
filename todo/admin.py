from django.contrib import admin

from .models import Task, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('user', 'title', 'due_date', 'priority', 'status')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('user', 'name')
