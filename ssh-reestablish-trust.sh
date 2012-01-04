#!/bin/bash

# somethime os has been reinstall on the remote host, 
# trust connection needs to be reestablished.

#1. remove hosts from my known_hosts
#2. cp my public key to hosts' authorized_keys

if ! ( grep -q "/" <<< "$0" ); then
    cd $(dirname $(which $0))
else
    cd $(dirname $0)
fi

for r in $@; do
    username=$(awk -v FS=@ '{if (NF == 2) print $1;}' <<< "$r")
    if [ ! -n "$username" ]; then username=root; fi
    hostname=$(awk -v FS=@ '{print $NF}' <<< "$r")
    echo $username@$hostname    
   
    ./ssh-remove-knownhosts.py $hostname

    if [ ! -f ~/.ssh/id_rsa.pub ]; then 
	echo "public key not found!" 
	continue
    fi
    #add my public key to host's authorized_keys 
    host="$username@$hostname"
    scp ~/.ssh/id_rsa.pub $host:/tmp/id_rsa.pub.tmp
    ssh $host 'mkdir -p ~/.ssh; touch ~/.ssh/authorized_keys; mark=$(awk "{print \$NF;}" /tmp/id_rsa.pub.tmp); sed -i -e "/$mark/d" ~/.ssh/authorized_keys; cat /tmp/id_rsa.pub.tmp >> ~/.ssh/authorized_keys'
    #test the trusted connection
    ssh $host 'hostname'
done
