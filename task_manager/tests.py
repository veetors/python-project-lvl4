from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker


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


# class TasksViewsTest(TestCase):
