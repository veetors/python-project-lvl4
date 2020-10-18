from django.forms import HiddenInput, ModelForm
from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Task title'
        self.fields['description'].label = 'Task description'

    class Meta:
        model = Task
        fields = [
            'name',
            'status',
            'description',
            'creator',
            'assigned_to',
            'tags',
        ]
        widgets = {
            'creator': HiddenInput(),
        }
