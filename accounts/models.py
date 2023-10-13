from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # 사용자에 대한 추가 필드를 정의할 수 있습니다.
    # 예를 들어, 프로필 이미지, 전화번호 등
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
