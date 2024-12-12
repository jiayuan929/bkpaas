# Generated by Django 4.2.16 on 2024-12-12 11:12

from django.db import migrations
import paas_wl.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ("specs", "0008_auto_20240327_0941"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appmodeldeploy",
            name="operator",
            field=paas_wl.utils.models.BkUserField(
                blank=True, db_index=True, max_length=128, null=True, verbose_name="操作者"
            ),
        ),
    ]
