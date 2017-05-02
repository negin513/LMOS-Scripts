#!/usr/bin/env python

import subprocess
import os
import argparse
import glob
import re

import time
from datetime import datetime, timedelta

from namelist_maker import make_wps_namelist
from namelist_maker import make_wrf_namelist
from qsub_maker import make_qsub
from job_submitter import submit_job
from macc_download_maker import make_macc_download
## What do we do?
## 1) 
    
def ch_dir(dir):
	cmd_line  = "cd "+ dir
	#print cmd_line 
	os.chdir(os.path.expanduser(dir)) # Is there any way to do this with subrpocess???
	#print "\nCurrent Directory:\n\t"+os.getcwd()+'\n'

def mk_dir(dir):
	cmd_line  = "mkdir "+ dir
	#print cmd_line
	subprocess.call(["mkdir", dir])	

def get_parser():
    	"""Get parser object for this script."""
    	from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    	parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    	parser = argparse.ArgumentParser(description='Setting the flags and input file.')
    	#parser.add_argument('-T', '--tag', help='Add a tag to your work.',required=True, action="store", dest="tag")
    	parser.add_argument('-sst', '--sst', help='Get SST analyses grib version 1 format!'  , action="store_true", dest="sst_switch", default=False)
    	parser.add_argument('--now', help='Get SST analyses grib version 1 format!'  , action="store_true", dest="now_switch", default=False)
    	parser.add_argument('-fir', '--fire', help='Get SST analyses grib version 1 format!'  , action="store_true", dest="sst_switch", default=False)
    	return parser	

if __name__ == "__main__":
	
	## 1) Set your directories
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    parent_dir   = os.path.dirname(script_dir)
    result_dir   = parent_dir+ "/results/"
    wrf_dir   = parent_dir+ "/WRFV3/test/em_real/"
    wps_dir   = parent_dir+ "/WPS/"
    macc_dir  = parent_dir+"/macc_data/"
    args         = get_parser().parse_args()
    if args.sst_switch:
        print "\nWTF\n"

    sim_length_hour = 48 # simulation length hours
    download_length_hour = 72 
   
    if args.now_switch:
        sim_start_time = datetime.now()
        print sim_start_time
    else:
        sim_start_time    = datetime(2017,04,01,00,00,00,00) ### CAN ADD TZ INFO 
        print sim_start_time
        
    sim_end_time    = sim_start_time + timedelta(hours= sim_length_hour )
    print sim_end_time

    sim_start_date = sim_start_time.strftime('%Y%m%d')
    print sim_start_date
	## 2) step 2: GFS DATA
    gfs_run = '06' ## WHAT IS THIS?

    ch_dir(parent_dir)
    mk_dir('gfs_data')
    ch_dir('gfs_data')
    mk_dir(sim_start_date)
    ch_dir(sim_start_date)

    # GFS data for today is available
    if (args.now_switch or sim_start_time.date()==datetime.now()):
        for i in range(0,download_length_hour+3,3):
		    #downloading data
		    print "not downloading"
		    #os.system('wget http://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/MT.gfs_CY.'+gfs_run+'/RD.'+sim_start_date+'/PT.grid_DF.gr2/fh.'+str(i).zfill(4) +'_tl.press_gr.0p50deg')
    
    # MACC date
    #mac_start_time    = sim_start_time - timedelta(hours= 48)
    ch_dir(parent_dir)
    mk_dir(macc_dir)    
    ch_dir(macc_dir)
    make_macc_download(str(sim_start_time.year),str(sim_start_time.month),str(sim_start_time.day))
    os.system('sh macc_download.sh')
   
    #ch_dir(parent_dir)
    #mk_dir('MACC_data')
    #ch_dir('MACC_data')

    #os.system()
    
    #print(wps_dir)
	#"# ---------------------------------------------------------"
	#"# run WPS"
	#"# run link_grib.csh"
	#"# run ungrib.exe"
	#"# run metgrid.exe"
	#"# ---------------------------------------------------------"

	## cleaning the WPS directory
    ## ****
    ch_dir(wps_dir)
    os.system('./link_grib.csh '+parent_dir+'/gfs_data/'+sim_start_date+'/*')
    sim_start_time = sim_start_time + timedelta(days=1)
    make_wps_namelist(\
            str(sim_start_time.year),str(sim_start_time.month),str(sim_start_time.day),\
            str(sim_end_time.year),str(sim_end_time.month),str(sim_end_time.day))
    os.system('ln -sf ungrib/Variable_Tables/Vtable.GFS_new.1 Vtable')
    os.system('./ungrib.exe >& ungrib.log')
    os.system('./metgrid.exe >& metgrid.log')


    ### Run real.exe
    ch_dir(wrf_dir)
    os.system('ln -sf '+ wps_dir + 'met_em* .')
    make_wrf_namelist(\
            str(sim_start_time.year),str(sim_start_time.month),str(sim_start_time.day),\
            str(sim_end_time.year),str(sim_end_time.month),str(sim_end_time.day))
    make_qsub('real.exe',112)
    submit_job('run_real.exe.sh')



    





	









	
