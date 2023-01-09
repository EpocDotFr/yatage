Running a game
==============

The ``yatage`` executable is automatically made available when YATAGE is installed. This is the executable that must be
used in order to run games.

Basic usage
-----------

The most basic use of ``yatage`` is:

.. code-block:: console

    $ yatage {WORLD FILE}

Where ``{WORLD FILE}`` is the path to a YATAGE world file (``*.yml``).

A bunch of validation steps will be performed on the given file before being actually used to make sure it is a well-formed
world file .

Exiting the game
^^^^^^^^^^^^^^^^

You can exit the game anytime using either :kbd:`Control-d` or :kbd:`Control-c`.

Note you will lose your progress as YATAGE does not allow to save game state (yet).

Advanced usage
--------------

More advanced stuff is needed in some specific use cases.

Debug mode
^^^^^^^^^^

Sometimes, you will need debug information about what's happening, or perform actions that would never be possible while
playing normally, for example while creating a game. Use the ``--debug`` flag:

.. code-block:: console

    $ yatage {WORLD FILE} --debug

This will add the following debug statements in-game:

  - World file version, number of rooms and number of items will be displayed before world's description
  - Rooms identifier will be displayed next to all rooms names
  - Details will be displayed next to the exits' name (exit type, conditions, rooms identifiers / names, etc)

In addition, the following new actions are made available (for debug purposes only!):

  - ``spawn <item>``: spawn a new item identified by ``<item>`` into the player's inventory
  - ``tp <room>``: teleport the player to the room identified by ``<room>``

Finally, debug mode will alter some of the game engine's behavior:

  - Used items will not be hidden in inventory. A ``[used]`` suffix will instead be appended to the items' name

Automate actions
^^^^^^^^^^^^^^^^

Sometimes, you will be tired of typing every single action that needs to be made in order to get to a given progress
in-game, for example while creating a game. Fortunately, there's the ``--actions`` option:

.. code-block:: console

    $ yatage {WORLD FILE} --actions {ACTIONS FILE}

Where ``{ACTIONS FILE}`` is the path to a plain text file (usually ``*.txt``) which contains the actions to be
automatically executed, in order, starting from the top.

The file should contain one action per line:

.. literalinclude:: ../../examples/short_actions.txt
    :language: text

If debug mode is enabled, debug actions are made available too (see above).