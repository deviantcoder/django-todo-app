from django.shortcuts import render
from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'todo/home.html'


class DashboardView(generic.TemplateView):
    template_name = 'todo/dashboard.html'
