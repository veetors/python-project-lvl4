from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from task_manager import models


class HomePageViewTest(TestCase):
    def setUp(self):
        """Set suite up."""
        self.client = Client()
        self.faker = Faker()

    def test_redirect_if_not_logged_in(self):
        """Test redirect to login page if not logged in."""
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))

    def test_redirect_if_logged_in(self):
        """Test redirect to task_list page if logged in."""
        username = self.faker.user_name()
        password = self.faker.password(length=12)
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        user.save()
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('task_list'))


class TagViewsTest(TestCase):
    def get_new_tag(self):
        """Create, save to DB and return tag object with random name."""
        tag_name = self.faker.word()
        tag = models.Tag.objects.create(name=tag_name)
        return tag

    def setUp(self):
        """Set suite up."""
        self.client = Client()
        self.faker = Faker()
        username = self.faker.user_name()
        password = self.faker.password(length=12)
        User.objects.create_user(
            username=username,
            password=password,
        )
        self.client.login(username=username, password=password)

    def test_tag_create(self):
        """Test creation tag and redirect to tag_list page."""
        tag_name = self.faker.word()
        response = self.client.post(reverse('tag_new'), data={
            'name': tag_name,
        })
        self.assertRedirects(response, reverse('tag_list'))
        self.assertTrue(models.Tag.objects.get(name=tag_name))

    def test_tag_udate(self):
        """Test update tag and redirect to tag_list page."""
        tag = self.get_new_tag()

        tag_id = tag.id
        updated_tag_name = self.faker.word()

        response = self.client.post(reverse('tag_edit', args=(tag_id,)), data={
            'name': updated_tag_name,
        })

        self.assertRedirects(response, reverse('tag_list'))

        expected_tag_name = models.Tag.objects.get(id=tag_id).name
        self.assertEqual(expected_tag_name, updated_tag_name)

    def test_tag_delete(self):
        """Test delete tag and redirect to tag_list page."""
        tag = self.get_new_tag()
        tag_id = tag.id
        response = self.client.post(reverse('tag_delete', args=(tag_id,)))
        self.assertRedirects(response, reverse('tag_list'))
        with self.assertRaises(models.Tag.DoesNotExist):
            models.Tag.objects.get(id=tag_id)

    def test_tag_list(self):
        """Test tag_list view."""
        quantity_of_tags = 5
        for _ in range(quantity_of_tags):
            self.get_new_tag()

        response = self.client.get(reverse('tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('task_manager/tag_list.html')
        self.assertEqual(len(response.context['object_list']), quantity_of_tags)


class TaskViewsTest(TestCase):
    def get_new_task(self, user=None):
        """Create, save to DB and return task object."""
        current_user = user or self.user
        task_title = self.faker.sentence()
        task_description = self.faker.paragraph()
        task = models.Task.objects.create(
            name=task_title,
            description=task_description,
            status=self.task_status,
            creator=current_user,
            assigned_to=current_user,
        )
        return task

    def setUp(self):
        """Set suite up."""
        self.client = Client()
        self.faker = Faker()

        username = self.faker.user_name()
        password = self.faker.password(length=12)
        self.user = User.objects.create_user(
            username=username,
            password=password,
        )
        self.client.login(username=username, password=password)

        self.task_status = models.TaskStatus.objects.create(
            id=models.DEFAULT_STATUS_ID,
            name=self.faker.word(),
        )

    def test_task_create(self):
        """Test task create and redirect to task_list page."""
        task_title = self.faker.sentence()
        task_description = self.faker.paragraph()

        response = self.client.post(reverse('task_new'), data={
            'name': task_title,
            'description': task_description,
            'assigned_to': self.user.id,
        })

        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(models.Task.objects.get(name=task_title))

    def test_task_update(self):
        """Test update task and redirect to task_detail page."""
        task = self.get_new_task()
        task_id = task.id
        updated_title = self.faker.sentence()
        updated_description = self.faker.paragraph()

        response = self.client.post(
            reverse('task_edit', args=(task_id,)),
            data={
                'name': updated_title,
                'description': updated_description,
                'status': self.task_status.id,
                'assigned_to': self.user.id,
            },
        )

        updated_task = models.Task.objects.get(id=task_id)

        self.assertRedirects(response, reverse('task_detail', args=(task_id,)))
        self.assertEqual(updated_task.name, updated_title)
        self.assertEqual(updated_task.description, updated_description)

    def test_tag_delete(self):
        """Test delete task and redirect to tag_list page."""
        task = self.get_new_task()
        task_id = task.id
        response = self.client.post(reverse('task_delete', args=(task_id,)))
        self.assertRedirects(response, reverse('task_list'))
        with self.assertRaises(models.Task.DoesNotExist):
            models.Task.objects.get(id=task_id)

    def test_task_list(self):
        """Test task_list view."""
        quantity_of_tasks = 5
        for _ in range(quantity_of_tasks):
            self.get_new_task()

        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('task_manager/task_list.html')
        self.assertEqual(
            len(response.context['task_filter'].qs),
            quantity_of_tasks,
        )

    def test_user_task_list(self):
        """Test user_task_list view."""
        request_user = self.user
        another_user = User.objects.create_user(
            username=self.faker.user_name(),
            password=self.faker.password(length=12),
        )

        request_user_quantity_tasks = 4
        another_user_quantity_tasks = 2

        for _ in range(request_user_quantity_tasks):
            self.get_new_task(request_user)
        for _ in range(another_user_quantity_tasks):
            self.get_new_task(another_user)

        response = self.client.get(reverse('user_task_list'))
        context_queryset = response.context['task_filter'].qs

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('task_manager/task_list.html')
        self.assertEqual(
            len(context_queryset),
            request_user_quantity_tasks,
        )

        for task in context_queryset:
            self.assertEqual(task.creator.id, request_user.id)
