# Generated by Django 4.0.2 on 2022-03-17 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcall',
            name='first_name_client',
            field=models.CharField(max_length=150, verbose_name='имя клиента'),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='first_name_client',
            field=models.CharField(max_length=150, verbose_name='имя клиента'),
        ),
    ]
