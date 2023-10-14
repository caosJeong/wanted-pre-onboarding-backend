from rest_framework import serializers

from .models import JobPosting, Application


class JobPostingListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_country = serializers.CharField(source='company.country', read_only=True)
    company_location = serializers.CharField(source='company.location', read_only=True)

    class Meta:
        model = JobPosting
        fields = (
            'id', 'company', 'company_name', 'company_country', 'company_location', 'position', 'reward', 'skills'
        )


class JobPostingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ('position', 'reward', 'skills', 'content')


class JobPostingDetailSerializer(JobPostingListSerializer):
    company_another_postings = serializers.ListField(child=serializers.IntegerField(), source='another_ids')

    class Meta:
        model = JobPosting
        fields = (
            'id', 'company_name', 'company_country', 'company_location', 'position',
            'reward', 'content', 'skills', 'company_another_postings'
        )


class ApplicationSerializer(serializers.ModelSerializer):
    job_posting_content = serializers.CharField(source='job_posting.content', read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'job_posting', 'job_posting_content', 'applicant')
