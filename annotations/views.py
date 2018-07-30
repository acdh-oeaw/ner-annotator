from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView

from reversion.models import Version

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . models import NerSample
from . forms import NerSampleForm, NerSampleFilterFormHelper, UploadFileForm
from . filters import NerSampleListFilter
from . utils import create_ner_samples_from_csv


@method_decorator(login_required, name="dispatch")
class UploadNerSamplesView(FormView):
    template_name = 'annotations/import_ner_samples.html'
    form_class = UploadFileForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(UploadNerSamplesView, self).get_context_data()
        context['ner_before'] = NerSample.objects.all().count()
        return context

    def form_valid(self, form, **kwargs):
        context = super(UploadNerSamplesView, self).get_context_data(**kwargs)
        context['ner_before'] = NerSample.objects.all().count()
        cd = form.cleaned_data
        file = cd['file']
        create_ner_samples_from_csv(file)
        context['ner_after'] = NerSample.objects.all().count()
        return render(self.request, self.template_name, context)


class NerSampleToDoListView(GenericListView):
    model = NerSample
    filter_class = NerSampleListFilter
    formhelper_class = NerSampleFilterFormHelper
    init_columns = [
        'id',
        'text',
        'entity_checked',
    ]

    def get_queryset(self, **kwargs):
        qs = super(NerSampleToDoListView, self).get_queryset()
        qs = qs.filter(entity_checked__isnull=True)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs


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
        context['next_filtered'] = self.object.get_next(filtered=True)
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
