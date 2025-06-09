from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Task, Category


class TaskForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.RadioSelect(),
        required=False
    )

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'due_date',
            'priority',
            'category'
        )
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'placeholder': 'What needs to be done?'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Describe the task.'})
        self.fields['category'].widget.attrs.update({'placeholder': 'Select a category'})

        if user is not None:        
            self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        
        if due_date and due_date < timezone.now().date():
            raise ValidationError('Due date cannot be in the past')
        
        return due_date
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        
        if not title:
            raise ValidationError('Title cannot be empty')
        
        return title
