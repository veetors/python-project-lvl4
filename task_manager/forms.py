from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from task_manager.models import Task


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Task title'
        self.fields['description'].label = 'Task description'
        self.fields['creator'].disabled = True

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'creator',
            'assigned_to',
            'tags',
        ]


class TaskCreationForm(TaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].widget.attrs.update({'hidden': True})
        self.fields['status'].disabled = True
