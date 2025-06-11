from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('tasks/list/', views.get_task_list, name='get_task_list'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('tasks/mark/completed/<str:id>/', views.MarkTaskCompletedView.as_view(), name='mark_task_completed'),
]