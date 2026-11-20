from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="test-pass")

    def test_task_create_requires_login(self):
        response = self.client.get(reverse("tasks:create"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('tasks:create')}",
        )

    def test_task_form_renders_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("tasks:create"))

        self.assertContains(response, "Add a task")
        self.assertContains(response, 'type="date"')

    def test_task_create_assigns_current_user(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("tasks:create"),
            {
                "title": "Finish deployment",
                "description": "Set up the Render database",
                "due_date": "2026-12-01",
                "priority": "High",
            },
        )

        self.assertRedirects(response, reverse("tasks:list"))
        task = Task.objects.get()
        self.assertEqual(task.user, self.user)
        self.assertFalse(task.completed)

    def test_task_delete_confirmation_renders_for_owner(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
            user=self.user,
            title="Remove old task",
            description="No longer needed",
            due_date="2026-12-01",
            priority="Low",
        )

        response = self.client.get(reverse("tasks:delete", args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete")
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())

    def test_task_delete_post_deletes_and_redirects(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
            user=self.user,
            title="Remove old task",
            description="No longer needed",
            due_date="2026-12-01",
            priority="Low",
        )

        response = self.client.post(reverse("tasks:delete", args=[task.pk]))

        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
