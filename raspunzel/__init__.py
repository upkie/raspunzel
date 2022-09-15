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
Deploy and run Bazel targets on a Raspberry Pi.
"""

import argparse
import os
import sys

from .build import build
from .run import run
from .spdlog import logging
from .sync import sync
from .workspace import Workspace

__version__ = "0.2.0"


def get_argument_parser() -> argparse.ArgumentParser:
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
    subparsers = parser.add_subparsers(title="subcommands", dest="subcmd")

    # build -------------------------------------------------------------------
    parser_build = subparsers.add_parser(
        "build",
        help="build Bazel targets listed in a project file",
    )
    parser_build.add_argument("target", help="Bazel target")
    parser_build.add_argument(
        "subargs",
        nargs=argparse.REMAINDER,
        help="arguments forwarded to the target",
    )

    # run ---------------------------------------------------------------------
    parser_run = subparsers.add_parser(
        "run",
        help="run a Bazel target",
    )
    parser_run.add_argument("target", help="Bazel target")
    parser_run.add_argument(
        "subargs",
        nargs=argparse.REMAINDER,
        help="arguments forwarded to the target",
    )

    # sync --------------------------------------------------------------------
    parser_sync = subparsers.add_parser(
        "sync",
        help="sync Bazel workspace with the remote host",
    )
    parser_sync.add_argument(
        "destination",
        help="destination in rsync+ssh format [user@]host:path",
    )

    return parser


def main(argv=None):
    parser = get_argument_parser()
    args = parser.parse_args(argv)
    if args.subcmd is None:
        parser.print_help()
        sys.exit(-1)
    if args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    if args.sudo and os.geteuid() != 0:
        args = ["sudo", "-E", sys.executable] + sys.argv + [os.environ]
        os.execlpe("sudo", *args)

    if args.subcmd == "build":
        build(args.target, args.subargs)
    elif args.subcmd == "run":
        run(Workspace(), args.target, args.subargs)
    elif args.subcmd == "sync":
        sync(Workspace(), args.destination)
