import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, precision_recall_fscore_support
from django.conf import settings

from . models import NerSample


def annotation_scores(request):
    results = {}
    samples = NerSample.objects.exclude(entity_checked__isnull=True)
    if samples:
        results['nr_checked'] = samples.count()
        results['nr_all'] = NerSample.objects.all().count()
        samples = samples.values_list(
            'id',
            'text',
            'entity_checked',
            'entity_json'
        )
        df = pd.DataFrame(list(samples), columns=['id', 'text', 'checked', 'guess'])
        df['entities_checked'] = df.apply(lambda x: x['checked']['entities'], axis=1)
        df['entities_guess'] = df.apply(lambda x: x['guess']['entities'], axis=1)
        df['entities_checked_str'] = df.apply(
            lambda x: "{}".format(x['checked']['entities']),
            axis=1
        )
        df['entities_guess_str'] = df.apply(lambda x: "{}".format(x['guess']['entities']), axis=1)
        df['entities_checked_count'] = df.apply(lambda x: len(x['checked']['entities']), axis=1)
        df['entities_guess_count'] = df.apply(lambda x: len(x['guess']['entities']), axis=1)

        y_true = np.array(df['entities_checked_str'])
        y_pred = np.array(df['entities_guess_str'])
        results['f1_str'] = precision_recall_fscore_support(y_true, y_pred, average='micro')
        results['cks_str'] = cohen_kappa_score(y_true, y_pred)

        y_true = np.array(df['entities_checked_count'])
        y_pred = np.array(df['entities_guess_count'])
        results['f1_count'] = precision_recall_fscore_support(y_true, y_pred, average='micro')
        results['cks_count'] = cohen_kappa_score(y_true, y_pred)

        return results
    else:
        return {
            "f1_count": "No samples created yet",
            "cks_count": "No samples created yet"
        }
