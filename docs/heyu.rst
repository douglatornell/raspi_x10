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

Once the USB serial adapter is connected to the Raspberry Pi and the CM11 change the :kbd:`TTY` directive in :file:`/home/pi/.heyu/x10config` to :kbd:`/dev/ttyUSB0` and test the interface connection with :command:`heyu info`.
The response should be something like:

.. code-block:: bash

    $ heyu info
    starting heyu_relay
    Heyu version 2.11-rc1
    Configuration at /home/pi/.heyu/x10config
    Powerline interface on /dev/ttyUSB0
    Firmware revision Level = 1
    Interface battery usage = 17:34  (hh:mm)
    Raw interface clock: Sat, Day 000, 18:03:55
    (--> Civil Time: Sat 01 Jan 2013   18:03:55 PST)
    No schedule has been uploaded by Heyu.
    Housecode = H
    0 = off, 1 = on,               unit  16.......8...4..1
    Last addressed device =       0x0002 (0000000000010000)
    Status of monitored devices = 0x1044 (1000000000000101)
    Status of dimmed devices =    0xa199 (0111011110000000)
