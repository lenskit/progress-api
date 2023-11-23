Progress API
============

.. py:module:: progress_api

There is one function and one class of primray interest to libraries using the
progress API: :py:func:`make_progress` and its return class, :py:class:`Progress`.

Creating Progress Bars
----------------------

.. autofunction:: make_progress

Progress Bar Interface
----------------------

.. autoclass:: Progress

.. _states:

Multiple States
---------------

The progress API supports multiple *states* and *outcomes* in progress reports
(an outcome is just a state that represents one of the various ways a task
can be finished, such as success or error).  :py:func:`make_progress` has two
parameters to provide the state configuration for a progress bar.  They interact
as follows:

*   If both ``states`` and ``outcomes`` are provided, then ``ouctomes`` is a
    list of final task states (succeeded, failed, etc.), and ``states`` is a
    list of *non-final* states an item may pass through on its way to a final
    state.  States should usually be specified in reverse order, so items
    typically pass from the last state to the first (e.g. connecting, loading,
    parsing, etc.), and finally to an outcome, although this is not enforced
    (the progress API does not track individual items, only the current count in
    each state).  When all items are completed, the total across the outcomes
    should equal the total number of items.

*   If only ``outcomes`` is specified, then they are a list of final task states,
    and no non-final states are reported.

*   If only ``states`` is specified, then the **first** state is considered the
    final state, and other states are intermediate in-progress states.

*   If neither ``states`` nor ``outcomes`` is specified, the progress bar is
    configured with a single final state ``'finished'``.

State names usually aren't displayed, but they can be logged by backends, and
configurable backends will use them to determine colors or other visuals. Backends
that only support a single state should report the sum of all final states as their
completed item count.

It is not recommended to include an initial state; the initial state can
be modeled by the fraction of the total that has not yet been added to any
state.

For an example, if you want to track final states ``loaded`` and ``failed``,
with intermediate states ``connecting`` and ``loading``, you would call
:py:func:`make_progress` as follows::

    p = make_progress(
        total,
        outcomes=["loaded", "failed"],
        states=["loading", "connecting"]
    )

For a single outcome with intermediate states, you can do::

    p = make_progress(
        total,
        states=["finished", "in-progress", "queued"]
    )
