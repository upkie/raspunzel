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

"""Deploy and run Bazel targets on a Raspberry Pi."""

import argparse
import logging
import os
import sys

from .run import run
from .workspace import Workspace

__version__ = "1.0.0"


def get_argument_parser() -> argparse.ArgumentParser:
    """Get command-line argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-s",
        "--sudo",
        default=False,
        action="store_true",
        help="run as administrator (sudo -E)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="verbose mode",
    )
    parser.add_argument("command", help="Bazel command")
    parser.add_argument("target", help="Bazel target")
    parser.add_argument(
        "subargs",
        nargs=argparse.REMAINDER,
        help="arguments forwarded to the target",
    )
    return parser


def main(argv=None):
    """Entry point for the command-line tool."""
    parser = get_argument_parser()
    args = parser.parse_args(argv)
    if args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    if args.sudo and os.geteuid() != 0:
        args = ["sudo", "-E", sys.executable] + sys.argv + [os.environ]
        os.execlpe("sudo", *args)
    if args.command == "run":
        run(Workspace(), args.target, args.subargs)
    else:  # unknown command
        logging.error(f'Command "{args.command}" not available with raspunzel')
