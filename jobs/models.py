from django.db import models

from accounts.models import CustomUser
from companies.models import Company


class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()
    skills = models.CharField(max_length=100)

    def __str__(self):
        return self.position


class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete)
