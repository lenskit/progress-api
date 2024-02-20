# This file is from Enlighten, distributed with Progress API.
# Licensed under the Mozilla Public License, see LICENSE for details.
# SPDX-License-Identifier: MPL

# Copyright 2017 - 2023 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Simple progress bar example
"""

import time

from progress_api import make_progress


def process_files():
    """
    Process files with a single progress bar
    """

    with make_progress(total=100, label="Simple", unit="ticks") as pbar:
        for _ in range(100):
            time.sleep(0.05)
            pbar.update()


if __name__ == "__main__":
    process_files()
