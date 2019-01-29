import ast
import pandas as pd
import requests
import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from . models import NerSample


def create_ner_samples_from_csv(file, text_col='text', ent_col='entities'):
    df = pd.read_csv(file)
    df['dict'] = df[ent_col].map(ast.literal_eval)
    for i, row in df.iterrows():
        try:
            textlenght = len(row[text_col])
        except TypeError:
            textlenght = None

        if textlenght is None:
            pass
        else:
            ner, _ = NerSample.objects.get_or_create(
                text=row[text_col], entity_json=row['dict']
            )


def create_ner_samples_from_list(ner_list, limit=10):
    for row in ner_list:
        if len(row[0]) > limit:
            ner = NerSample.objects.get_or_create(
                text=row[0], entity_json=row[1]
            )


def create_ner_sample_from_qs(app_label, model_label, textfield, endpoint, start=0, limit=None):
    url = endpoint
    try:
        ct = ContentType.objects.get(app_label=app_label, model=model_label).model_class()
    except ObjectDoesNotExist:
        ct = None
    if ct:
        qs = ct.objects.all()
        if qs:
            try:
                limit = int(limit)
            except TypeError:
                limit = qs.count()
            for x in qs[start:limit]:
                obj_text = getattr(x, textfield, 'None')
                if obj_text:
                    text = "{}".format(obj_text).strip()
                else:
                    text = None
                if text:
                    payload = {}
                    payload['longtext'] = text
                    payload['dont_split'] = True
                    headers = {'content-type': "application/json; charset=utf-8"}
                    response = requests.request(
                        "POST", url, headers=headers,
                        data=json.dumps(payload)
                    )
                    resp_dict = json.loads(response.text)
                    if resp_dict:
                        for y in resp_dict:
                            ner, _ = NerSample.objects.get_or_create(
                                text=y[0]
                            )
                            ner.entity_json = y[1]
                            ner.content_object = x
                            ner.save()
                            yield ner
