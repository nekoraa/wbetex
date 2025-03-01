# Generated by Django 4.2.6 on 2023-10-22 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DENGLUZHUCE', '0002_用户信息'),
    ]

    operations = [
        migrations.CreateModel(
            name='游戏帖子',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('链接', models.URLField(verbose_name='链接')),
                ('标题', models.CharField(max_length=200, verbose_name='标题')),
                ('内容', models.TextField(verbose_name='内容')),
                ('日期', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('封面', models.ImageField(blank=True, null=True, upload_to='game_images/', verbose_name='游戏图片')),
                ('发帖人', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发帖人')),
            ],
        ),
        migrations.CreateModel(
            name='游戏帖子图片',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('图片', models.FileField(upload_to='game_images/', verbose_name='游戏图片')),
                ('游戏帖子', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='游戏图片', to='DENGLUZHUCE.游戏帖子', verbose_name='游戏帖子')),
            ],
        ),
    ]
