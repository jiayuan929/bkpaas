# Generated by Django 3.2.12 on 2023-12-12 07:10

from django.db import migrations


def is_legacy_custom_collector_config_name(name_en: str, app_code: str, module_name: str):
    json_name = f"bkapp__{app_code}__{module_name}__json".replace("-", "_")
    stdout_name = f"bkapp__{app_code}__{module_name}__stdout".replace("-", "_")
    return name_en in [json_name, stdout_name]


def init_is_builtin_field(apps, schema_editor):
    """初始化 CustomCollectorConfig.is_builtin 字段"""
    CustomCollectorConfig = apps.get_model('log', 'CustomCollectorConfig')
    qs = CustomCollectorConfig.objects.all()

    for item in qs:
        module = item.module
        app_code = module.application.code
        module_name = module.name
        if is_legacy_custom_collector_config_name(item.name_en, app_code, module_name):
            item.is_builtin = True
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0005_auto_20231211_1121'),
    ]

    operations = [migrations.RunPython(init_is_builtin_field)]
