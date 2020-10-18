from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from task_manager.tags.models import Tag


class TagList(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tags/tag_list.html'


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/tag_create_form.html'
    success_url = reverse_lazy('tags:tag_list')


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/tag_update_form.html'
    success_url = reverse_lazy('tags:tag_list')


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'tags/tag_confirm_delete.html'
    success_url = reverse_lazy('tags:tag_list')
