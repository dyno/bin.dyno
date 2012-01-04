#!/bin/bash
#fix error for NO_PUBKEY

[ -z "$1" ] && { echo "no key specified!"; exit 1; }

pubkey=$1
gpg --keyserver keyserver.ubuntu.com --recv $pubkey
gpg --export --armor $pubkey | sudo apt-key add -

