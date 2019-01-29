from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField
import reversion

TAG = """
<mark class="entity" style="background: {}; padding: 0.45em 0.6em; color: white;
margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone;
-webkit-box-decoration-break: clone">
    {}
    <span style="font-size: 0.8em;
    font-weight: bold; line-height:
    1; border-radius: 0.35em; text-transform: uppercase;
    vertical-align: middle; margin-left: 0.5rem">{}</span>
</mark>
"""

TAG_COLORS = {
    "PER": '#007bff',
    "LOC": '#5a6268',
    "ORG": "#28a745",
    "MISC": '#17a2b8',
    "OBJECT": '#5a6268',
    "FALSE": '#5a6268'
}


@reversion.register()
class NerSample(models.Model):
    text = models.TextField(
        blank=True, verbose_name="Text", help_text="The annotated text"
    )
    entity_json = JSONField(
        blank=True, null=True, verbose_name="Entitiy-Annotations",
        help_text="offset annotations of annotations"
    )
    entity_checked = JSONField(
        blank=True, null=True, verbose_name="Corrected Annotation",
        help_text="Corrected Annotation"
    )
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.entity_checked is not None:
            ent_dict = self.entity_checked
            cleaned_dict = []
            for x in ent_dict['entities']:
                clean = [int(x[0]), int(x[1]), x[2]]
                cleaned_dict.append(clean)
            ent_dict['entities'] = cleaned_dict
            self.entity_checked = ent_dict
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'annotations:nersample_detail', kwargs={'pk': self.id}
        )

    def get_api_url(self):
        return reverse(
            'nersample-detail', kwargs={'pk': self.id}
        )

    @classmethod
    def get_listview_url(self):
        return reverse('annotations:browse_nersamples')

    @classmethod
    def get_createview_url(self):
        return reverse('annotations:nersample_create')

    def get_next(self, filtered=False):
        if filtered:
            qs = self.__class__.objects.filter(entity_checked__isnull=True)
            next = qs.filter(id__gt=self.id)
        else:
            next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self, filtered=False):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def make_html_samples(self):
        tag = TAG
        sents = []
        text = self.text
        if self.entity_json['entities']:
            for x in self.entity_json['entities']:
                an_dict = {
                    "sent": self.text,
                    "start": x[0],
                    "end": x[1],
                    "ent": x[2]
                }
                sl = text[x[0]:x[1]]
                markup = tag.format(TAG_COLORS[x[2]], sl, x[2])
                start = text[:x[0]]
                end = text[x[1]:]
                an_dict["annotated"] = "".join([start, markup, end])
                sents.append(an_dict)
        else:
            sents.append(
                {
                    "sent": self.text,
                    "start": None,
                    "end": None,
                    "ent": "FALSE",
                    "annotated": self.text
                }
            )
        return sents

    def return_ents(self):
        ents = []
        for x in self.make_html_samples():
            if x['start'] is None:
                pass
            else:
                ents.append(x['sent'][x['start']:x['end']])
        return ents
