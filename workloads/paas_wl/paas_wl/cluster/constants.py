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
from blue_krill.data_types.enum import EnumField, StructuredEnum
from django.utils.translation import gettext_lazy as _


class ClusterTokenType(int, StructuredEnum):
    SERVICE_ACCOUNT = 1


class ClusterType(str, StructuredEnum):
    """集群类别"""

    NORMAL = EnumField('normal', label=_('普通集群'))
    VIRTUAL = EnumField('virtual', label=_('虚拟集群'))


class ClusterFeatureFlag(str, StructuredEnum):
    """集群特性标志"""

    ENABLE_EGRESS_IP = EnumField('enable_egress_ip', label=_('支持提供出口 IP'))
    ENABLE_MOUNT_LOG_TO_HOST = EnumField('enable_mount_log_to_host', label=_('允许挂载日志到主机'))
