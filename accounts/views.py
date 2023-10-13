from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from accounts.serializers import UserSerializer
from companies.serializers import CompanySerializer

User = get_user_model()


@extend_schema(request=UserSerializer, responses=UserSerializer)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CompanySerializer
