from django.contrib.auth.models import User
from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
