from django.contrib import admin
from task_manager.statuses.models import TaskStatus
from task_manager.tags.models import Tag
from task_manager.tasks.models import Task

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(Tag)
