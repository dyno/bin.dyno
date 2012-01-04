#!/usr/bin/python

from __future__ import with_statement

import re
from os.path import exists

ptn_sn = re.compile(r"\d+\s*$")
ptn_frame = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$")

def validate(sub_file):
    print "validate '%s' ..." % sub_file
    fix_bom = False
    with open(sub_file) as f:
        lines = f.read().splitlines()
        for idx, line in enumerate(lines):
            if ptn_sn.match(line):
                if not ptn_frame.match(lines[idx + 1]):
                    print "invalid: %4s => %s" % (line, lines[idx + 1])
                    return
            elif idx == 0:
                if line.startswith("\xef\xbb\xbf"):
                    fix_bom = True
                    if not ptn_frame.match(lines[idx + 1]):
                        print "invalid: %4s => %s" % (line[3:], lines[idx + 1])
                        return

    if not fix_bom: 
        print "done."
        return

    print "remove byte order mark..."
    with open(sub_file, "w") as f:
        lines[0] = lines[0][3:]
        f.write("\n".join(lines))

    print "done."

if __name__ == "__main__":
    import sys
    if sys.argv > 1:
        l = sys.argv[1:]
    else:
        from glob import glob
        l= glob("*.avi")

    for movie in l:
        sub_file = "%s.srt" % movie[:-4]
        if exists(sub_file):
            validate(sub_file)
