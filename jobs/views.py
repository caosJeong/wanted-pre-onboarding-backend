import django_filters
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_nested.viewsets import NestedViewSetMixin

from .filters import JobPostingFilter
from .models import JobPosting, Application
from .serializers import JobPostingDetailSerializer, ApplicationSerializer, JobPostingListSerializer, \
    JobPostingUpdateSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.prefetch_related('company').all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = JobPostingFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobPostingDetailSerializer
        elif self.action == 'partial_update':
            return JobPostingUpdateSerializer
        return JobPostingListSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        another_ids = list(self.queryset.filter(company_id=obj.company_id).values_list('id', flat=True))
        obj.another_ids = another_ids
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


@extend_schema(exclude=True)
class JobPostingApplicationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    parent_lookup_kwargs = {'job_posting_pk': 'job_posting'}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch('job_posting', queryset=JobPosting.objects.prefetch_related('company')))
