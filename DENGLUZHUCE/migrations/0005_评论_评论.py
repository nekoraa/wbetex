# Generated by Django 4.2.6 on 2023-10-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DENGLUZHUCE', '0004_评论'),
    ]

    operations = [
        migrations.AddField(
            model_name='评论',
            name='评论',
            field=models.TextField(default=1, verbose_name='评论'),
            preserve_default=False,
        ),
    ]
