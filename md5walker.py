#!/usr/bin/python -u

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os, os.path
#import ConfigParser
#import re
#import tempfile
#import optparse
import sys
#import commands
import hashlib

mode=None

if len(sys.argv)==2:
    if sys.argv[1]=="check":
        mode="c"
    elif sys.argv[1]=="update":
        mode="u"
    else:
        print "argument must be check or update"
        print "check only checks. update only updates missing or updated files"
        print "without any arguments, both is done, plus not matching sums with correct mtimes are updated."
        sys.exit(1)


directories=[os.getcwd()]

def announce_and_execute(command, safe=False):
    print "in "+os.getcwd()+": "+command
    retval=os.system(command)
    if safe and retval != 0:
        print command + "returned value " + retval

def md5_file(fullpath):
    m=hashlib.md5()
    file=open(fullpath)
    tmp=file.read(1024*1024)
    while(tmp!=""):
        m.update(tmp)
        tmp=file.read(1024*1024)
    return m.hexdigest()

def create_md5_file(fullpath):
    print "creating md5 file for "+fullpath
    md5file=open(fullpath+".md5",'w')
    md5file.write(md5_file(fullpath)+"\n")
    md5file.close()
    
while len(directories)>0:
    directory=directories.pop()
    tmplist=os.listdir(directory)
    tmplist.sort()
    for dir in tmplist:
        fullpath=os.path.join(directory,dir)
        if os.path.isfile(fullpath):

            if len(fullpath)<=4 or (len(fullpath) >4 and not fullpath[-4:]==".md5"):
                if os.path.isfile(fullpath+".md5"):
                    if os.path.getmtime(fullpath+".md5") < os.path.getmtime(fullpath):
                        if mode==None or mode=="u":
                            create_md5_file(fullpath)
                    elif mode==None or mode=="c":
                        md5computed=md5_file(fullpath)+"\n"
                        md5stored=open(fullpath+".md5",'r').read()
                        if md5computed != md5stored:
                            print "md5sum for "+fullpath+" does not match! "
                            if mode==None:
                                print "creating new..."
                                create_md5_file(fullpath)
                        else:
                            continue
                            #print fullpath+" ok"

                elif mode==None or mode=="u":
                    create_md5_file(fullpath)

            else:
                if not os.path.isfile(fullpath[:-4]):
                    print "Deleting orphan md5 file "+fullpath
                    os.unlink(fullpath)
                    continue

        elif os.path.isdir(fullpath):
            directories.append(fullpath)
