from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import RestrictedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from task_manager.forms import SignupForm, TaskForm
from task_manager.models import Task, TaskStatus


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


class TasksList(LoginRequiredMixin, ListView):
    model = Task


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
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


class StatusList(LoginRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'task_manager/status_list.html'


class StatusCreate(LoginRequiredMixin, CreateView):
    model = TaskStatus
    fields = ['name']
    template_name = 'task_manager/status_create_form.html'
    success_url = reverse_lazy('status_list')


class StatusUpdate(LoginRequiredMixin, UpdateView):
    model = TaskStatus
    fields = ['name']
    template_name = 'task_manager/status_update_form.html'
    success_url = reverse_lazy('status_list')


class StatusDelete(LoginRequiredMixin, DeleteView):
    model = TaskStatus
    template_name = 'task_manager/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')
    error_url = reverse_lazy('status_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except RestrictedError:
            messages.add_message(
                request,
                messages.ERROR,
                (
                    'Status "{0}" can\'t be deleted, because it is used in some task.'
                ).format(self.object.name),
            )
            return redirect(self.error_url)
        return redirect(self.success_url)
