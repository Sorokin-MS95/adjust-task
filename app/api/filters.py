from datetime import datetime
from functools import reduce

from django.db.models import Q
from rest_framework.filters import BaseFilterBackend

from .serializers import QUERY_DATE_PARAMS_FORMAT

from django.db.models import Sum, Avg


class DateFromFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(date__gte=datetime.strptime(request.query_params['date_from'], QUERY_DATE_PARAMS_FORMAT))


class DateToFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(date__lte=datetime.strptime(request.query_params['date_to'], QUERY_DATE_PARAMS_FORMAT))


class DateFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(date=datetime.strptime(request.query_params['date'], QUERY_DATE_PARAMS_FORMAT))


class ChannelFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # OR expression
        channel_names = request.query_params.getlist('channel')
        q_exp = map(lambda x: Q(channel__iexact=x), channel_names)
        return queryset.filter(reduce(lambda a, b: a | b, q_exp))


class CountryFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # OR expression
        country_names = request.query_params.getlist('country')
        q_exp = map(lambda x: Q(country__iexact=x), country_names)
        return queryset.filter(reduce(lambda a, b: a | b, q_exp))


class OSFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # OR expression
        os_names = request.query_params.getlist('os')
        q_exp = map(lambda x: Q(os__iexact=x), os_names)
        return queryset.filter(reduce(lambda a, b: a | b, q_exp))


class OrderFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.order_by(*request.query_params.getlist('order'))


class GroupByFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.values(*request.query_params.getlist('group')).annotate(clicks=Sum('clicks'),
                                                                                impressions=Sum('impressions'),
                                                                                installs=Sum('installs'),
                                                                                revenue=Sum('revenue'),
                                                                                cpi=Avg('cpi'))


# Mapping dict is used here to apply filters based on query params.
METRIC_PARAM_FILTER_MAPPING = {
    'date_from': DateFromFilterBackend,
    'date_to': DateToFilterBackend,
    'date': DateFilterBackend,
    'channel': ChannelFilterBackend,
    'country': CountryFilterBackend,
    'os': OSFilterBackend,
    'order': OrderFilterBackend,
    'group': GroupByFilterBackend,
}
