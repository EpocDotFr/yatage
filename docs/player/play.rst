Playing a game
==============

Now that you're able to :doc:`run a game <run>` using a valid YATAGE world file, it can be played.

When starting a game, you will be first shown various information about the world being played on (you can show it
again later anytime using the :ref:`action-intro` action).

.. note::

    Extra information may be shown if debug mode is enabled (see :ref:`Debug mode`).

The game itself then begins.

Actions
-------

YATAGE implements the typical game loop of text adventure games (we'll not get into details here), it thus excepts you
to type the action to perform next.

General
^^^^^^^

.. _action-look:

``look``
  Examine the current room.

.. _action-intro:

``intro``
  Show the introductory text that is displayed when starting the game.

.. _action-exit:

``exit``
  Exit the game.

.. _action-go:

``go <exit>`` or merely ``<exit>``
  Travel to the direction ``<exit>``.

  Examples: ``go entrance`` or ``entrance``

.. _action-inv:

``inventory`` or ``inv``
  List items currently in inventory.

.. _action-help:

``help``
  Show help about all available actions.

.. _action-help-action:

``help <action>``
  Show help about the specific action ``<action>``.

  Example: ``help drop``

Items
^^^^^

.. _action-look-item:

``look <item>``
  Examine item ``<item>``. May be either an item in the current room or in the inventory.

  Example: ``look security card``

.. _action-take:

``take <item>``
  Take item ``<item>`` from the current room and put it into the inventory.

  Example: ``take security card``

.. _action-take-all:

``take all``
  Take all items from the current room and put them into the inventory.

.. _action-drop:

``drop <item>``
  Remove the item ``<item>`` from the inventory and drop it into the current room.

  Example: ``drop security card``

.. _action-drop-all:

``drop all``
  Remove all items from the inventory and drop them into the current room.

.. _action-use:

``use <item>``
  Activate or apply item ``<item>``. Item must be present in inventory.

  Example: ``use security card``

.. _actions-debug:

Debug
^^^^^

Those are available if debug mode is enabled (see :ref:`Debug mode`).

.. _action-spawn:

``spawn <item>``
  Spawn a new item identified by ``<item>`` into the inventory.

  Example: ``spawn security card``

.. _action-destroy:

``destroy <item>``
  Destroy item identified by ``<item>`` in the inventory.

  Example: ``destroy security card``

.. _action-destroy-all:

``destroy all``
  Destroy all items in the inventory.

.. _action-tp:

``tp <room>``
  Teleport the player to the room identified by ``<room>``.

  Example: ``tp Building hall``

Good luck! Remember you can :ref:`exit the game <Exiting the game>` anytime.

You're now ready to :doc:`create your own games <../creator/world>`!