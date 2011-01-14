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
#import sys
#import commands
import hashlib


directories=[os.getcwd()]

def announce_and_execute(command, safe=False):
    print "in "+os.getcwd()+": "+command
    retval=os.system(command)
    if safe and retval != 0:
        print command + "returned value " + retval

def md5_file(fullpath):
    m=hashlib.md5()
    m.update(open(fullpath).read())
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
                        create_md5_file(fullpath)
                    else:
                        md5computed=md5_file(fullpath)+"\n"
                        md5stored=open(fullpath+".md5",'r').read()
                        if md5computed != md5stored:
                            print "md5sum for "+fullpath+" does not match! creating new..."
                            create_md5_file(fullpath)
                            
                else:
                    create_md5_file(fullpath)

            else:
                if not os.path.isfile(fullpath[:-4]):
                    print "Deleting orphan md5 file "+fullpath
                    os.unlink(fullpath)
                    continue

        elif os.path.isdir(fullpath):
            directories.append(fullpath)
