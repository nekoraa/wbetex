# Generated by Django 4.2.6 on 2023-10-21 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DENGLUZHUCE', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='用户信息',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('个性签名', models.TextField(blank=True)),
                ('头像', models.ImageField(default='blank-profile-picture.png', upload_to='profile_images')),
                ('背景图片', models.ImageField(default='blank-profile-picture.png', upload_to='profile_images')),
                ('用户名', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
