Open Energy Efficiency Meter
============================

***WARNING: The repository location for the Open EE Meter calculation has moved:***

Please go to https://github.com/impactlab/eemeter for the newest version

This repository is no longer updated.

Documentation
-------------

Docs on [RTD](http://eemeter.readthedocs.org/en/latest/).

Installation
------------

Execute the following command to install:

    $ pip install git+git://github.com/impactlab/eemeter.git#egg=ee-meter

Testing
-------

This library uses the py.test framework. To develop locally, clone the repo,
and in a virtual environment execute the following commands:

    $ git clone https://github.com/impactlab/eemeter
    $ cd eemeter
    $ pip install numpy scipy pytest
    $ python setup.py develop
    $ py.test

You should ensure that you are using the virtualenv py.test executable with
`py.test --version`.

Some tests are slow and are skipped by default; to run these, use the `--runslow` flag:

    $ py.test --runslow

Licence
-------

MIT
