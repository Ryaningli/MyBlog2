from django.db import models
from Application.User.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='用户名id')
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    type = models.SmallIntegerField('文章类型', null=True)
    like_count = models.IntegerField('点赞数', default=0)
    views_count = models.IntegerField('浏览数', default=0)
    created_time = models.DateTimeField('创建时间')
    updated_time = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        db_table = 'blog'
        ordering = ['-created_time']       # 默认排序


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    content = models.CharField('评论内容', max_length=255)
    blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING, null=True, related_name='comments')
    lv1_comment = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True, related_name='所属一级评论')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True, related_name='父评论')
    level = models.SmallIntegerField('评论等级', default=1)
    like_count = models.IntegerField('点赞数', default=0)
    created_time = models.DateTimeField('评论时间')
    state = models.SmallIntegerField('状态', default=1)

    class Meta:
        db_table = 'comment'
        ordering = ['-created_time']       # 默认排序


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, blank=True, null=True)
    created_time = models.DateTimeField('点赞时间')

    class Meta:
        db_table = 'like'
