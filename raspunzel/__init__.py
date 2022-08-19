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
import logging
import sys

from .bazel import Workspace
from .run import run
from .sync import sync

__version__ = "0.2.0-pre"


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help=(
            "Verbose mode. "
            "Causes raspunzel to print messages about its progress."
        ),
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="subcmd")

    # raspunzel run -----------------------------------------------------------
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

    # raspunzel sync ----------------------------------------------------------
    parser_sync = subparsers.add_parser(
        "sync",
        help="Sync Bazel workspace with the remote host",
    )
    parser_sync.add_argument(
        "destination",
        help="Destination in rsync+ssh format [user@]host:path",
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

    workspace = Workspace()

    if args.subcmd == "run":
        run(workspace, args.target, args.subargs)
    elif args.subcmd == "sync":
        sync(workspace, args.destination)
