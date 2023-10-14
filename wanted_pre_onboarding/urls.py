"""
URL configuration for wanted_pre_onboarding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from accounts.views import UserViewSet
from companies.views import CompanyViewSet
from jobs.views import JobPostingViewSet, JobPostingApplicationViewSet

router = DefaultRouter()
router.register(r'job-postings', JobPostingViewSet)
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
jop_posting_router = NestedDefaultRouter(router, r'job-postings', lookup='job_posting')
jop_posting_router.register(r'apply', JobPostingApplicationViewSet, basename='jobposting-apply')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path(f'api/{settings.API_VERSION}/', include(router.urls)),
    path(f'api/{settings.API_VERSION}/', include(jop_posting_router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
