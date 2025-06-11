from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import TaskForm
from .models import Task


class HomeView(generic.TemplateView):
    template_name = 'todo/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todo:dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    

@login_required
def dashboard_view(request):
    context = {
        'task_form': TaskForm(user=request.user),
        'tasks': request.user.tasks.filter(is_completed=False, is_deleted=False).select_related('category'),
        'completed_tasks': request.user.tasks.filter(is_completed=True).select_related('category'),
    }

    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            messages.success(request, 'Task created!')

            return redirect('todo:dashboard')
        else:
            for error in form.non_field_errors():
                messages.warning(request, error)
            context['task_form'] = form
            return render(request, 'todo/dashboard.html', context)

    return render(request, 'todo/dashboard.html', context)


@login_required
def get_task_list(request):
    tasks = request.user.tasks.filter(is_completed=False, is_deleted=False).select_related('category')
    return render(request, 'todo/partials/_task_list.html', {'tasks': tasks})


@login_required
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            messages.success(request, 'Task created!')

            return HttpResponse(status=204)

        return render(request, 'todo/partials/_task_form.html', {'task_form': form})
    return redirect('todo:dashboard')


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
