TouhouS Documentation
=====================

Intro
-----

TouhouS is a shmup game engine written in Python 3 and Pyglet.

Dependencies
^^^^^^^^^^^^

Required
""""""""

* Python 3
* Pyglet 1.2alpha1

.. note::

    Pyglet 1.2alpha1 has a bug where the entire screen is shifted down halfway.
    Use the latest mercurial build instead.

Optional
""""""""

* Cython 0.17.4 for building extensions
* Sphinx 1.1.3 for generating documentation

Building
--------

Build and install `touhouS` as you would any Python package.

Building Cython extensions
^^^^^^^^^^^^^^^^^^^^^^^^^^

I've made a modification to `setup.py` for Cython compilation.  Simply run
`python setup.py c` instead of `python setup.py` and it will use Cython's
`build_ext` to compile the extensions.  Make sure you have Cython installed if
you do this.

Generating documentation
^^^^^^^^^^^^^^^^^^^^^^^^

If for some reason you would like to generate this documentation yourself, make
sure Sphinx is installed, `cd` into `doc`, and run `make html`.
