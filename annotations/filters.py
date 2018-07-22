import django_filters

from . models import NerSample


class NerSampleListFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=NerSample._meta.get_field('text').help_text,
        label=NerSample._meta.get_field('text').verbose_name
        )

    class Meta:
        model = NerSample
        fields = ['text', 'id']
