from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from reversion.models import Version

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . models import NerSample
from . forms import NerSampleForm, NerSampleFilterFormHelper
from . filters import NerSampleListFilter


class NerSampleListView(GenericListView):
    model = NerSample
    filter_class = NerSampleListFilter
    formhelper_class = NerSampleFilterFormHelper
    init_columns = [
        'id',
        'text',
        'entity_checked',
    ]


class NerSampleDetailView(DetailView):
    model = NerSample
    template_name = 'annotations/nersample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NerSampleDetailView, self).get_context_data(**kwargs)
        context['history'] = Version.objects.get_for_object(self.object)
        return context


class NerSampleCreate(BaseCreateView):

    model = NerSample
    form_class = NerSampleForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerSampleCreate, self).dispatch(*args, **kwargs)


class NerSampleUpdate(BaseUpdateView):

    model = NerSample
    form_class = NerSampleForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerSampleUpdate, self).dispatch(*args, **kwargs)


class NerSampleDelete(DeleteView):
    model = NerSample
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('entities:browse_institutions')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerSampleDelete, self).dispatch(*args, **kwargs)
