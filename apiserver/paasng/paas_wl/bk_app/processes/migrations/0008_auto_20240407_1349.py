# Generated by Django 3.2.12 on 2024-04-07 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0007_auto_20231127_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processspec',
            name='image',
        ),
        migrations.RemoveField(
            model_name='processspec',
            name='image_credential_name',
        ),
        migrations.RemoveField(
            model_name='processspec',
            name='image_pull_policy',
        ),
    ]