import django_filters
from django.db.models import Q

from jobs.models import JobPosting


class JobPostingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='custom_search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(company__name__icontains=value) | Q(company__country__icontains=value)
            | Q(company__location__icontains=value) | Q(position__icontains=value)
            | Q(content__icontains=value) | Q(skills__icontains=value)
        )

    class Meta:
        model = JobPosting
        fields = ('search',)