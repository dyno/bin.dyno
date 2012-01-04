#!/bin/sh
#this will download the installed package deb file
#then use dbkg -i --force-<action> $1 force reinstall the package
if [ $# == 1 ]
then
    echo sudo apt-get --download-only --reinstall $1
fi
