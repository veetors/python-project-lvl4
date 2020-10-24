from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from task_manager.filters import TaskFilter, UserTaskFilter
from task_manager.forms import SignupForm, TaskCreationForm, TaskForm
from task_manager.models import Tag, Task


def home(request):
    tasks = Task.objects.all()

    return render(request, 'task_manager/home.html', context={
        'tasks': tasks,
    })


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    success_message = 'Account was created for %(username)s'


# Tasks
class TaskList(LoginRequiredMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_filter = TaskFilter(self.request.GET)
        context['task_filter'] = task_filter
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('task_list')

    def get_initial(self):
        user = self.request.user
        return {
            'creator': user,
            'assigned_to': user,
        }


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('task_detail', args=(self.object.id,))


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')


class UserTaskList(TaskList):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_filter = UserTaskFilter(self.request.user, self.request.GET)
        context['task_filter'] = task_filter
        return context


# Tags
class TagList(LoginRequiredMixin, ListView):
    model = Tag


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('tag_list')


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('tag_list')


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tag_list')
