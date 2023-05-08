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

"""Bazel workspace information."""

import logging
from os import path

from .utils import find_file


def get_workspace_name(workspace_file: str) -> str:
    """Read workspace name from WORKSPACE file.

    Args:
        workspace_file: Path to WORKSPACE file.

    Returns:
        Workspace name, if found.

    Raises:
        ValueError: if workspace name could not be found.
    """
    for line in open(workspace_file, encoding="utf-8").readlines():
        if line.startswith('workspace(name = "'):
            return line.split('"')[1]

    raise ValueError(
        "Could not find name in WORKSPACE. "
        "Note that we don't parse Starlark beyond "
        '``workspace(name = "something")``.'
    )


class Workspace:
    """Bazel workspace information.

    Attributes:
        bazel_bin: Path to bazel-bin directory.
        name: Name of the workspace, defined in WORKSPACE file.
        root: Path to the workspace root directory.
    """

    bazel_bin: str
    name: str
    root: str

    def __init__(self):
        """Initialize Bazel workspace information."""
        bazel_bin = find_file("bazel-bin", required=True)
        workspace_file = find_file("WORKSPACE", required=True)
        name = get_workspace_name(workspace_file)
        logging.info(f"Found bazel-bin at {bazel_bin}")
        logging.info(f"Found workspace file at {workspace_file}")
        logging.info(f'Read workspace name as "{name}"')
        self.bazel_bin = bazel_bin
        self.name = name
        self.root = path.dirname(workspace_file)
