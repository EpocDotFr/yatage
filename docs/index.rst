YATAGE documentation
====================

Welcome! This documentation is about YATAGE, Yet Another `Text Adventure Game <https://en.wikipedia.org/wiki/Interactive_fiction>`__ Engine.

|pyversion| |pypiv| |tests| |pypil|

Text adventure games have been around for a lot of decades now, created back in an age when computer graphics were reduced
to their simplest form: alphanumeric characters and symbols.

This simplicity in displaying a game's UI using these last has something fascinating: it is easy to both create and play
such game type. You don't have to worry about **a ton** of things, compared to a 3D or even a 2D game.

You still have to worry about creating a game engine, though. A relatively simple and small one, but a game engine anyway.

YATAGE has been created to not worry about this step, reducing text adventure game development effort to one thing: writing
as less characters and symbols as possible in one file, in a structured fashion (`YAML <https://en.wikipedia.org/wiki/YAML>`__),
to create a playable game.

Example
-------

Here is a short example, which uses a small subset of the game engine's capabilities:

.. literalinclude:: ../examples/short.yml
    :language: yaml

:download:`Download <../examples/short.yml>` and :doc:`run <player/run>` this example after :ref:`installing <Installation>` YATAGE.

Prerequisites
-------------

  - Python >= 3.8

Installation
------------

From PyPI:

.. code-block:: console

    $ pip install yatage

Locally, after cloning/downloading the repo:

.. code-block:: console

    $ pip install .

Guide
-----

.. toctree::
   :caption: Player's Guide
   :maxdepth: 4

   player/run
   player/play

.. toctree::
   :caption: Creator's Guide
   :maxdepth: 4

   creator/world
   creator/room
   creator/item

Credits
-------

  - Logo by `Delapouite <https://game-icons.net/1x1/delapouite/dungeon-gate.html>`__ (`CC BY 3.0 <https://creativecommons.org/licenses/by/3.0/>`__)

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/yatage.svg
.. |pypiv| image:: https://img.shields.io/pypi/v/yatage.svg
.. |tests| image:: https://github.com/EpocDotFr/yatage/actions/workflows/tests.yml/badge.svg
.. |pypil| image:: https://img.shields.io/pypi/l/yatage.svg
