AvaShell
###########################################

A desktop app that launches a Python script when started and then stays in system tray.
Might be useful if you need to keep running a script in the background. E.g. web crawler.

Checkout Source Codes
==============================

.. code-block:: bash

    git clone https://github.com/sampot/avashell.git
    cd avashell
    git submodule init
    git submodule update

Make the Distribution Package
===================================

.. code-block:: bash

    python pyinst/pyinstaller.py avashell.spec --clean -y


Launch the Application
=================================

Windows
--------------------

Launch the application from command line.
.. code-block:: bash

    dist\avashell\avashell.exe

OS X
--------------------

Launch from the console
.. code-block:: bash

    ./dist/avashell/avashell

or run the app bundle:

.. code-block:: bash
    open dist/Avashell.app

Ubuntu
--------------

Launch from the console
.. code-block:: bash

    ./dist/avashell/avashell



License
-------------

Source codes are released under the new BSD license.

Note that the icons are copyrighted by EAvatar Technology Ltd.
