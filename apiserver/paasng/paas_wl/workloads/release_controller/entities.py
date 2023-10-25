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
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from paasng.platform.engine.constants import ImagePullPolicy


@dataclass
class ContainerRuntimeSpec:
    """The runtime specification of a container which contains image, command and
    other info. Used for building Command and SlugBuilderTemplate.
    """

    image: str
    # The actual command for starting the container
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None
    envs: Dict[str, str] = field(default_factory=dict)
    image_pull_policy: ImagePullPolicy = field(default=ImagePullPolicy.IF_NOT_PRESENT)
    image_pull_secrets: List[Dict[str, str]] = field(default_factory=list)
