from .models import Status
from .forms import StatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import UserAuthenticateMixin, DeleteProtectionMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class StatusesListView(UserAuthenticateMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses')
    }


class StatusCreateView(UserAuthenticateMixin, SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'form.html'
    form_class = StatusForm
    success_message = _('Status successfully created')
    success_url = reverse_lazy('statuses_list')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(UserAuthenticateMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'form.html'
    form_class = StatusForm
    success_message = _('Status successfully changed')
    success_url = reverse_lazy('statuses_list')
    extra_context = {
        'title': _('Change status'),
        'button_text': _('Change'),
    }


class StatusDeleteView(
    UserAuthenticateMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView
):
    model = Status
    template_name = 'delete.html'
    success_message = _('Status successfully delete')
    success_url = reverse_lazy('statuses_list')
    protected_message = _(
        'It is not possible to delete a status because it is in use'
    )
    protected_url = reverse_lazy('statuses_list')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Delete'),
    }
