# Generated by Django 4.2.7 on 2023-12-29 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_websocket'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AlterField(
            model_name='message',
            name='session_key',
            field=models.CharField(max_length=80, verbose_name='sessionid'),
        ),
        migrations.AlterField(
            model_name='websocket',
            name='key',
            field=models.CharField(max_length=80, verbose_name='websocket连接'),
        ),
    ]
