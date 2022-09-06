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
Sync Bazel workspace to the Raspberry Pi.
"""

from .utils import sh
from .workspace import Workspace


def sync(workspace: Workspace, destination: str) -> None:
    """
    Synchronize Bazel workspace with remote host.

    Args:
        workspace: Bazel workspace information.
        destination: Destination in rsync+ssh format ``[user@]host:path``.

    Note:
        If the destination is only a host (without a path), the default path is
        set from the workspace name.
    """
    bazel_bin = workspace.bazel_bin
    if ":" in destination:
        host, remote_path = destination.split(":")
        if len(remote_path) < 1:
            remote_path = workspace.name
    else:  # ":" not in destination
        host = destination
        remote_path = workspace.name
    sh(f"ssh {host} mkdir -p {remote_path}")
    sh(f"rsync -Lrtu --delete {bazel_bin}/ {host}:{remote_path}/bazel-bin/")
    sh(f"scp {workspace.root}/WORKSPACE {host}:{remote_path}/WORKSPACE")
