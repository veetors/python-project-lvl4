from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelForm
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

    class Meta:
        model = Task
        fields = ['name', 'description', 'creator', 'assigned_to']
        widgets = {'creator': HiddenInput()}
