from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    first_name = None
    last_name = None
    nick_name = models.CharField('昵称', max_length=150, blank=True, null=True)


class Blog(models.Model):
    user_id = None
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    created_time = models.DateTimeField('创建时间')
    updated_time = models.DateTimeField('更新时间')
