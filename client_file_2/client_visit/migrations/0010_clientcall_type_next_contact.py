# Generated by Django 4.0.2 on 2022-03-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_visit', '0009_clientvisit_type_next_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcall',
            name='type_next_contact',
            field=models.CharField(blank=True, choices=[('Звонок', 'Звонок'), ('Визит', 'Визит')], max_length=50, verbose_name='тип следующего контакта'),
        ),
    ]