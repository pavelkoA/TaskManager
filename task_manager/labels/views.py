from .models import Label
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import CustomLoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LabelListView(CustomLoginRequiredMixin,
                    ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'
    extra_context = {
        'title': _('Labels')
    }


class LabelCreateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    template_name = 'labels/create.html'
    fields = ['name']
    success_message = _('Label successfully created')
    success_url = reverse_lazy('labels_list')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    template_name = 'labels/update.html'
    fields = ['name']
    success_message = _('Label successfully changed')
    success_url = reverse_lazy('labels_list')
    extra_context = {
        'title': _('Change label'),
        'button_text': _('Change'),
    }


class LabelDeleteView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_message = _('Label successfully delete')
    success_url = reverse_lazy('labels_list')
    protected_message = _(
        'It is not possible to delete the label, it is in use')
    protected_url = 'labels_list'

    extra_context = {
        'title': _('Delete label'),
        'button_text': _('Delete'),
    }

    def post(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(self.request, self.protected_message)
            return redirect(self.protected_url)
        return super().post(request, *args, **kwargs)
