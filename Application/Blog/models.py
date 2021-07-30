from django.db import models
from Application.User.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='用户名id')
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    type = models.SmallIntegerField('文章类型', null=True)
    created_time = models.DateTimeField('创建时间')
    updated_time = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        db_table = 'blog'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, default=None, null=True)
    content = models.CharField('评论内容', max_length=255)
    created_time = models.DateTimeField('评论时间')

    class Meta:
        db_table = 'comment'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, blank=True, null=True)
    created_time = models.DateTimeField('点赞时间')

    class Meta:
        db_table = 'like'
