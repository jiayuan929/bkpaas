# Generated by Django 4.2.16 on 2024-12-12 11:21

from django.db import migrations
import paasng.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ("pluginscenter", "0025_auto_20240827_1624"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operationrecord",
            name="operator",
            field=paasng.utils.models.BkUserField(
                blank=True, db_index=True, max_length=128, null=True
            ),
        ),
        migrations.AlterField(
            model_name="plugininstance",
            name="creator",
            field=paasng.utils.models.BkUserField(
                blank=True, db_index=True, max_length=128, null=True
            ),
        ),
        migrations.AlterField(
            model_name="pluginrelease",
            name="creator",
            field=paasng.utils.models.BkUserField(
                blank=True, db_index=True, max_length=128, null=True
            ),
        ),
    ]
