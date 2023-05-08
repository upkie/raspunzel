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

"""Deploy and run Bazel targets on the Raspberry Pi."""

import logging
import os
from os import path
from typing import List

from .workspace import Workspace


def read_arch(bazel_bin, target, name):
    """Read system architecture."""
    suffix = "-2.params"
    if path.exists(f"{bazel_bin}/{target}/{name}_spine-2.params"):
        suffix = "_spine-2.params"  # for C++ agents
    with open(f"{bazel_bin}/{target}/{name}{suffix}", "r") as params:
        for line in params:
            if line.startswith("bazel-out"):
                return line.split("/")[1]


def log_run(target_name: str, arch: str) -> None:
    """Log target name and build configuration.

    Args:
        target_name: Name of the Bazel target.
        arch: Build configuration found.
    """
    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"
    RESET: str = "\033[0m"

    target_message = f"Found target {YELLOW}{target_name}{RESET}"
    target_message += "for build configuration "
    color = RED
    if "opt" in arch:
        color = GREEN
    elif "fastbuild" in arch:
        color = YELLOW
    elif "unknown" in arch:
        color = RED
    target_message += color + arch + RESET
    logging.info(target_message)


def run(workspace: Workspace, target: str, subargs: List[str]) -> None:
    """Run target from a Bazel workspace.

    Args:
        workspace: Bazel workspace information.
        target: Label of the Bazel target to run.
        subargs: Command-line arguments for the target.
    """
    try:
        if ":" in target:
            target_dir, target_name = target.split(":")
        else:  # target name is directory name
            target_dir = target
            target_name = target.split("/")[-1]
    except ValueError as e:
        raise ValueError(
            f"{target} does not appear to be a valid Bazel label"
        ) from e
    target_dir = target_dir.lstrip("/")
    if target_dir[0] == "@":
        external_name, target_dir = target_dir[1:].split("//")
        target_dir = f"external/{external_name}/{target_dir}"

    try:
        arch = read_arch(workspace.bazel_bin, target_dir, target_name)
    except FileNotFoundError:
        logging.warning(
            "Couldn't read arch from "
            f"'{workspace.bazel_bin}/{target_dir}/{target_name}-2.params', "
            "maybe the target is not a Python script?"
        )
        arch = "unknown"

    log_run(target_name, arch)

    execution_path = (
        f"{workspace.bazel_bin}/{target_dir}/"
        f"{target_name}.runfiles/{workspace.name}/{target_dir}"
    )

    os.chdir(execution_path)
    os.execv(target_name, [target_name] + subargs)
