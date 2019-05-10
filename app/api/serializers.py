from rest_framework import serializers

from .models import PerformanceMetric

QUERY_DATE_PARAMS_FORMAT = "%d.%m.%Y"
QUERY_ORDER_PARAMS_CHOICES = ['date', '-date', '-channel', 'channel', '-country', 'country', '-os', 'os',
                              '-impressions', 'impressions', '-clicks', 'clicks', '-installs', 'installs', '-spend',
                              'spend', '-revenue', 'revenue', '-cpi', 'cpi']
QUERY_GROUP_PARAMS_CHOICES = ['date', 'channel', 'country', 'os']


def valid_order_param(value):
    for param in value:
        if param not in QUERY_ORDER_PARAMS_CHOICES:
            raise serializers.ValidationError('"{}" is not a valid order parameter.'.format(param))


def valid_group_param(value):
    for param in value:
        if param not in QUERY_GROUP_PARAMS_CHOICES:
            raise serializers.ValidationError('"{}" is not a valid group parameter.'.format(param))


class MetricsQueryParamSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField(required=False, input_formats=[QUERY_DATE_PARAMS_FORMAT])
    date_to = serializers.DateTimeField(required=False, input_formats=[QUERY_DATE_PARAMS_FORMAT])

    channel = serializers.ListField(
        child=serializers.CharField(required=False, max_length=255),
        min_length=0, required=False
    )

    country = serializers.ListField(
        child=serializers.CharField(required=False, max_length=255),
        min_length=0, required=False
    )

    os = serializers.ListField(
        child=serializers.CharField(required=False, max_length=255),
        min_length=0, required=False
    )

    order = serializers.ListField(max_length=255, validators=[valid_order_param], required=False)

    group = serializers.ListField(max_length=255, validators=[valid_group_param], required=False, min_length=0)


class PerformanceMetricSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format=QUERY_DATE_PARAMS_FORMAT)
    cpi = serializers.DecimalField(max_digits=9, decimal_places=3)

    class Meta:
        model = PerformanceMetric
        fields = ['date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue', 'cpi']


class PerformanceMetricGroupBySerializer(serializers.Serializer):
    # We're using a new serializer in case adding new fields in the foreseeable future.
    date = serializers.DateTimeField(format=QUERY_DATE_PARAMS_FORMAT, required=False)
    country = serializers.CharField(max_length=255, required=False)
    channel = serializers.CharField(max_length=255, required=False)
    os = serializers.CharField(max_length=255, required=False)

    clicks = serializers.IntegerField()
    impressions = serializers.IntegerField()
    installs = serializers.IntegerField()
    revenue = serializers.IntegerField()
    cpi = serializers.DecimalField(max_digits=9, decimal_places=3)
