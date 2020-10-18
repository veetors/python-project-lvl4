from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TasksList(LoginRequiredMixin, ListView):
    model = Task


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('tasks:task_list')

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
        return reverse_lazy('tasks:task_detail', args=(self.object.id,))


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
