# Generated by Django 4.2.6 on 2024-03-11 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DENGLUZHUCE', '0009_aimodel_ai名字_aimodel_最大输出字数_aimodel_检索记忆长度_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='相似度阈值',
            field=models.TextField(default='0.5'),
        ),
    ]
