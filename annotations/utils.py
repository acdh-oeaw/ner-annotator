import ast
import pandas as pd

from . models import NerSample


def create_ner_samples_from_csv(file):
    df = pd.read_csv(file)
    df['dict'] = df['1'].map(ast.literal_eval)
    for i, row in df.iterrows():
        if len(row['0']) > 2:
            ner = NerSample.objects.get_or_create(
                text=row['0'], entity_json=row['dict']
            )
