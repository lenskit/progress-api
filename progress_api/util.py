"""
Utility functions for implementing progress backends.
"""


def format_metric(label: str, value: int | str | float | None, fmt: str | None = None):
    """
    Helper method to format meters.
    """
    if fmt is None:
        vf = str(value)
    else:
        vf = fmt.format(value)

    return f"{label} {vf}"
