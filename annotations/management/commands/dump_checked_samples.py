import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from annotations.models import NerSample


class Command(BaseCommand):

    help = "Dump annotations as csv"

    def handle(self, *args, **kwargs):
        output_file = os.path.join('data', 'checked_samples.csv')
        samples = NerSample.objects.exclude(
            entity_checked__isnull=True
        ).values_list('text', 'entity_checked')

        df = pd.DataFrame(list(samples), columns=['text', 'entities'])
        df.to_csv(output_file, index=False)
        self.stdout.write(
            "dumped {} samples to 'checked_samples.csv'".format(len(df.index))
        )
