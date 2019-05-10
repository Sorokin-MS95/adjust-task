from django.db import models

from .managers import PerformanceMetricManager


class PerformanceMetric(models.Model):
    date = models.DateTimeField(auto_now=False, blank=False)
    channel = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    os = models.CharField(max_length=50, blank=False, null=False)
    impressions = models.IntegerField(blank=False, null=False)
    clicks = models.IntegerField(null=False, blank=False)
    installs = models.IntegerField(null=False, blank=False)
    spend = models.FloatField(blank=False, null=False)
    revenue = models.FloatField(blank=False, null=False)

    objects = PerformanceMetricManager()
