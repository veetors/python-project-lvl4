from django.contrib.auth.models import User
from django.db import models
from task_manager.statuses.models import TaskStatus
from task_manager.tags.models import Tag


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.RESTRICT,
    )
    creator = models.ForeignKey(
        User,
        related_name='creator',
        on_delete=models.CASCADE,
    )
    assigned_to = models.ForeignKey(
        User,
        related_name='assignet_to',
        null=True,
        on_delete=models.SET_NULL,
    )

    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
