# This file is from Enlighten, distributed with Progress API.
# Licensed under the Mozilla Public License, see LICENSE for details.
# SPDX-License-Identifier: MPL

# Copyright 2017 - 2020 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Multiple progress bars example
"""

import logging
import platform
import random
import time
from contextlib import contextmanager

from progress_api.api import make_progress

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("enlighten")

DATACENTERS = 5
SYSTEMS = (5, 10)  # Range
FILES = (10, 100)  # Range


@contextmanager
def win_time_granularity(milliseconds):
    """
    time.sleep() on Windows may not have high precision with older versions of Python
    This will temporarily change the timing resolution


    # https://docs.microsoft.com/en-us/windows/desktop/api/timeapi/nf-timeapi-timebeginperiod
    """

    from ctypes import windll  # pylint: disable=import-outside-toplevel

    try:
        windll.winmm.timeBeginPeriod(milliseconds)
        yield
    finally:
        windll.winmm.timeEndPeriod(milliseconds)


def process_files():
    """
    Process a random number of files on a random number of systems across multiple data centers
    """

    # Get a top level progress bar
    enterprise = make_progress(
        total=DATACENTERS, label="Processing:", unit="datacenters", leave=True
    )

    # Iterate through data centers
    for d_num in range(1, DATACENTERS + 1):
        systems = random.randint(*SYSTEMS)  # Random number of systems
        # Get a child progress bar. leave is False so it can be replaced
        datacenter = make_progress(
            total=systems, label="  Datacenter %d:" % d_num, unit="systems", leave=False
        )

        # Iterate through systems
        for s_num in range(1, systems + 1):
            # Has no total, so will act as counter. Leave is False
            system = make_progress(label="    System %d:" % s_num, unit="files", leave=False)
            files = random.randint(*FILES)  # Random file count

            # Iterate through files
            for _ in range(files):
                system.update()  # Update count
                time.sleep(random.uniform(0.001, 0.005))  # Random processing time

            system.finish()  # Close counter so it gets removed
            # Log status
            LOGGER.info("Updated %d files on System %d in Datacenter %d", files, s_num, d_num)
            datacenter.update()  # Update count

        datacenter.finish()  # Close counter so it gets removed

        enterprise.update()  # Update count

    enterprise.finish()  # Close counter, won't be removed but does a refresh


def main():
    """
    Main function
    """

    process_files()


if __name__ == "__main__":
    if platform.system() == "Windows":
        with win_time_granularity(1):
            main()
    else:
        main()
