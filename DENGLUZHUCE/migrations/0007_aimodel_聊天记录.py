# Generated by Django 4.2.6 on 2024-03-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DENGLUZHUCE', '0006_aimodel_chatrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='聊天记录',
            field=models.TextField(default=123, max_length=100000000),
            preserve_default=False,
        ),
    ]
