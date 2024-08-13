# Generated by Django 3.2.25 on 2024-08-12 12:42

from django.db import migrations, models
import paasng.bk_plugins.pluginscenter.models.definitions


class Migration(migrations.Migration):

    dependencies = [
        ('pluginscenter', '0022_auto_20240730_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pluginvisiblerangedefinition',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='pluginvisiblerangedefinition',
            name='description_zh_cn',
        ),
        migrations.RemoveField(
            model_name='pluginvisiblerangedefinition',
            name='scope',
        ),
        migrations.AddField(
            model_name='pluginvisiblerangedefinition',
            name='api',
            field=paasng.bk_plugins.pluginscenter.models.definitions.PluginBackendAPIField(null=True),
        ),
        migrations.AddField(
            model_name='pluginvisiblerangedefinition',
            name='initial',
            field=paasng.bk_plugins.pluginscenter.models.definitions.PluginVisibleRangeLevelField(null=True),
        ),
        migrations.AlterField(
            model_name='operationrecord',
            name='subject',
            field=models.CharField(choices=[('plugin', '插件'), ('test_version', '测试版本'), ('version', '版本'), ('basic_info', '基本信息'), ('logo', 'logo'), ('market_info', '市场信息'), ('config_info', '配置信息'), ('visible_range', '可见范围'), ('publisher', '发布者'), ('release_strategy', '发布策略')], max_length=32),
        ),
    ]
