Playing a game
==============

Now that you're able to :doc:`run a game <run>` using a valid YATAGE world file, it can be played.

When running a game, you will be first shown various information about the world being played on.

.. note::

    Extra information may be shown if debug mode is enabled (see :ref:`Debug mode`).

The game itself then begins.

Actions
-------

YATAGE implements the typical game loop of text adventure games (we'll not get into details here), it thus excepts you
to type the action to perform next.

The available actions are:

``drop <item>``
  Remove the item ``<item>`` from the inventory and drop it into the current room.

  Example: ``drop security card``

``go <exit>`` or merely ``<exit>``
  Travel to the direction ``<exit>``.

  Examples: ``go entrance`` or ``entrance``

``help``
  Show help about all available actions.

``help <action>``
  Show help about the specific action ``<action>``.

  Example: ``help drop``

``inv``
  List items currently in inventory.

``look``
  Examine the current room.

``look <item>``
  Examine item ``<item>``. May be either an item in the current room or in the inventory.

  Example: ``look security card``

``take <item>``
  Take item ``<item>`` from the current room and put it into the inventory.

  Example: ``take security card``

``use <item>``
  Activate or apply item ``<item>``. Item must be present in inventory.

  Example: ``use security card``

.. note::

    Additional actions are available if debug mode is enabled (see :ref:`Debug mode`).

Good luck! Remember you can :ref:`exit the game <Exiting the game>` anytime.

You're now ready to :doc:`create your own games <../creator/world>`!