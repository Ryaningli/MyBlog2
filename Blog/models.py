from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    first_name = None
    last_name = None
    nick_name = models.CharField(max_length=150, blank=True, null=True)


class Blog(models.Model):
    user_id = None
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()


class Test(models.Model):
    fie = models.CharField(max_length=10)