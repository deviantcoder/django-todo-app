from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
from .models import Task


class HomeView(generic.TemplateView):
    template_name = 'todo/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todo:dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'todo/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskForm(user=self.request.user)
        context['tasks'] = self.request.user.tasks.all()

        return context
