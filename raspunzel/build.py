#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Build Bazel targets locally.
"""

from .utils import sh


def build(target: str, subargs: str, config: str = "pi64") -> None:
    """
    Build Bazel targets specified in a YAML project file.

    Args:
        target: Bazel targets.
        subargs: Arguments to bazel build subcommand.
        config: Bazel configuration to use.
    """
    sh(f"bazel build --config={config} {target} " + " ".join(subargs))
