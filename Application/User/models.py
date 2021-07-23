from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = None
    last_name = None
    nick_name = models.CharField('昵称', max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'user'
