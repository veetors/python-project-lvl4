from django.contrib import admin
from task_manager.models import Task, TaskStatus

admin.site.register(Task)
admin.site.register(TaskStatus)
