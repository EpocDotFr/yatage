Room
====

Rooms defines the physical dimension of the world. The player moves between rooms to advance throughout the game.

Rooms *may* define:

  - **Exits**, which are different ways to leave the room;
  - Instances of :doc:`items <item>`, which can be taken then interacted with by the player.

The following section details how a room *must* be structured, following the YAML format.

.. _room-structure:

Room structure
--------------

At the very least, a room *must* contain:

  - A :ref:`room-description`

.. _room-description:

description
^^^^^^^^^^^

  - Type: string
  - Required: **yes**
  - Format: none

This attribute *must* be a multiline or one-line string of any size describing the room and its content.

It is shown when the player enters a room, and when the player invokes the :ref:`action-look` action, just after
:ref:`room-name` (if set) or otherwise just after the room's :ref:`reference <world-rooms>`.

.. _room-name:

name
^^^^

  - Type: string
  - Required: no
  - Format: none

This attribute *should* be a one-line string and *should* be a few words long.

A room's display name is, by default, its associated :ref:`reference <world-rooms>`. This behavior *may* be overridden by
this attribute. If set, its value will be used everywhere the room's display name must be shown.

.. _room-items:

items
^^^^^

  - Type: array
  - Required: no
  - Format: array of items references

.. todo::

    Document.

.. _room-exits:

exits
^^^^^

  - Type: mapping
  - Required: no
  - Format: string => ``exit``

.. todo::

    Document.

Exit types
----------

.. todo::

    Document.
