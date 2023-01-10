YATAGE documentation
====================

Welcome! This documentation is about YATAGE, Yet Another `Text Adventure Game <https://en.wikipedia.org/wiki/Interactive_fiction>`__ Engine.

|pyversion| |pypiv| |pypil|

Text adventure games have been around for a lot of decades now, created back in an age when computer graphics were reduced
to their simplest form: alphanumeric characters and symbols.

This simplicity in displaying a game's UI using these last has something fascinating: it is easy to both create and play
such game type. You don't have to worry about **a ton** of things, compared to a 3D or even a 2D game.

You still have to worry about creating a game engine, though. A relatively simple and small one, but a game engine anyway.

YATAGE has been created to not worry about this step, reducing text adventure game development effort to one thing: writing
as less characters and symbols as possible in one file, in a structured fashion (`YAML <https://en.wikipedia.org/wiki/YAML>`__),
to create a playable game.

Here's a short example, which uses a small subset of the game engine's capabilities:

.. literalinclude:: ../examples/short.yml
    :language: yaml

Features
--------

.. todo::

    Document.

Prerequisites
-------------

  - Python 3.8

Installation
------------

From PyPI:

.. code-block:: console

    $ pip install yatage

Locally, after cloning/downloading the repo:

.. code-block:: console

    $ pip install .

Player's Guide
--------------

Guide about running and playing games.

.. toctree::
   :maxdepth: 4

   player/run
   player/play

Creator's Guide
---------------

Guide about creating games.

.. toctree::
   :maxdepth: 4

   creator/world
   creator/rooms
   creator/items

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/yatage.svg
.. |pypiv| image:: https://img.shields.io/pypi/v/yatage.svg
.. |pypil| image:: https://img.shields.io/pypi/l/yatage.svg
