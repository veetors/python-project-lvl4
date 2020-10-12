from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from task_manager.forms import SignupForm, TaskForm
from task_manager.models import Task


def home(request):
    tasks = Task.objects.all()

    return render(request, 'task_manager/home.html', context={
        'tasks': tasks,
    })


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    success_message = 'Account was created for %(username)s'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        user = self.request.user
        return {
            'creator': user,
            'assigned_to': user,
        }
