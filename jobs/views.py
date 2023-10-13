from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import JobPosting, Application
from .serializers import JobPostingSerializer, ApplicationSerializer


@extend_schema(request=JobPostingSerializer, responses=JobPostingSerializer)
class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(request=ApplicationSerializer, responses=ApplicationSerializer)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
