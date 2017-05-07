#!/usr/bin/env python

import subprocess
import os
import argparse
import glob
import re
import time
def runCmd(exe):
    p = subprocess.Popen(exe,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        retcode = p.poll()
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break
def hasRQJob():
    jobs = runCmd('qstat')
    for line in jobs:
        columns = line.split()
        if columns[-2] in ('Q','R'): return True
    return False

def is_running():
	cmd = ['qstat','-u','mabdioskouei']
        p = subprocess.Popen(cmd, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
        out, err = p.communicate()
	print out


if __name__ == "__main__":
	is_running()
	hasRQJob()

