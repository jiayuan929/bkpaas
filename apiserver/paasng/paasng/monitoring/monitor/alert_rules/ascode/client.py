# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

    http://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and
limitations under the License.

We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

import jinja2
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from paasng.accessories.bkmonitorv3.client import make_bk_monitor_client
from paasng.accessories.bkmonitorv3.shim import get_or_create_bk_monitor_space
from paasng.monitoring.monitor.alert_rules.config import RuleConfig
from paasng.platform.applications.models import Application

from .exceptions import AsCodeAPIError

logger = logging.getLogger(__name__)


class AsCodeClient:
    """AsCodeClient 用于向 bkmonitor 下发告警规则

    :param app_code: 应用 code
    :param rule_configs: app 的告警规则配置. 结合 MonitorAsCode 模板, 渲染出 bkmonitor 理解的告警规则
    :param default_receivers: app 的默认告警接收者
    """

    def __init__(self, app_code: str):
        self.app_code = app_code
        self.default_notice_group_name = f"[{self.app_code}] {_('通知组')}"

    def apply_rule_configs(self, rule_configs: List[RuleConfig]):
        """下发告警规则"""
        self._validate(rule_configs)
        configs = self._render_rule_configs(rule_configs)
        self._apply_rule_configs(configs)

    def apply_notice_group(self, receivers: List[str]):
        """下发通知组"""
        tpl_dir = Path(os.path.dirname(__file__))
        loader = jinja2.FileSystemLoader([tpl_dir / 'notice_tpl'])
        j2_env = jinja2.Environment(loader=loader, trim_blocks=True)
        configs = {
            'notice/default_notice.yaml': j2_env.get_template('notice.yaml.j2').render(
                notice_group_name=self.default_notice_group_name, receivers=receivers
            )
        }
        self._apply_rule_configs(configs, f'{self.app_code}_notice_group', incremental=False)

    def _validate(self, rule_configs: List[RuleConfig]):
        for config in rule_configs:
            if config.app_code != self.app_code:
                raise ValueError(
                    f'apply rules error: app_code({config.app_code}) from rule_configs not match '
                    f'app_code({self.app_code})'
                )

    def _render_rule_configs(self, rule_configs: List[RuleConfig]) -> Dict:
        """按照 MonitorAsCode 规则, 渲染出如下示例目录结构:

        └── rule
          ├── high_cpu_usage.yaml
          └── high_mem_usage.yaml
        """
        tpl_dir = Path(os.path.dirname(__file__))
        loader = jinja2.FileSystemLoader([tpl_dir / 'rules_tpl', tpl_dir / 'notice_tpl'])
        j2_env = jinja2.Environment(loader=loader, trim_blocks=True)

        configs = {}
        for conf in rule_configs:
            ctx = conf.to_dict()
            ctx['notice_group_name'] = self.default_notice_group_name
            # 涉及到 rabbitmq 的告警策略, 指标是通过 bkmonitor 配置的采集器采集, 需要添加指标前缀
            if 'rabbitmq' in conf.alert_code:
                ctx['rabbitmq_metric_name_prefix'] = settings.RABBITMQ_MONITOR_CONF.get('metric_name_prefix', '')

            configs[f'rule/{conf.alert_rule_name}.yaml'] = j2_env.get_template(f'{conf.alert_code}.yaml.j2').render(
                **ctx
            )

        return configs

    def _apply_rule_configs(self, configs: Dict, config_group: Optional[str] = None, incremental: bool = True):
        """同步告警配置到 bkmonitor

        :param configs: 告警规则配置
        :param config_group: 配置分组
        :param incremental: 是否增量更新
        """
        space, _ = get_or_create_bk_monitor_space(Application.objects.get(code=self.app_code))
        try:
            make_bk_monitor_client().as_code_import_config(
                configs,
                int(space.iam_resource_id),
                config_group or self.app_code,
                overwrite=False,
                incremental=incremental,
            )
        except Exception as e:
            logger.error(f'ascode import alert rule configs of app_code({self.app_code}) error: {e}')
            raise AsCodeAPIError(e)
