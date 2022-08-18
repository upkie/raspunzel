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
Deploy and run Bazel targets on the Raspberry Pi.
"""

import argparse
import os
import sys
from os import path
from typing import Optional, List

from colorama import Fore

__version__ = "0.0.1"


def find_file(name: str, required: bool) -> Optional[str]:
    """
    Search for a file or directory in the script's parent folders.

    Args:
        name: Name of the file or directory to search.
        required: If True, raise an exception if the file is not found.

    Returns:
        File path, if found, None otherwise.

    Raises:
        FileNotFoundError: if the file was not found.
    """
    cur_path = os.getcwd()
    while path:
        bin_path = path.join(cur_path, name)
        if path.exists(bin_path):
            return bin_path
        old_path = cur_path
        cur_path = path.dirname(cur_path)
        if cur_path == old_path:
            break
    if required:
        raise FileNotFoundError(f"Cannot find {name} in parent folders")
    return None


def find_bazel_bin_directory():
    """
    Search for a path in parent folders containing a bazel-bin directory.

    Returns:
        Path to bazel-bin directory.

    Raises:
        FileNotFoundError: if no bazel-bin directory was found.
    """
    return find_file("bazel-bin", required=True)


def read_arch(bazel_bin, target, name):
    suffix = "-2.params"
    if path.exists(f"{bazel_bin}/{target}/{name}_spine-2.params"):
        suffix = "_spine-2.params"  # for C++ agents
    with open(f"{bazel_bin}/{target}/{name}{suffix}", "r") as params:
        for line in params:
            if line.startswith("bazel-out"):
                return line.split("/")[1]


def get_workspace_name():
    workspace_file = find_file("WORKSPACE", required=True)
    print(f"workspace_file = {workspace_file}")
    for line in open(workspace_file, encoding="utf-8").readlines():
        if line.startswith('workspace(name = "'):
            return line.split('"')[1]
    raise ValueError(
        "Could not find name in WORKSPACE. "
        "Note that we don't parse Starlark beyond "
        '``workspace(name = "something")``.'
    )


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcmd")

    # raspunzel run --------------------------------------------
    parser_run = subparsers.add_parser(
        "run",
        help="Run a Bazel target",
    )

    parser_run.add_argument("target", help="Bazel target")

    parser_run.add_argument(
        "subargs",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to the target.",
    )
    return parser


def run(workspace_name: str, target: str, subargs: List[str]) -> None:
    try:
        if ":" in target:
            target_dir, target_name = target.split(":")
        else:  # target name is directory name
            target_dir = target
            target_name = target.split("/")[-1]
    except ValueError:
        print(f"{target} does not appear to be a valid Bazel label")
        sys.exit(-2)
    target_dir = target_dir.lstrip("/")
    if target_dir[0] == "@":
        external_name, target_dir = target_dir[1:].split("//")
        target_dir = f"external/{external_name}/{target_dir}"
    bazel_bin = find_bazel_bin_directory()

    try:
        arch = read_arch(bazel_bin, target_dir, target_name)
    except FileNotFoundError:
        print(Fore.YELLOW + "WARNING: " + Fore.RESET, end="")
        print(
            "Couldn't read arch from "
            f"{bazel_bin}/{target_dir}/{target_name}-2.params"
        )
        print("Maybe the target is not a Python script?")
        arch = "unknown"

    execution_path = (
        f"{bazel_bin}/{target_dir}/"
        f"{target_name}.runfiles/{workspace_name}/{target_dir}"
    )

    os.chdir(execution_path)
    print(f"{Fore.GREEN}INFO: {Fore.RESET}", end="")
    print(f"Found target {Fore.YELLOW}{target_name}{Fore.RESET} ", end="")
    print("for build configuration ", end="")
    color = Fore.RED
    if "opt" in arch:
        color = Fore.GREEN
    elif "fastbuild" in arch:
        color = Fore.YELLOW
    elif "unknown" in arch:
        color = Fore.RED
    print(color + arch + Fore.RESET)
    os.execv(target_name, [target_name] + subargs)


def main(argv=None):
    parser = get_argument_parser()
    args = parser.parse_args(argv)
    if args.subcmd is None:
        parser.print_help()
        sys.exit(-1)
    print(args)

    workspace_name = get_workspace_name()
    print(f"workspace_name = {workspace_name}")

    if args.subcmd == "run":
        run(workspace_name, args.target, args.subargs)
