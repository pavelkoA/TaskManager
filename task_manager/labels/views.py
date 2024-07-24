from .models import Label
from .forms import LabelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import UserAuthenticateMixin, DeleteProtectionMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LabelListView(UserAuthenticateMixin,
                    ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'
    extra_context = {
        'title': _('Labels')
    }


class LabelCreateView(UserAuthenticateMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    template_name = 'form.html'
    form_class = LabelForm
    success_message = _('Label successfully created')
    success_url = reverse_lazy('labels_list')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(UserAuthenticateMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    template_name = 'form.html'
    form_class = LabelForm
    success_message = _('Label successfully changed')
    success_url = reverse_lazy('labels_list')
    extra_context = {
        'title': _('Change label'),
        'button_text': _('Change'),
    }


class LabelDeleteView(UserAuthenticateMixin,
                      DeleteProtectionMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_message = _('Label successfully delete')
    success_url = reverse_lazy('labels_list')
    protected_message = _(
        'It is not possible to delete a label because it is in use'
    )
    protected_url = reverse_lazy('labels_list')
    extra_context = {
        'title': _('Delete label'),
        'button_text': _('Delete'),
    }
