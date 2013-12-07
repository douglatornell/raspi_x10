***********************
RaspberryPi Admin Notes
***********************

First Boot
==========

:program:`raspi-config` comes up after the boot scripts run.
It can be run later from the command line with :command:`sudo raspi-config`.
See http://elinux.org/RPi_raspi-config.

Set the keyboard layout:

* Generic PC 104 keys
* English (US) (twice)
* AltGr default for keyboard layout
* No compose key
* Set Ctrl-Alt-Backspace to terminate X server

Change pi user password.

Choose the :kbd:`en_CA.UTF-8 UTF-8` locale and set it as the default locale for the system environment.

Set the timezone to :kbd:`America/Vancouver`.

Enable the :program:`ssh` server.

Set the boot behaviour to boot to the command line;
from there the desktop GUI can be started with :command:`startx`.

Reboot.


Initial Setup
=============

Create :file:`$HOME/.ssh/` and :program:`scp` public :program:`ssh` key into :file:`$HOME/.ssh/authorized_keys`.
Configure :program:`ssh` logins from laptop.

Update package cache with :command:`sudo apt-get update`.

Install Mercurial with :command:`sudo apt-get install mercurial`.

Install :program:`mg` editor with :command:`sudo apt-get install mg`.

Clone :file:`dotfiles` repo from Bitbucket,
move :file:`.bash_logout`,
:file:`.bashrc`,
and :file:`.profile` into it and symlink them into :file:`$HOME` directory.
Set up :file:`.hgrc` and :file:`.hgignore` and symlink them into :file:`$HOME`.
Create :file:`.bash_aliases` for personal aliases and envvar settings and symlink it into :file:`$HOME`.
