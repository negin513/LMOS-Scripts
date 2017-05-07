#!/usr/bin/env python

import subprocess
import os
import argparse
import glob
import re
import time

    
def ch_dir(dir):
	cmd_line  = "cd "+ dir
	#print cmd_line 
	os.chdir(os.path.expanduser(dir)) # Is there any way to do this with subrpocess???
	#print "\nCurrent Directory:\n\t"+os.getcwd()+'\n'

def mk_dir(dir):
	cmd_line  = "mkdir "+ dir
	#print cmd_line
	subprocess.call(["mkdir", dir])	

def execute(cmd):
	#should fix this .....
    	p = subprocess.Popen(cmd, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    	out, err = p.communicate()
	print out

if __name__ == "__main__":
	 script_dir     = os.path.dirname(os.path.abspath(__file__))
   	 parent_dir     = os.path.dirname(script_dir)
    	 result_dir     = parent_dir+ "/results/"
	 CGRER_html_dir = parent_dir+ "/CGRER_html/"
	 
	 mk_dir(CGRER_html_dir)
	 ch_dir(CGRER_html_dir)

