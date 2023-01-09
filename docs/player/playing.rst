Playing a game
==============

Now that you're able to :doc:`run a game <running>` using a valid YATAGE world file, it can be played.

When running a game, you will be shown various information about the world being played on. Extra information may be
shown if debug mode is enabled (see :ref:`Debug mode`).

The game itself then begins.

Actions
-------

YATAGE implements the typical game loop of text adventure games (we'll not get into details here), it thus excepts you
to type the action to perform next.

The available actions are:

  - ``drop <item>`` -- Drop the item identified by ``<item>`` from the inventory on the current room's floor
  - ``go <exit>`` or merely ``<exit>`` -- Move to the direction ``<exit>``
  - ``help`` -- TODO

    - ``help <action>`` -- TODO
  - ``inv`` -- TODO
  - ``look`` -- TODO

    - ``look <subject>`` -- TODO
  - ``take <item>`` -- TODO
  - ``use <item>`` -- TODO
