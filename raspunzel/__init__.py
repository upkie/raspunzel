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

import os
import sys
from os import path

from colorama import Fore


def find_bazel_bin_directory():
    """
    Search for a path in the script's parent folders containing a bazel-bin
    folder.
    """
    cur_path = path.abspath(__file__)
    while path:
        bin_path = path.join(cur_path, "bazel-bin")
        if path.exists(bin_path):
            return bin_path
        old_path = cur_path
        cur_path = path.dirname(cur_path)
        if cur_path == old_path:
            break
    raise FileNotFoundError("Cannot find bazel-bin in parent folders")


def read_arch(bazel_bin, target, name):
    suffix = "-2.params"
    if path.exists(f"{bazel_bin}/{target}/{name}_spine-2.params"):
        suffix = "_spine-2.params"  # for C++ agents
    with open(f"{bazel_bin}/{target}/{name}{suffix}", "r") as params:
        for line in params:
            if line.startswith("bazel-out"):
                return line.split("/")[1]


def main(argv=None):
    workspace_name = "gupil"

    if len(sys.argv) < 2 or (len(sys.argv) >= 3 and sys.argv[2] != "--"):
        this = sys.argv[0]
        print(f"Usage: {this} //label/for:target [-- [target arguments]]")
        sys.exit(0)

    try:
        target, name = sys.argv[2].split(":")
    except ValueError:
        print(f"{sys.argv[1]} does not appear to be a valid Bazel label")
        sys.exit(-2)
    target = target.lstrip("/")
    if target[0] == "@":
        external_name, target = target[1:].split("//")
        target = f"external/{external_name}/{target}"
    bazel_bin = find_bazel_bin_directory()

    try:
        arch = read_arch(bazel_bin, target, name)
    except FileNotFoundError:
        print(Fore.YELLOW + "WARNING: " + Fore.RESET, end="")
        print(f"Couldn't read arch from {bazel_bin}/{target}/{name}-2.params")
        print("Maybe the target is not a Python script?")
        arch = "unknown"

    execution_path = (
        f"{bazel_bin}/{target}/{name}.runfiles/{workspace_name}/{target}"
    )

    if "-cd" in sys.argv:  # our little secret!
        print(execution_path)  # Usage: cd $(raspunzel //label/for:target)
        sys.exit(0)

    os.chdir(execution_path)
    print(f"{Fore.GREEN}INFO: {Fore.RESET}", end="")
    print(f"Found target {Fore.YELLOW}{name}{Fore.RESET} ", end="")
    print("for build configuration ", end="")
    color = Fore.RED
    if "opt" in arch:
        color = Fore.GREEN
    elif "fastbuild" in arch:
        color = Fore.YELLOW
    elif "unknown" in arch:
        color = Fore.RED
    print(color + arch + Fore.RESET)
    os.execv(name, [name] + sys.argv[3:])
