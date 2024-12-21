# Generated by Django 4.2.16 on 2024-12-21 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("log", "0006_auto_20231212_1510"),
    ]

    operations = [
        migrations.AddField(
            model_name="elasticsearchconfig",
            name="tenant_id",
            field=models.CharField(
                db_index=True,
                default="default",
                help_text="本条数据的所属租户",
                max_length=32,
                verbose_name="租户 ID",
            ),
        ),
    ]