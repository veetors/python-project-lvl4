from django.contrib.auth.models import User
from django.db import models

DEFAULT_STATUS_ID = 1


class TaskStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        TaskStatus,
        default=DEFAULT_STATUS_ID,
        on_delete=models.CASCADE,
    )
    creator = models.ForeignKey(
        User,
        related_name='creator',
        on_delete=models.CASCADE,
    )
    assigned_to = models.ForeignKey(
        User,
        related_name='assignet_to',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
