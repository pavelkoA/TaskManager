from django.db import models
from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=150, unique=True, blank=False, verbose_name=_('Name')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='author',
        verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='executor',
        verbose_name=_('Executor')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Creation date')
    )
    labels = models.ManyToManyField(
        Label, through='TaskLabel', through_fields=('task', 'label'),
        blank=True, verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)