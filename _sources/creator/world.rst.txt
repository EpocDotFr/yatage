World file
==========

YATAGE needs a world file in order to be able to run a game: it is a plaintext `YAML <https://en.wikipedia.org/wiki/YAML>`__-formatted
file (``*.yml``) which is itself structured in a specific fashion.

This file contains everything that is needed in order to create a text adventure game, namely:

  - :doc:`Rooms <room>`, which defines the physical dimension of the world;
  - :doc:`Items <item>`, which defines objects that can be found along the way.

The following section details how this file *must* be structured, following the YAML format.

.. _world-structure:

World structure
---------------

At the very least, the world file *must* contain:

  - A :ref:`world-version`
  - A :ref:`world-name`
  - A starting room (:ref:`world-start`)
  - At least one well-formed room in :ref:`world-rooms` referenced by :ref:`world-start` above

.. _world-version:

version
^^^^^^^

  - Type: integer
  - Required: **yes**
  - Allowed values: ``1``

Although not used yet (at least in the earliest releases of YATAGE), this attribute tells which version the world file
has been written in.

It will allow to handle future -- inevitable -- breaking changes of the world file's structure.

.. _world-name:

name
^^^^

  - Type: string
  - Required: **yes**
  - Format: none

This attribute *should* be a one-line string and *should* be a few words long. It *may* be your world's name, your hero's
name, your game's name, etc.

It is shown emphasized when running a game at the very beginning.

.. _world-start:

start
^^^^^

  - Type: string
  - Required: **yes**
  - Format: room reference

This attribute is a reference to the starting room of the game, in other words the room where the player will start
playing.

See also :ref:`world-rooms`.

.. _world-rooms:

rooms
^^^^^

  - Type: mapping
  - Required: **yes**
  - Format: string => :ref:`room <room-structure>`
  - Minimum count: 1

This attribute holds all the world's rooms definition. It is a mapping between rooms references (a string) and a
:ref:`room <room-structure>` structure.

References *must* obviously be unique. References are used as the in-game rooms name unless the rooms's :ref:`room-name`
has been set. At least one well-formed room *must* be defined and referenced by :ref:`world-start`.

See also :doc:`room`.

.. _world-description:

description
^^^^^^^^^^^

  - Type: string
  - Required: no
  - Format: none

This attribute *may* be a multiline string of any size describing this world, which *may* be used as an introduction to
the game.

It is shown when running a game at the very beginning, just after :ref:`world-author` (if set) or otherwise just after
:ref:`world-name`.

.. _world-author:

author
^^^^^^

  - Type: string
  - Required: no
  - Format: none

This attribute *should* be a single-line string containing any information about the author(s) of this world.

It is shown when running a game at the very beginning, just after :ref:`world-name` and before :ref:`world-description`
(if set).

.. _world-items:

items
^^^^^

  - Type: mapping
  - Required: no
  - Format: string => :ref:`item <item-structure>`

This attribute holds all the world's items definition. It is a mapping between items references (a string) and an
:ref:`item <item-structure>` structure.

References *must* obviously be unique. References are used as the in-game items name unless the item's ``alias`` has
been set. References *should* preferably be lowercase.

See also :doc:`item`.