# Generated by Django 3.2.25 on 2024-08-08 03:10

from django.db import migrations, models
import django.db.models.deletion
import paasng.infras.iam.constants
import paasng.misc.audit.constants
import paasng.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0012_application_is_ai_agent_app'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminOperationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(help_text='仅需要后台执行的的操作才需要记录结束时间', null=True)),
                ('access_type', models.IntegerField(choices=[(0, '网页'), (1, 'API')], default=paasng.misc.audit.constants.AccessType['WEB'], verbose_name='访问方式')),
                ('result_code', models.IntegerField(choices=[(0, '成功'), (1, '执行中'), (-1, '失败'), (-2, '中断')], default=paasng.misc.audit.constants.ResultCode['SUCCESS'], verbose_name='操作结果')),
                ('data_before', models.JSONField(blank=True, null=True, verbose_name='操作前的数据')),
                ('data_after', models.JSONField(blank=True, null=True, verbose_name='操作后的数据')),
                ('operation', models.CharField(choices=[('create', '新建'), ('delete', '删除'), ('create_app', '创建应用'), ('online_to_market', '发布到应用市场'), ('offline_from_market', '从应用市场下架'), ('modify_market_info', '完善应用市场配置'), ('modify_market_url', '修改应用市场访问地址'), ('modify_basic_info', '修改基本信息'), ('start', '启动'), ('stop', '停止'), ('scale', '扩缩容'), ('enable', '启用'), ('disable', '停用'), ('apply', '申请'), ('renew', '续期'), ('deploy', '部署'), ('offline', '下架')], max_length=32, verbose_name='操作类型')),
                ('target', models.CharField(choices=[('app', '应用'), ('module', '模块'), ('process', '进程'), ('access_control', '用户限制'), ('cloud_api', '云 API 权限'), ('secret', '密钥'), ('env_var', '环境变量'), ('addon', '增强服务')], max_length=32, verbose_name='操作对象')),
                ('attribute', models.CharField(blank=True, help_text='如增强服务的属性可以为：mysql、bkrepo', max_length=32, null=True, verbose_name='对象属性')),
                ('module_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='模块名，非必填')),
                ('environment', models.CharField(blank=True, choices=[('stag', '预发布环境'), ('prod', '生产环境')], max_length=16, null=True, verbose_name='环境，非必填')),
                ('app_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='应用ID, 非必填')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppOperationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(help_text='仅需要后台执行的的操作才需要记录结束时间', null=True)),
                ('access_type', models.IntegerField(choices=[(0, '网页'), (1, 'API')], default=paasng.misc.audit.constants.AccessType['WEB'], verbose_name='访问方式')),
                ('result_code', models.IntegerField(choices=[(0, '成功'), (1, '执行中'), (-1, '失败'), (-2, '中断')], default=paasng.misc.audit.constants.ResultCode['SUCCESS'], verbose_name='操作结果')),
                ('data_before', models.JSONField(blank=True, null=True, verbose_name='操作前的数据')),
                ('data_after', models.JSONField(blank=True, null=True, verbose_name='操作后的数据')),
                ('operation', models.CharField(choices=[('create', '新建'), ('delete', '删除'), ('create_app', '创建应用'), ('online_to_market', '发布到应用市场'), ('offline_from_market', '从应用市场下架'), ('modify_market_info', '完善应用市场配置'), ('modify_market_url', '修改应用市场访问地址'), ('modify_basic_info', '修改基本信息'), ('start', '启动'), ('stop', '停止'), ('scale', '扩缩容'), ('enable', '启用'), ('disable', '停用'), ('apply', '申请'), ('renew', '续期'), ('deploy', '部署'), ('offline', '下架')], max_length=32, verbose_name='操作类型')),
                ('target', models.CharField(choices=[('app', '应用'), ('module', '模块'), ('process', '进程'), ('access_control', '用户限制'), ('cloud_api', '云 API 权限'), ('secret', '密钥'), ('env_var', '环境变量'), ('addon', '增强服务')], max_length=32, verbose_name='操作对象')),
                ('attribute', models.CharField(blank=True, help_text='如增强服务的属性可以为：mysql、bkrepo', max_length=32, null=True, verbose_name='对象属性')),
                ('module_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='模块名，非必填')),
                ('environment', models.CharField(blank=True, choices=[('stag', '预发布环境'), ('prod', '生产环境')], max_length=16, null=True, verbose_name='环境，非必填')),
                ('app_code', models.CharField(max_length=32, verbose_name='应用ID, 必填')),
                ('action_id', models.CharField(blank=True, choices=[('view_basic_info', '基础信息查看'), ('edit_basic_info', '基础信息编辑'), ('delete_application', '应用删除'), ('manage_members', '成员管理'), ('manage_access_control', '访问控制管理'), ('manage_app_market', '应用市场管理'), ('data_statistics', '数据统计'), ('basic_develop', '基础开发'), ('manage_cloud_api', '云 API 管理'), ('view_alert_records', '告警记录查看'), ('edit_alert_policy', '告警策略配置'), ('manage_addons_services', '增强服务管理'), ('manage_env_protection', '部署环境限制管理'), ('manage_module', '模块管理')], help_text='action_id 为空则不会将数据上报到审计中心', max_length=32, null=True)),
                ('resource_type_id', models.CharField(choices=[('application', 'Application'), ('space', 'Bkmonitorspace'), ('apm_application', 'Bkmonitorapm'), ('grafana_dashboard', 'Bkmonitordashboard'), ('indices', 'Bklogindices'), ('collection', 'Bklogcollection'), ('es_source', 'Bklogessource')], default=paasng.infras.iam.constants.ResourceType['Application'], help_text='开发者中心注册的资源都为蓝鲸应用', max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppLatestOperationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latest_operated_at', models.DateTimeField(db_index=True)),
                ('application', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='latest_op_record', to='applications.application')),
                ('operation', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='audit.appoperationrecord')),
            ],
        ),
    ]
