from django.db import models
from django.contrib.postgres.fields import JSONField


class NerSample(models.Model):
    text = models.TextField(
        blank=True, verbose_name="Text", help_text="The annotated text"
    )
    entity_json = JSONField(
        blank=True, null=True, verbose_name="Entitiy-Annotations",
        help_text="offset annotations of entities"
    )
    entity_checked = JSONField(
        blank=True, null=True, verbose_name="Corrected Annotation",
        help_text="Corrected Annotation"
    )

    def __str__(self):
        return self.text

    def make_html_samples(self):
        tag = '<span class="spacy-{}">{}</span>'
        sents = []
        text = self.text
        if self.entity_json['entities']:
            for x in self.entity_json['entities']:
                sl = text[x[0]:x[1]]
                markup = tag.format(x[2].lower(), sl)
                start = text[:x[0]]
                end = text[x[1]:]
                annotated = "".join([start, markup, end])
                sents.append(annotated)
        else:
            sents = [self.text]
        return sents
