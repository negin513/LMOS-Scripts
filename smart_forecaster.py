#!/usr/bin/env python

import subprocess
import os
import argparse
import glob
import re
import time

from datetime import datetime, timedelta
from namelist_maker import make_wps_namelist, make_wrf_namelist
from qsub_maker import submit_job
from macc_download_maker import make_macc_download, make_macc_inp
    
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
	if err or p.returncode:
		print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print "Oops... This command failed:   "
		print cmd
		print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print err

def get_parser():
    	"""Get parser object for this script."""
    	from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    	parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    	parser = argparse.ArgumentParser(description='Setting the flags and input file.')
    	parser.add_argument('-sst', '--sst', help='Get SST analyses grib version 1 format!'  , action="store_true", dest="sst_switch", default=False)
    	parser.add_argument('--forecast','--now', help='Get SST analyses grib version 1 format!' , action="store_true", dest="now_switch", default=True)
    	return parser	


if __name__ == "__main__":
	
    ## 1) Set your directories
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    parent_dir   = os.path.dirname(script_dir)
    result_dir   = parent_dir+ "/results/"
    wrf_dir      = parent_dir+ "/WRFV3/test/em_real/"
    wps_dir      = parent_dir+ "/WPS/"
    gfs_dir      = parent_dir+ "/gfs_data/"
    macc_dir     = parent_dir+ "/macc_data/"
    moz_dir      = macc_dir  + "mozbc_vMACC/"
    pert78_dir   = parent_dir+ "/WRFV3/test/em_real_78RED/"


    sim_length_hour      = 72 # simulation length hours  
    download_length_hour = 96 # Ask Maryam?!
   
    args         = get_parser().parse_args()
    if args.sst_switch:
        print "\nSST Does not work for now!!!\n"
    
    if args.now_switch:
        start_time = datetime.now()
    #else:  
    #    start_time    = datetime(2017,04,01,00,00,00,00) ### CAN ADD TZ INFO 
    #    print sim_start_time
    

    start_date      = start_time.strftime('%Y%m%d')
    sim_start_time  = start_time + timedelta(days=1)   ## only for LMOS since every day we run for next day
    sim_end_time    = sim_start_time + timedelta(hours= sim_length_hour )

    
    ## 2) step 2: GFS DATA
    gfs_run = '06'

    ch_dir(parent_dir)
    mk_dir(gfs_dir)
    ch_dir(gfs_dir)
    mk_dir(start_date)
    ch_dir(start_date)

    #if (args.now_switch or sim_start_time.date()==datetime.now()):
    for i in range(0,download_length_hour+3,3):
        print "Downloading GFS DATA..."
	gfs_link = 'http://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/MT.gfs_CY.'+gfs_run+'/RD.'+start_date+'/PT.grid_DF.gr2/fh.'+str(i).zfill(4) +'_tl.press_gr.0p50deg'
        #os.system('wget '+gfs_link)
	##subprocess.call(['wget', gfs_link])
    
    
    # 3) step 3: Run WPS 
    #print(wps_dir)
    #print(\
	#"# ---------------------------------------------------------"
	#"# WPS"
	#"# run link_grib.csh"
	#"# run ungrib.exe"
	#"# run metgrid.exe"
	#"# ---------------------------------------------------------")

    #ch_dir(wps_dir)
    
    #make_wps_namelist(\
    #        str(sim_start_time.year),str(sim_start_time.month),str(sim_start_time.day),\
    #        str(sim_end_time.year),str(sim_end_time.month),str(sim_end_time.day))
    
    ####cmd = ["./geogrid.exe", "2>&1","|tee", "geogrid.log"]
    ####execute(cmd)
    
    #os.system('rm -rf met_em* PFILE* FILE*')
    #os.system('./geogrid.exe >& geogrid.log')
    #os.system('./link_grib.csh '+parent_dir+'/gfs_data/'+start_date+'/*')
    #os.system('ln -sf ungrib/Variable_Tables/Vtable.GFS_new.1 Vtable')
    #os.system('./ungrib.exe >&  ungrib.log')
    #os.system('./metgrid.exe 2>&1 |tee metgrid.log')

    #4) step 4: Run real.exe
    #ch_dir(wrf_dir)
    #os.system('rm -rf met_em*')
    #os.system('rm -rf wrfbdy_d01 wrfinput_d01')
    #os.system('ln -sf '+ wps_dir + 'met_em* .')
    #make_wrf_namelist(\
    #        str(sim_start_time.year),str(sim_start_time.month),str(sim_start_time.day),\
    #        str(sim_end_time.year),str(sim_end_time.month),str(sim_end_time.day))
    #real_ID  = submit_job('real.exe',56 , 0, 'CGRER')

    # 5) step 5: MACC data 
    #macc_start_time    = sim_start_time - timedelta(days=1)
    #ch_dir(parent_dir)
    #mk_dir(macc_dir)    
    #ch_dir(macc_dir)
    #make_macc_download(str(macc_start_time.year),str(macc_start_time.month),str(macc_start_time.day))
    #os.system('sh macc_download.sh')
    #time.sleep(300)
    # 6) step 6: run mozbc (This one is dependent on finishing real"
    #while not os.path.isfile(wrf_dir+"wrfbdy_d01"):
    #	print "Waiting for real.exe to finish"
    #	print "Zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    
    #ch_dir(moz_dir)
    #os.system('ln -sf '+ wrf_dir+'wrfinput_d01 .')
    #os.system('ln -sf '+ wrf_dir+'wrfbdy_d01 .')
    #make_macc_inp(str(macc_start_time.year),str(macc_start_time.month),str(macc_start_time.day))
    #os.system('ln -sf '+ wps_dir+'met_em* .')
    #os.system('./mozbc < MACC_LMOS_d01.inp ')

    #ch_dir(wrf_dir)
    #wrf_ID   = submit_job('wrf.exe', 224, 0 , 'CGRER')

    #### PERTURBATIONS
    ch_dir(pert78_dir)
    #os.system('rm -rf met_em*')
    #os.system('rm -rf wrfbdy_d01 wrfinput_d01')
    os.system('ln -sf '+ wps_dir + 'met_em* .')
    make_wrf_namelist(\
            str(sim_start_time.year),str(sim_start_time.month),str(sim_start_time.day),\
            str(sim_end_time.year),str(sim_end_time.month),str(sim_end_time.day))
    real_ID_pert78  = submit_job('real.exe',56 , 0, 'CGRER')
    time.sleep(500)

    ch_dir(moz_dir)
    os.system('ln -sf '+ pert78_dir+'wrfinput_d01 .')
    os.system('ln -sf '+ pert78_dir+'wrfbdy_d01 .')
    os.system('./mozbc < MACC_LMOS_d01.inp ')
    ch_dir(pert78_dir)
    wrf_ID_pert78   = submit_job('wrf.exe', 224, 0 , 'CGRER')

    ## VISUALTIZATION
   


    





	









	
