# This file is from Enlighten, distributed with Progress API.
# Licensed under the Mozilla Public License, see LICENSE for details.
# SPDX-License-Identifier: MPL


# Copyright 2019 - 2021 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Demo of Enlighten's features
"""

import os
import platform
import random
import sys
import time

from progress_api import make_progress
from progress_api.backends.enlighten import EnlightenProgressBackend
from progress_api.config import set_backend

# Hack so imports work regardless of how this gets called
# We do it this way so any enlighten path can be used
sys.path.insert(1, os.path.dirname(__file__))

# pylint: disable=wrong-import-order,import-error,wrong-import-position
from multicolored import load, run_tests  # noqa: E402
from multiple_logging import process_files, win_time_granularity  # noqa: E402
from prefixes import download  # noqa: E402


def initialize(initials=15):
    """
    Simple progress bar example
    """

    # Simulated preparation
    pbar = make_progress(total=initials, label="Initializing:", unit="initials", leave=True)
    for _ in range(initials):
        time.sleep(random.uniform(0.05, 0.25))  # Random processing time
        pbar.update()
    pbar.finish()


def main():
    """
    Main function
    """

    # status = manager.status_bar(
    #     status_format="Enlighten{fill}Stage: {demo}{fill}{elapsed}",
    #     color="bold_underline_bright_white_on_lightslategray",
    #     justify=enlighten.Justify.CENTER,
    #     demo="Initializing",
    #     autorefresh=True,
    #     min_delta=0.5,
    # )
    # docs = manager.term.link(
    #     "https://python-enlighten.readthedocs.io/en/stable/examples.html", "Read the Docs"
    # )
    # manager.status_bar(
    #     " More examples on %s! " % docs, position=1, fill="-", justify=enlighten.Justify.CENTER
    # )

    initialize(15)
    # status.update(demo="Loading")
    load(40)
    # status.update(demo="Testing")
    run_tests(20)
    # status.update(demo="Downloading")
    download(2.0 * 2**20)
    # status.update(demo="File Processing")
    process_files()


if __name__ == "__main__":
    if os.environ.get("PROGRESS_BACKEND", None) == "enlighten":
        set_backend(
            EnlightenProgressBackend(
                state_colors={
                    "loaded": "green",
                    "loading": "yellow",
                    "connecting": "blue",
                    "downloaded": "purple",
                    "passed": "green",
                    "failed": "red",
                    "errored": "yellow",
                }
            )
        )

    if platform.system() == "Windows":
        with win_time_granularity(1):
            main()
    else:
        main()
