from task_manager.tasks.models import Task
from django.forms import CheckboxInput
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter


class TaskFilter(FilterSet):

    status = ModelChoiceFilter(queryset=Status.objects.all(),
                               field_name='status',
                               label=_('Status'))

    executor = ModelChoiceFilter(queryset=get_user_model().objects.all(),
                                 field_name='executor',
                                 label=_('Executor'))

    labels = ModelChoiceFilter(queryset=Label.objects.all(),
                               field_name='labels',
                               label=_('Label'))

    own_tasks = BooleanFilter(widget=CheckboxInput,
                              label=_('Only your own tasks'),
                              field_name='creator',
                              method='get_own_tasks')

    def get_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user.id
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'own_tasks']
