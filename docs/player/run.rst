Running a game
==============

The ``yatage`` executable is automatically made available when YATAGE is :ref:`installed <installation>`. This is the
executable that must be used in order to run games.

Basic usage
-----------

The most basic use of ``yatage`` is:

.. code-block:: console

    $ yatage <world>

Where ``<world>`` is the path to a :doc:`YATAGE world file <../creator/world>`.

A bunch of validation steps will be performed on the given file before being actually used to make sure it is a well-formed
world file.

Exiting the game
^^^^^^^^^^^^^^^^

You can exit the game anytime using either :kbd:`Control-D`, :kbd:`Control-C`, or the :ref:`action-exit` action.

.. note::

    You will lose your progress as YATAGE does not allow to save game state (yet).

Advanced usage
--------------

More advanced stuff is needed in some specific use cases.

Debug mode
^^^^^^^^^^

Sometimes, you will need debug information about what's happening, or perform actions that would never be possible while
playing normally, for example while creating a game. Use the ``--debug`` flag:

.. code-block:: console

    $ yatage <world> --debug

This will add the following debug statements in-game:

  - Current YATAGE version
  - World file version, number of rooms and number of items will be displayed before world's description
  - Rooms identifier will be displayed next to all rooms names
  - Details will be displayed next to the exits' name (exit type, conditions, rooms identifiers / names, etc)

In addition, debug mode will alter some of the game engine's behavior:

  - Used items will not be hidden in inventory. A ``[used]`` suffix will instead be appended to the items' name

Finally, new :ref:`actions <actions-debug>` are made available.

Automating actions
^^^^^^^^^^^^^^^^^^

Sometimes, you will be tired of typing every single action that needs to be made in order to get to a given progress
in-game, for example while creating a game. Fortunately, there is the ``--actions`` option:

.. code-block:: console

    $ yatage <world> --actions <actions>

Where ``<actions>`` is the path to a plain text file (usually ``*.txt``) which contains the actions to be automatically
executed, in order, starting from the top.

The file should contain one action per line:

.. literalinclude:: ../../examples/short_actions.txt
    :language: text

.. note::

    If debug mode is enabled, debug actions are made available too (see :ref:`Debug mode`).

You can now continue to :doc:`play`.