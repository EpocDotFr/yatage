Creating world file
===================

YATAGE needs what we call a "world file" to be able to run a game: it's a plaintext `YAML <https://en.wikipedia.org/wiki/YAML>`__-formatted
file (``*.yml``) which is itself structured in a specific fashion.

Here's a kinda useless bare-minimum example world file:

.. literalinclude:: ../../examples/bare-minimum.yml
    :language: yaml

At the very least, the world file must have:

  - A :ref:`version`
  - A :ref:`name`
  - A starting room :ref:`start`
  - At least one room in :ref:`rooms` referenced by :ref:`start`

    - This sole room must have at least a ``description``

Continue reading below to learn about the details of the world file structure.

Structure
---------

``version``
^^^^^^^^^^^

  - Type: integer
  - Required: **yes**
  - Allowed values: ``1``

Although not used yet (at least in the earliest releases of YATAGE), this required attribute tells which version the
world file has been written in. It will allow to handle future -- inevitable -- breaking changes of the world file
structure.

``name``
^^^^^^^^

  - Type: string
  - Required: **yes**
  - Format: none

This attribute should be a one-line string and should be a few words long. It's shown emphasized when running a game at the
very beginning. It may be your world's name, your hero's name, your game's name, etc.

``start``
^^^^^^^^^

  - Type: string
  - Required: **yes**
  - Format: room reference

This attribute is a room reference to the starting room of the game, in other words the room where the player will start
playing. See also :ref:`rooms`.

``rooms``
^^^^^^^^^

  - Type: mapping
  - Required: **yes**

This attribute holds all the world's rooms definition. See :doc:`rooms` for full details.

``description``
^^^^^^^^^^^^^^^

  - Type: string
  - Required: no
  - Format: none

This attribute may be a multiline string of any size describing this world, which may be used as an introduction to the
game. It's shown when running a game at the very beginning, just after :ref:`author` (if set) or otherwise just after
:ref:`name`.

``author``
^^^^^^^^^^

  - Type: string
  - Required: no
  - Format: none

This attribute should be a one-line string containing any information about the author(s) of this world. It's shown when
running a game at the very beginning, just after :ref:`name` and before :ref:`description` (if set).

``items``
^^^^^^^^^

  - Type: mapping
  - Required: no

This attribute holds all the world's items definition. See :doc:`items` for full details.