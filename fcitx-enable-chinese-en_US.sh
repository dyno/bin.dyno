#!/bin/bash

cfg_file=$(find /usr/lib/gtk-2.0/ -name libgtk2.0-0.immodules)
sudo patch -N $cfg_file < libgtk2.0-0.immodules.patch

if [ -f ${cfg_file}.rej ]; then
    sudo rm ${cfg_file}.rej
fi
