from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from task_manager.statuses.models import TaskStatus


class StatusList(LoginRequiredMixin, ListView):
    model = TaskStatus
    template_name = 'statuses/status_list.html'


class StatusCreate(LoginRequiredMixin, CreateView):
    model = TaskStatus
    fields = ['name']
    template_name = 'statuses/status_create_form.html'
    success_url = reverse_lazy('statuses:status_list')


class StatusUpdate(LoginRequiredMixin, UpdateView):
    model = TaskStatus
    fields = ['name']
    template_name = 'statuses/status_update_form.html'
    success_url = reverse_lazy('statuses:status_list')


class StatusDelete(LoginRequiredMixin, DeleteView):
    model = TaskStatus
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses:status_list')
    error_url = reverse_lazy('statuses:status_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except RestrictedError:
            messages.add_message(
                request,
                messages.ERROR,
                (
                    'Status "{0}" can\'t be deleted, '
                    'because it is used in some task.'
                ).format(self.object.name),
            )
            return redirect(self.error_url)
        return redirect(self.success_url)
