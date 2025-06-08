from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


User = get_user_model()


class Task(models.Model):
    class TASK_PRIORITY(models.TextChoices):
        LOW = ('low', 'Low')
        MEDIUM = ('medium', 'Medium')
        HIGH = ('high', 'High')

    class TASK_STATUS(models.TextChoices):
        PENDING = ('pending', 'Pending')
        IN_PROGRESS = ('in_progress', 'In progress')
        ON_HOLD = ('on_hold', 'On hold')
        COMPLETED = ('completed', 'Completed')
        DELETED = ('deleted', 'Deleted')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=7,
        choices=TASK_PRIORITY.choices,
        default=TASK_PRIORITY.LOW
    )
    status = models.CharField(
        max_length=12,
        choices=TASK_STATUS.choices,
        default=TASK_STATUS.PENDING
    )
    category = models.ManyToManyField('Category', related_name='tasks', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ('user', '-created')
        indexes = (
            models.Index(fields=['user', 'status'], name='taskUserStatusIdx'),
            models.Index(fields=['priority'], name='taskPriorityIdx'),
            models.Index(fields=['due_date'], name='taskDueDateIdx'),
        )

    def __str__(self):
        return f'{self.title} ({self.status})'
    
    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError('Due date cannot be in the past')
        if not self.title.strip():
            raise ValidationError('Title cannot be empty')
        
        return super().clean()
    
    def mark_pending(self):
        self.status = self.TASK_STATUS.PENDING
        self.save()

    def mark_in_progress(self):
        self.status = self.TASK_STATUS.IN_PROGRESS
        self.save()

    def mark_on_hold(self):
        self.status = self.TASK_STATUS.ON_HOLD
        self.save()

    def mark_completed(self):
        self.status = self.TASK_STATUS.COMPLETED
        self.save()

    def mark_deleted(self):
        self.status = self.TASK_STATUS.DELETED
        self.save()


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.name.strip():
            raise ValidationError('Name cannot be empty')
        return super().clean()
