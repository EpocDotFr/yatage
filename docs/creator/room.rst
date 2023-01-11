Room
====

Rooms defines the physical dimension of the world. The player moves between rooms to advance throughout the game.

Rooms *may* define:

  - **Exits**, which are different ways to leave the current room;
  - Instances of :doc:`items <item>`, which can be taken then interacted with by the player.

The following section details how a room *must* be structured, following the YAML format.

.. _room-structure:

Room structure
--------------

At the very least, a room must contain:

  - A :ref:`room-description`

.. _room-description:

description
^^^^^^^^^^^

  - Type: string
  - Required: **yes**
  - Format: none

.. todo::

    Document.

.. _room-name:

name
^^^^

  - Type: string
  - Required: no
  - Format: none

.. todo::

    Document.

items
^^^^^

  - Type: array
  - Required: no
  - Format: array of items references

.. todo::

    Document.