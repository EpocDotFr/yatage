Creating world file
===================

YATAGE needs what we call a "world file" to be able to run a game: it's a plaintext `YAML <https://en.wikipedia.org/wiki/YAML>`__-formatted
file (``*.yml``) which is itself structured in a specific fashion.

Here's a kinda useless bare-minimum example world file:

.. literalinclude:: ../../examples/bare-minimum.yml
    :language: yaml

At the very least, the world file must have:

  - A ``version``
  - A ``name``
  - A starting room ``start``
  - At least one room in ``rooms`` referenced by ``start`` above
    - The sole room must have at least a ``description``

Continue reading below to learn about this file's structure.

Structure
---------

``version``
^^^^^^^^^^^

  - Type: integer
  - Required: **yes**
  - Allowed values: ``1``

.. todo::

    Document.

``name``
^^^^^^^^^^^

  - Type: string
  - Required: **yes**

.. todo::

    Document.

``start``
^^^^^^^^^

  - Type: string
  - Required: **yes**

.. todo::

    Document.

``description``
^^^^^^^^^^^^^^^

  - Type: string
  - Required: no

.. todo::

    Document.

``author``
^^^^^^^^^^

  - Type: string
  - Required: no

.. todo::

    Document.
