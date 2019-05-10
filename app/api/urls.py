from django.urls import path

from .views import PerformanceMetricView

urlpatterns = [
    path('metrics', PerformanceMetricView.as_view(), name='metrics'),
]
