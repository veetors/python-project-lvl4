from django_filters import FilterSet
from task_manager.models import Task


class TaskFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filter in ('assigned_to', 'status', 'tags'):
            filter_field = self.filters[filter].field
            filter_field.widget.attrs.update({
                'class': 'selectpicker',
            })
            if filter != 'tags':
                filter_field.empty_label = 'Nothing selected'

    @property
    def qs(self):
        return super().qs.order_by('-created_at')

    class Meta:
        model = Task
        fields = ('assigned_to', 'status', 'tags')


class UserTaskFilter(TaskFilter):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    @property
    def qs(self):
        parent_qs = super().qs
        return parent_qs.filter(creator=self.user).order_by('-created_at')
