#!/usr/bin/python

import sha
import re
import hmac
import commands
from os.path import expanduser, exists

def get_host_by_name(hostname):
    ptn_ip = re.compile(r"\d+\.\d+\.\d+\.\d+")
    if ptn_ip.match(hostname):
        return hostname

    ip = ""
    try:
        import socket
        #NOTE: if return value is not constant, we treat it as configuration error.
        ip = socket.gethostbyname(hostname)
        if ip.startswith("127") and not hostname.startswith("localhost"):
                stdout = run_cmd("host %s" % hostname)
                l = [ line.split()[-1] for line in stdout.splitlines()]
                l = [_ip for _ip in l if ptn_ip.match(_ip)]
                l.sort()
                if l:
                    ip = l[0]
    except:
        pass
    return ip

#know_hosts format
#man sshd
#hostnames bits exponent modulus comment
#should i use construct?
#http://wntrknit.freeshell.org/decrypt_known_hosts

class KnownHosts(object):
    def __init__(self, known_hosts=expanduser("~/.ssh/known_hosts")):
        self.known_hosts = known_hosts
        self.hosts = {}
        self.__unmarshall()

    def __unmarshall(self):
        f = open(self.known_hosts)
        try:
            for line in f:
                #preprocess
                line = line.strip()
                if line.startswith("#"): continue
                if not line: continue 
                hostnames = line.split()[0]
                self.hosts[hostnames] = line    
        finally:
            f.close()

    def marshall(self):
        f = open(self.known_hosts, "w")
        try:
            for h in self.hosts:
                f.write("%s\n" % self.hosts[h])
        finally:
            f.close()

    def remove(self, hostname):
        #get hostname alias
        alias = [hostname, ]
        if "." in hostname:
            short_hostname = hostname.split(".")[0]
            alias.append(short_hostname)
        else:
            found_in_ssh_config = False
            ssh_config = expanduser("~/.ssh/config")
            if exists(ssh_config):
                cmd = r"sed -n -r -e '/^Host %s/,/Host/ s/^\s+HostName\s+(.*)$/\1/p' %s" % \
                        (hostname, ssh_config)
                h = commands.getoutput(cmd).strip()
                if h and not h in alias: 
                    found_in_ssh_config = True
                    alias.append(h)

            if not found_in_ssh_config:
                cmd = "grep search /etc/resolv.conf" 
                status, output = commands.getstatusoutput(cmd)
                if status == 0:
                    domain = output.split()[-1]
                    h =  "%s.%s"% (hostname, domain) 
                    if not h in alias: 
                        alias.append(h)
        
        for h in alias[:]:
            ip = get_host_by_name(h)
            if ip and ip not in alias: 
                alias.append(ip)
        
        print "%r => %r" % (hostname, alias)
       
        #clear text hostname
        for h in alias: #h is a hostname
            if h in self.hosts:
                print "del %-32s => %s" % (h, self.hosts[h])
                del self.hosts[h]

        #hashed hostname
        for h in self.hosts.keys(): #h is a hash record
            if h.startswith("|1|"):
                salt, hash = h[3:].split("|")
                d = dict([ (hmac.new(salt.decode("base64"), x, sha.new).digest().encode("base64").strip(), x)
                            for x in alias])
                if  hash in d:
                    del self.hosts[h]
                    print "del %-32s => %s" % (d[hash], h)

if __name__ == "__main__":
    import sys

    kh = KnownHosts()
    for hostname in sys.argv[1:]:
        kh.remove(hostname)
    kh.marshall()

