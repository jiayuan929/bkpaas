# -*- coding: utf-8 -*-
# TencentBlueKing is pleased to support the open source community by making
# 蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
# Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# We undertake not to change the open source license (MIT license) applicable
# to the current version of the project delivered to anyone in the future.

# 请谨慎使用 signal 来添加审计记录，目前仅保留除操作审计外的其他操作的 signal

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from paas_wl.bk_app.cnative.specs.constants import DeployStatus
from paas_wl.bk_app.cnative.specs.models import AppModelDeploy
from paas_wl.bk_app.cnative.specs.signals import post_cnative_env_deploy
from paasng.infras.iam.permissions.resources.application import AppAction
from paasng.misc.audit import constants
from paasng.misc.audit.utils import add_app_audit_record
from paasng.platform.applications.models import Application, ModuleEnvironment
from paasng.platform.engine.constants import JobStatus
from paasng.platform.engine.models import Deployment
from paasng.platform.engine.signals import post_appenv_deploy
from paasng.platform.modules.models import Module

logger = logging.getLogger(__name__)

JOB_STATUS_TO_RESULT_CODE = {
    JobStatus.SUCCESSFUL: constants.ResultCode.SUCCESS,
    JobStatus.FAILED: constants.ResultCode.FAILURE,
    JobStatus.PENDING: constants.ResultCode.ONGOING,
    JobStatus.INTERRUPTED: constants.ResultCode.INTERRUPT,
}
DEPLOY_STATUS_TO_RESULT_CODE = {
    DeployStatus.PENDING: constants.ResultCode.ONGOING,
    DeployStatus.PROGRESSING: constants.ResultCode.ONGOING,
    DeployStatus.READY: constants.ResultCode.SUCCESS,
    DeployStatus.ERROR: constants.ResultCode.FAILURE,
    DeployStatus.UNKNOWN: constants.ResultCode.FAILURE,
}


@receiver(post_save)
def on_model_post_save(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    """记录应用、模块创建操作记录"""
    # 创建应用
    if isinstance(instance, Application) and created:
        add_app_audit_record(
            app_code=instance.code,
            # 创建应用未在权限中心注册，因此操作也不能上报到设计中心
            action_id="",
            user=instance.owner,
            operation=constants.OperationEnum.CREATE_APP,
            target=constants.OperationTarget.APP,
        )
    # 创建模块
    elif isinstance(instance, Module) and created:
        add_app_audit_record(
            app_code=instance.application.code,
            user=instance.creator,
            action_id=AppAction.MANAGE_MODULE,
            operation=constants.OperationEnum.CREATE,
            target=constants.OperationTarget.MODULE,
            attribute=instance.name,
        )


@receiver(post_appenv_deploy)
def on_deploy_finished(sender: ModuleEnvironment, deployment: Deployment, **kwargs):
    """Create new operation record when a deployment has finished"""
    application = deployment.app_environment.application
    result_code = JOB_STATUS_TO_RESULT_CODE.get(deployment.status, constants.ResultCode.ONGOING)
    add_app_audit_record(
        app_code=application.code,
        user=deployment.operator,
        action_id=AppAction.BASIC_DEVELOP,
        operation=constants.OperationEnum.DEPLOY,
        target=constants.OperationTarget.APP,
        source_object_id=deployment.id.hex,
        module_name=deployment.app_environment.module.name,
        env=deployment.app_environment.environment,
        result_code=result_code,
    )


@receiver(post_cnative_env_deploy)
def on_cnative_deploy_finished(sender: ModuleEnvironment, deploy: AppModelDeploy, **kwargs):
    """当云原生应用部署完成后，记录操作审计记录"""
    application = Application.objects.get(id=deploy.application_id)
    result_code = DEPLOY_STATUS_TO_RESULT_CODE.get(deploy.status, constants.ResultCode.ONGOING)
    add_app_audit_record(
        app_code=application.code,
        user=deploy.operator,
        action_id=AppAction.BASIC_DEVELOP,
        operation=constants.OperationEnum.DEPLOY,
        target=constants.OperationTarget.APP,
        source_object_id=deploy.pk,
        module_name=deploy.module.name,
        env=deploy.environment_name,
        result_code=result_code,
        data_type=constants.DataType.BKAPP_REVERSION,
        data_after=deploy.revision.id,
    )