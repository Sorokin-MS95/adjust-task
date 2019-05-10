from django.db.models import manager

from django.db.models import F, ExpressionWrapper, DecimalField


class PerformanceMetricManager(manager.Manager):

    def with_cpi(self):
        '''
        Using annotate to add calculated fields: CPI.
        :return: QuerySet
        '''
        return self.model.objects.annotate(
            cpi=ExpressionWrapper(
                F('spend') / F('installs'), output_field=DecimalField()
            )
        )
