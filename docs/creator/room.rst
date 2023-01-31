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

At the very least, a room *must* contain a :ref:`room-description`.

.. _room-description:

description
^^^^^^^^^^^

+--------------+-------------------+--------------+
| Type: string | Required: **yes** | Format: none |
+--------------+-------------------+--------------+
| Example:                                        |
|                                                 |
| .. code-block:: yaml                            |
|                                                 |
|     description: You're on the sidewalk.        |
+-------------------------------------------------+

This attribute *must* be a multiline or one-line string of any size describing the room and its content.

It is shown when the player enters a room, and when the player invokes the :ref:`action-look` action, just after
:ref:`room-name` (if set) or otherwise just after the room's :ref:`reference <world-rooms>`.

.. _room-name:

name
^^^^

+--------------+--------------+--------------+
| Type: string | Required: no | Format: none |
+--------------+--------------+--------------+
| Example:                                   |
|                                            |
| .. code-block:: yaml                       |
|                                            |
|     name: Building hall                    |
+--------------------------------------------+

This attribute *should* be a one-line string and *should* be a few words long.

A room's display name is, by default, its associated :ref:`reference <world-rooms>`. This behavior *may* be overridden by
this attribute. If set, its value will be used everywhere the room's display name must be shown. It is shown when the
player enters a room, and when the player invokes the :ref:`action-look` action.

.. _room-items:

items
^^^^^

+-------------+--------------+-----------------------------------+
| Type: array | Required: no | Format: array of items references |
+-------------+--------------+-----------------------------------+
| Example:                                                       |
|                                                                |
| .. code-block:: yaml                                           |
|                                                                |
|     items: [security card, book]                               |
+----------------------------------------------------------------+

The list of :ref:`world-items` available for pickup in the room.

It is shown when the player enters a room, and when the player invokes the :ref:`action-look` action, just after
:ref:`room-description`.

.. _room-exits:

exits
^^^^^

+---------------+--------------+----------------------------+
| Type: mapping | Required: no | Format: string => ``exit`` |
+---------------+--------------+----------------------------+
| Example:                                                  |
|                                                           |
| .. code-block:: yaml                                      |
|                                                           |
|     exits:                                                |
|         back: Sidewalk                                    |
|         pursue: Down the street                           |
+-----------------------------------------------------------+

.. todo::

    Document.

Exit types
----------

.. todo::

    Document.
