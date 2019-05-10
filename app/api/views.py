from django.utils.decorators import method_decorator

from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination

from .filters import METRIC_PARAM_FILTER_MAPPING
from .models import PerformanceMetric
from .decorators import validate_query_params
from .serializers import MetricsQueryParamSerializer, PerformanceMetricSerializer, PerformanceMetricGroupBySerializer


class PerformanceMetricView(GenericAPIView):
    queryset = PerformanceMetric.objects.with_cpi()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.query_params.get('group'):
            return PerformanceMetricGroupBySerializer
        return PerformanceMetricSerializer

    def filter_queryset(self, queryset):
        '''
        This is done to apply filters based on GET params using mapping dict.
        :param queryset:
        :return:
        '''
        filter_backends = []
        for query_param in self.request.query_params:
            if query_param in METRIC_PARAM_FILTER_MAPPING:
                filter_backends.append(METRIC_PARAM_FILTER_MAPPING[query_param])

        for backend in filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    @method_decorator([validate_query_params(serializer_cls=MetricsQueryParamSerializer)])
    def get(self, request):
        qs = self.filter_queryset(self.queryset).all()
        page = self.paginator.paginate_queryset(qs, request)
        serializer = self.get_serializer_class()(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)
