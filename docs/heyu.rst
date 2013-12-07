**********
Heyu Notes
**********

Installation
============

Download latest tarball;
e.g. :command:`curl -O http://www.heyu.org/download/heyu-2.11-rc1.tar.gz`.

Extract the tarball,
build,
and install :program:`heyu`:

.. code-block:: bash

    $ tar xvzf heyu-2.11-rc1.tar.gz
    $ cd heyu-2.11-rc1
    $ sh ./Configure.sh
    $ make
    $ sudo make install

When the install script asks,
select the choice to put the sample configuruation file in :file:`/home/pi/.heyu/`,
and use :kbd:`dummy` for CM11 TTY port unless the USB serial adapter is connected,
in which case,
use its device path
(probably :file:`/dev/ttyUSB0`).
