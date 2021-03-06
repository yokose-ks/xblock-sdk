XBlock SDK |build-status| |coverage-status|
===========================================

This repository consists of three main components to assist in the creation of new XBlocks:

    * a template-based generator for new XBlocks (found in `prototype`)
    * sample XBlocks that can be the basis for new XBlock work (found in `sample_xblocks`)
    * Workbench runtime, a simple runtime for viewing and testing XBlocks in a browser (found in `workbench`)


Installation
------------

This code runs on Python 2.7. If you prefer to use Python 3, there is `a fork
of xblock-sdk that provides Python 3 support`_, but this fork is not yet
supported by edX.

1.  Get a local copy of this repo.

2.  (Optional)  Create and activate a virtualenv to work in.

3.  Install the requirements and register the XBlock entry points with (you may
    need to sudo this if you don't use virtualenv):

        $ make install

4. Create and sync the sqllite DB

        $ python manage.py syncdb

4.  Run the Django development server:

        $ python manage.py runserver

5.  Open a web browser to: http://127.0.0.1:8000

.. _a fork of xblock-sdk that provides Python 3 support: https://github.com/singingwolfboy/xblock-sdk/tree/py3

Testing
--------

To install all requirements and run the test suite:

    $ make

This will run:

    * Integration tests of XBlocks running within the workbench.
    * Individual tests written for the demo XBlocks

You can test XBlocks through a browser using `Selenium`_. We have included an
example Selenium test for ``thumbs`` that uses Django's `LiveServerTestCase`_.
It runs as part of the test suite as executed by the above command. You need to
have Firefox installed for this test case to run successfully.

.. _Selenium: http://docs.seleniumhq.org/
.. _LiveServerTestCase: https://docs.djangoproject.com/en/1.4/topics/testing/#django.test.LiveServerTestCase

To run the test suite under coverage:

    $ coverage run manage.py test

to execute the tests. Then to view the coverage report:

    $ coverage report

See the `coverage.py`_ docs for more info and options.

.. _coverage.py: http://nedbatchelder.com/code/coverage/

Using the workbench
-------------------

When you open the workbench, you'll see a list of sample XBlock configurations
(scenarios).  Each will display a page showing the XBlocks composited together,
along with internal information like the "database" contents.

The workbench doesn't use a real database, it simply stores all data in an
in-memory dictionary.  The data is all lost and reset when you restart the
server.

If you want to experiment with different students, you can use a URL parameter
to set the student ID, which defaults to 1:

    http://127.0.0.1:8000/?student_id=17

Different students will see different student state, for example, while seeing
the same content.  Student ids are strings, even if they contain only digits
as the default does.


Making your own XBlock
----------------------

Making an XBlock can be as simple as creating a Python class with a few
specific methods.  The ``thumbs`` XBlock demonstrates an XBlock with state,
views, and input handling.

We provide a script to create a new XBlock project to help you get started.
Run script/startnew.py in a directory where you want to create your XBlock
project.  startnew.py will prompt you for the name of the XBlock, and will
create a minimal working XBlock, ready for you to begin development.

You can provide scenarios for the workbench to display, see the thumbs.py
sample for an example, or the xblock/problem.py file.  The scenarios are
written in a simple XML language.  Note this is not an XML format we are
proposing as a standard.

Once you install your XBlock into your virtualenv, the workbench will
automatically display its scenarios for you to experiment with.


External XBlocks
----------------

We have been moving towards hosting XBlocks in external repositories, some of
which have been installed and will appear in the workbench:

ACID XBlock: https://github.com/edx/acid-block


License
-------

The code in this repository is licensed under version 3 of the AGPL unless
otherwise noted.

Please see ``LICENSE.txt`` for details.


How to Contribute
-----------------

Contributions are very welcome. The easiest way is to fork this repo, and then
make a pull request from your fork. The first time you make a pull request, you
may be asked to sign a Contributor Agreement.


Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org


Mailing List and IRC Channel
----------------------------

You can discuss this code on the `edx-code Google Group`__ or in the
``#edx-code`` IRC channel on Freenode.

__ https://groups.google.com/group/edx-code

.. |build-status| image:: https://travis-ci.org/edx/xblock-sdk.svg?branch=master
   :target: https://travis-ci.org/edx/xblock-sdk
.. |coverage-status| image:: https://coveralls.io/repos/edx/xblock-sdk/badge.png
   :target: https://coveralls.io/r/edx/xblock-sdk
