# Generated by Django 3.2 on 2021-07-22 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('type', models.SmallIntegerField(null=True, verbose_name='文章类型')),
                ('created_time', models.DateTimeField(verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(blank=True, null=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户名id')),
            ],
            options={
                'db_table': 'blog',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Blog.blog')),
                ('reply', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='Blog.comment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
