from rest_framework import viewsets
from . serializers import NerSampleSerializer
from . models import NerSample


class NerSampleViewSet(viewsets.ModelViewSet):

    queryset = NerSample.objects.all().order_by('id')
    serializer_class = NerSampleSerializer


class NerSampleViewSetToDo(viewsets.ModelViewSet):

    queryset = NerSample.objects.filter(entity_checked__isnull=True).order_by('id')
    serializer_class = NerSampleSerializer
