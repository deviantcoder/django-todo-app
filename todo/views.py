from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
        context['tasks'] = self.request.user.tasks.filter(is_completed=False, is_deleted=False).select_related('category')
        context['completed_tasks'] = self.request.user.tasks.filter(is_completed=True).select_related('category')

        return context
    
    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            messages.success(request, 'Task created!')

            return redirect('todo:dashboard')
        else:
            context = self.get_context_data()
            context['task_form'] = form

            for error in form.non_field_errors():
                messages.warning(request, error)

            return self.render_to_response(context)


class MarkTaskCompletedView(LoginRequiredMixin, View):
    success_url = reverse_lazy('todo:dashboard')

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['id'], user=request.user)

        if task.is_completed:
            task.is_completed = False
            task.save(update_fields=['is_completed'])
            messages.warning(request, 'Task completion unchecked')
        else:
            task.mark_completed()
            messages.success(request, 'Task completed!')

        return redirect(self.success_url)
