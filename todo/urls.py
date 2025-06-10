from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('tasks/mark/completed/<str:id>/', views.MarkTaskCompletedView.as_view(), name='mark_task_completed'),
]