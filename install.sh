#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

BASEDIR=`pwd`

chmod +x $BASEDIR/frpg.py
chmod +x $BASEDIR/prpg.py

ln -s $BASEDIR/frpg.py /usr/local/bin/frpg
ln -s $BASEDIR/prpg.py /usr/local/bin/rpg

echo "Done."