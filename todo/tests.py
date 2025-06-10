from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from datetime import datetime, timedelta

from .models import Task, Category


User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def create_task(
        self,
        user,
        title: str = 'New Task',
        description: str | None = '',
        due_date: datetime | None = None,
        category: Category | None = None
    ):
        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            due_date=due_date,
            category=category
        )
        return task


class TaskModelTests(BaseTest):    
    def test_create_task(self):
        task = self.create_task(
            user=self.user, description='some random text',
            due_date=datetime.now().date() + timedelta(days=9)
        )

        self.assertEqual(task.user, self.user)
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.description, 'some random text')
        self.assertEqual(task.due_date, datetime.now().date() + timedelta(days=9))

    def test_due_date_cannot_be_in_past(self):
        task = self.create_task(
            user=self.user, description='some random text',
            due_date=datetime.now().date() - timedelta(days=1)
        )

        with self.assertRaises(Exception):
            task.full_clean()

    def test_create_task_with_category(self):
        category = self.user.task_categories.first()

        task = self.create_task(
            user=self.user,
            category=category
        )

        self.assertEqual(task.category, self.user.task_categories.first())


class DashboardViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse('todo:dashboard')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse(settings.LOGIN_URL)}?next={self.url}')

    def test_dashboard_loads_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/dashboard.html')
        self.assertIn('task_form', response.context)
        self.assertIn('tasks', response.context)

    def test_post_request_create_task(self):
        self.client.force_login(self.user)

        post_data = {
            'title': 'New Task',
            'description': '',
            'due_data': '',
            'priority': 'low',
            'category': str(self.user.task_categories.first().pk)
        }

        response = self.client.post(self.url, data=post_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.url)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'New Task')

    def test_post_request_create_task_with_invalid_data(self):
        self.client.force_login(self.user)

        post_data = {
            'title': '',
            'description': '',
            'due_date': datetime.now().date() - timedelta(days=1),
            'priority': 'low',
            'category': str(self.user.task_categories.first().pk)
        }

        response = self.client.post(self.url, data=post_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title cannot be empty')
        self.assertContains(response, 'Due date cannot be in the past')


class MarkTaskCompletedViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.task = self.create_task(self.user)

    def test_mark_task_completed(self):
        pass
