from rest_framework import serializers

from . models import NerSample


class NerSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NerSample
        fields = "__all__"
