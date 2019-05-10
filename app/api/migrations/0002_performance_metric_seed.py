import csv
import os
import pytz

from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import migrations


def read_csv(path):
    result = []
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        col_names = [x.lower() for x in next(reader)]
        # Look through each line and construct dict
        [result.extend([dict(zip(col_names, line))]) for line in reader]
    return result


def is_valid_csv_seed(path, headers):
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        # lowercase col names just in case
        col_names = [x.lower() for x in next(reader)]
        diff = set(headers) - set(col_names)
    return True if not diff else False


def convert_metric_data(metric_data, model_cls):
    '''
    :param metric_data: dict data from csv seed file.
    :param model_cls: PerformanceMetric model class.
    :return: List of PerformanceMetric objects to insert.
    '''
    result = []
    for csv_metric in metric_data:
        result.append(model_cls(
            date=pytz.utc.localize(datetime.strptime(csv_metric['date'], "%d.%m.%Y", )),
            channel=csv_metric['channel'],
            country=csv_metric['country'],
            os=csv_metric['os'],
            impressions=int(csv_metric['impressions']),
            clicks=int(csv_metric['clicks']),
            installs=int(csv_metric['installs']),
            spend=float(csv_metric['spend']),
            revenue=float(csv_metric['revenue'])
        ))
    return result


def apply_seed(apps, schema):
    headers = ['date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue']
    csv_seed_path = os.path.join(settings.PROJECT_DIR, settings.CSV_SEED_FILENAME)
    if not os.path.exists(csv_seed_path):
        raise ValidationError('{} is not found.'.format(csv_seed_path))
    elif not os.access(csv_seed_path, os.R_OK):
        raise ValidationError('Cound not read .csv file. Check permissions.')
    elif not is_valid_csv_seed(csv_seed_path, headers):
        raise ValidationError('.csv file is not valid. Please, check file headers.')

    PerformanceMetric = apps.get_model('api', 'PerformanceMetric')
    performance_metrics_data = read_csv(csv_seed_path)
    performance_metrics = convert_metric_data(performance_metrics_data, PerformanceMetric)
    PerformanceMetric.objects.bulk_create(performance_metrics)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('api', '0001_performance_metric_model'),
    ]

    operations = [
        migrations.RunPython(apply_seed)
    ]
